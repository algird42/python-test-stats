# Python Text Stats

A small, dependency-free Python project that analyzes text from the command
line. It demonstrates a clean `src` layout, type hints, a reusable library API,
and automated tests.

## Features

- Count characters, words, unique words, sentences, and lines.
- Display the most frequent words.
- Read text from an argument, a UTF-8 file, or standard input.
- Produce either a readable report or JSON.
- Run without third-party runtime dependencies.

## Requirements

- Python 3.10 or newer

## Quick start

Run directly from the project directory:

```powershell
$env:PYTHONPATH = "src"
python -m text_stats "Python is simple. Python is powerful!"
```

Analyze a file:

```powershell
$env:PYTHONPATH = "src"
python -m text_stats --file README.md --top 8
```

Return JSON:

```powershell
$env:PYTHONPATH = "src"
python -m text_stats --json "Hello, GitHub!"
```

## Install locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
text-stats "One sentence. Another sentence."
```

## Tests

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Project structure

```text
python-text-stats/
├── src/text_stats/
│   ├── __init__.py
│   ├── __main__.py
│   ├── analyzer.py
│   └── cli.py
├── tests/
│   └── test_analyzer.py
├── pyproject.toml
└── README.md
```

## License

MIT

