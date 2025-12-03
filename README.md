# Test Gap Helper

A lightweight CLI that scans a repository for Python modules that lack
matching pytest files and scaffolds placeholder tests for those gaps. The goal
is to give you a head start when backfilling missing coverage across many
projects.

## Requirements

- Python 3.10+
- `git` available on your PATH
- `pytest` only if you intend to execute the generated stubs

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest  # optional, only to run generated tests
python3 main.py /path/to/target/repo
```

Point the CLI at either a local path or any git URL. Remote repositories are
cloned into a temporary directory automatically:

```bash
python3 main.py https://github.com/pallets/flask --limit 5 --dry-run
```

## Command reference

| Flag | Description |
|------|-------------|
| `repo` (positional) | Path or git URL to inspect |
| `--output` | Directory where stub files are written (default: `<repo>/.generated_tests`) |
| `--limit` | Upper bound on the number of modules to process |
| `--dry-run` | Print the plan without writing files |
| `--force` | Overwrite previously generated files |
| `--verbose` | Emit debug logging |

## How it works

1. The repository is prepared locally (using the passed path or a shallow git clone).
2. Each Python module outside `tests/` is parsed with `ast` to collect public functions and classes.
3. Modules that do not have a matching `test_*.py` file are turned into generation plans.
4. Plans become pytest stub files under the chosen output directory, each failing with a helpful message until you fill in real assertions.

The output always lives outside the inspected repository's code so that you can
review, move, or delete the generated files before copying them in.
