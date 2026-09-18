# CSV Contact Keep

> Interactive terminal directory manager utilizing localized flat-file storage and standard library synchronization mechanics.

## Overview

Managing simple personal directories often leads to introducing heavy database dependencies or external dynamic web tools. `csv-contact-keep` solves this operational friction by providing an isolated, terminal-based workflow for contact record insertion, formatted lookup, and fast field querying. It requires zero network connectivity, operates without binary compile steps, and leverages standard flat-file serialization to ensure your data stays readable by simple terminal primitives or spreadsheet tooling.

## How It Works

The system operates on an in-memory collection of key-value maps synchronized with localized disk storage:

1. **State Initialization:** Upon startup, `load_contacts` checks for `contacts.csv` using `pathlib.Path`. If present, the stream uses `csv.DictReader` to map headers (`Name`, `Phone`, `Email`, `Notes`) into standard Python `dict` instances contained within a top-level `list`. Missing files trigger a silent default fallback to an empty state rather than raising an uncaught exception.
2. **In-Memory Operations:** Addition and substring operations execute entirely against the primary standard `list` data structure. Search operations run full-table scans via list comprehensions with string standardizations (`.lower()`) to deliver case-insensitive substring matches.
3. **Persisted Mutations:** Updates stream to disk through `csv.DictWriter`, rewriting the local target via fixed schema rules (`CSV_HEADERS`). File handlers explicit set `newline=""` and `encoding="utf-8"` to maintain consistent line endings across platforms.

## Key Features

- **Flat-File Persistence:** Automatic creation and synchronization with localized CSV storage.
- **Substring Field Matching:** Case-insensitive search mechanics over stored contact identifiers.
- **Schema Validation:** Strict non-empty string enforcement on core fields before mutation steps trigger.
- **Cross-Platform IO Handling:** Defensive error catching for explicit disk read/write permissions (`IOError`, `csv.Error`).

## Tech Stack & Core Dependencies Breakdown

- **Language:** Python 3.10+
- **Standard Library Modules:**
  - `csv`: Engine responsible for standard data formatting, record reading, and row writing.
  - `pathlib`: Handles platform-agnostic file system paths.
  - `sys`: Handles predictable program exits via explicit exit codes (`sys.exit(0)`).

No external third-party dependencies are required.

## Environment & Web-Based Quick Start

### Running in GitHub Codespaces
1. Click the **Code** button at the top of the repository.
2. Select the **Codespaces** tab and click **Create codespace on main**.
3. Open the integrated terminal and execute:
   ```bash
   python main.py
   ```

### Local Virtual Environment Setup

```bash
# Clone or create your project directory
python -m venv .venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Run the utility
python main.py
```

## Repository Structure

```text
csv-contact-keep/
├── .github/
│   └── workflows/
│       └── ci.yml             # Automated syntax validation check workflow
├── .gitignore                 # Platform and Python artifact exclusion rules
├── LICENSE                    # MIT License open-source terms
├── README.md                  # Comprehensive repository documentation
└── main.py                    # Interactive CLI application entry point and logic
```

## Roadmap

**Type Safety Extensions:** Introduce explicit .pyi type stub declarations or convert data representations to dataclasses for tighter internal validation.

**Atomic Disk Synchronization:** Replace standard direct file rewrites with temporary write-and-replace patterns using tempfile to prevent payload loss during system interruptions.

**Configurable Storage Targets:** Enable dynamic CLI argument parsing (argparse) to support custom file path destinations at launch time.
