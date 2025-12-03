from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class ModuleSummary:
    """Metadata extracted from a Python module that might need tests."""

    source_path: Path
    relative_path: Path
    module_import: str
    defined_functions: tuple[str, ...] = field(default_factory=tuple)
    defined_classes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return self.relative_path.as_posix()


@dataclass(frozen=True, slots=True)
class SymbolTarget:
    """Represents a function or class that deserves a test stub."""

    name: str
    kind: str  # "function" or "class"


@dataclass(frozen=True, slots=True)
class TestStubRequest:
    """Plan to generate a stub file for a source module."""

    module: ModuleSummary
    test_relative_path: Path
    targets: Sequence[SymbolTarget]

    def iter_symbol_names(self) -> Iterable[str]:
        for target in self.targets:
            yield target.name
