from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .analyzer import PythonTestGapAnalyzer
from .repository import RepositoryResolver
from .stub_writer import StubWriter


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect Python modules without matching pytest files and scaffold stubs.",
    )
    parser.add_argument(
        "repo",
        help="Path or git URL of the repository to inspect.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Destination directory for generated tests (defaults to <repo>/.generated_tests).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of modules to process.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print the plan without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Increase logging verbosity.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(args.verbose)

    resolver = RepositoryResolver()
    with resolver.obtain(args.repo) as context:
        repo_path = context.path
        analyzer = PythonTestGapAnalyzer(repo_path)
        plans = analyzer.plan_missing_tests(limit=args.limit)

        if not plans:
            logging.info("No missing pytest modules were detected.")
            return 0

        if args.dry_run:
            for plan in plans:
                logging.info(
                    "Missing tests for %s -> %s (%d targets)",
                    plan.module.display_name,
                    plan.test_relative_path,
                    len(list(plan.iter_symbol_names())),
                )
            return 0

        writer = StubWriter(repo_path, args.output)
        written = writer.write(plans, overwrite=args.force)
        for path in written:
            logging.info("Generated %s", path.relative_to(repo_path))

        skipped = len(plans) - len(written)
        if skipped:
            logging.info(
                "Skipped %d files because they already existed. Use --force to overwrite.",
                skipped,
            )

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
