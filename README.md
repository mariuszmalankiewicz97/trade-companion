# Trade Companion

A Python application for scanning and analyzing stocks for swing trading opportunities.

## Project Goal

The goal of this project is to build a stock scanner that analyzes market data and identifies potential long trading setups.

The project is being developed using a test-driven development (TDD) approach.

## Technologies

* Python 3.14+
* pandas
* NumPy
* yfinance
* pytest
* Ruff
* Visual Studio Code

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/mariuszmalankiewicz97/trade-companion.git
cd trade-companion
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -e .
```

## VS Code Setup

Install the **Ruff** extension in Visual Studio Code.

Open the Extensions panel:

```text
Ctrl + Shift + X
```

Search for:

```text
Ruff
```

Install the **Ruff** extension by Astral Software.

To enable automatic formatting and fixes on save, open the VS Code `settings.json`:

```text
Ctrl + Shift + P
→ Preferences: Open User Settings (JSON)
```

Add:

```json
{
    "editor.formatOnSave": true,

    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit"
        }
    }
}
```

## Running Tests

Run all tests with:

```bash
pytest
```

## Ruff

Ruff is used for code linting and formatting.

Check the project for code issues:

```bash
ruff check .
```

Automatically fix issues that Ruff can fix:

```bash
ruff check . --fix
```

Format the code:

```bash
ruff format .
```

## Features

The project is currently under development.

Planned features:

* fetching stock market data,
* ticker validation,
* technical indicator analysis,
* High/Low pivot detection,
* support and resistance zone detection,
* volume analysis,
* Risk/Reward analysis,
* filtering potential long setups.

## Project Structure

```text
trade-companion/
├── src/
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Status

🚧 Work in progress.

## Author

Mariusz Malankiewicz
