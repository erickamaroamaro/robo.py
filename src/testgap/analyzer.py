from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from .models import ModuleSummary, SymbolTarget, TestStubRequest


@dataclass(slots=True)
class AnalyzerConfig:
    tests_dir_name: str = "tests"
    include_packages: Sequence[str] = ()
    exclude_dirs: Sequence[str] = (".git", "__pycache__", ".venv", ".idea")


class PythonTestGapAnalyzer:
    """Finds Python modules that lack sibling pytest modules."""

    def __init__(self, repo_root: Path, config: AnalyzerConfig | None = None) -> None:
        self.root = repo_root
        self.config = config or AnalyzerConfig()

    def plan_missing_tests(self, limit: int | None = None) -> list[TestStubRequest]:
        module_summaries = list(self._iter_non_test_modules())
        tests = set(self._iter_test_module_keys())

        plans: list[TestStubRequest] = []
        for summary in module_summaries:
            key = summary.relative_path.with_suffix("").name
            if key in tests:
                continue
            targets = self._collect_targets(summary)
            if not targets:
                continue
            test_rel = self._suggest_test_path(summary)
            plans.append(TestStubRequest(summary, test_rel, targets))
            if limit and len(plans) >= limit:
                break
        return plans

    def _iter_non_test_modules(self) -> Iterator[ModuleSummary]:
        for file_path in self.root.rglob("*.py"):
            if self._should_skip(file_path):
                continue
            if self._is_test_file(file_path):
                continue
            module = self._summarize_module(file_path)
            if module:
                yield module

    def _iter_test_module_keys(self) -> Iterable[str]:
        for file_path in self.root.rglob("*.py"):
            if self._is_test_file(file_path):
                yield self._canonical_test_key(file_path)

    def _should_skip(self, file_path: Path) -> bool:
        rel = file_path.relative_to(self.root)
        for part in rel.parts:
            if part in self.config.exclude_dirs:
                return True
        return False

    def _is_test_file(self, file_path: Path) -> bool:
        rel = file_path.relative_to(self.root)
        if self.config.tests_dir_name in rel.parts:
            return True
        stem = file_path.stem
        return stem.startswith("test_") or stem.endswith("_test")

    def _canonical_test_key(self, file_path: Path) -> str:
        stem = file_path.stem
        stem = stem.removeprefix("test_")
        stem = stem.removesuffix("_test")
        return stem

    def _summarize_module(self, file_path: Path) -> ModuleSummary | None:
        try:
            source = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        functions: list[str] = []
        classes: list[str] = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith("_"):
                    functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    classes.append(node.name)

        rel_path = file_path.relative_to(self.root)
        module_import = ".".join(rel_path.with_suffix("").parts)
        return ModuleSummary(
            source_path=file_path,
            relative_path=rel_path,
            module_import=module_import,
            defined_functions=tuple(functions),
            defined_classes=tuple(classes),
        )

    def _collect_targets(self, summary: ModuleSummary) -> list[SymbolTarget]:
        targets: list[SymbolTarget] = []
        for func in summary.defined_functions:
            targets.append(SymbolTarget(func, "function"))
        for cls in summary.defined_classes:
            targets.append(SymbolTarget(cls, "class"))
        return targets

    def _suggest_test_path(self, summary: ModuleSummary) -> Path:
        tests_dir = Path(self.config.tests_dir_name)
        module_name = summary.relative_path.with_suffix("").name
        return tests_dir / f"test_{module_name}.py"
