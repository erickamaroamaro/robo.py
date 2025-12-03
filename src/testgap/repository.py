from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Callable, Optional


class RepositoryError(RuntimeError):
    """Raised when a repository cannot be prepared."""


@dataclass
class RepositoryContext:
    """Holds a prepared repository checkout plus its cleanup callback."""

    path: Path
    _cleanup: Callable[[], None]

    def cleanup(self) -> None:
        self._cleanup()

    def __enter__(self) -> "RepositoryContext":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()


class RepositoryResolver:
    """Ensures a repository path exists locally before running analysis."""

    def __init__(self, working_dir: Optional[Path] = None) -> None:
        self.working_dir = working_dir or Path.cwd()

    def obtain(self, source: str) -> RepositoryContext:
        path_candidate = Path(source)
        if path_candidate.exists():
            return RepositoryContext(path_candidate.resolve(), lambda: None)

        return self._clone_remote(source)

    def _clone_remote(self, repo_url: str) -> RepositoryContext:
        destination = Path(mkdtemp(prefix="testgap_repo_"))
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(destination)],
                cwd=str(self.working_dir),
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            rmtree(destination, ignore_errors=True)
            raise RepositoryError(
                f"Unable to clone repository from '{repo_url}': {exc.stderr.strip()}"
            ) from exc

        return RepositoryContext(destination, lambda: rmtree(destination, ignore_errors=True))
