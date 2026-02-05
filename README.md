# BBS Converter

Real-time Poker HUD to Big Blinds (BB/s) converter. Captures on-screen poker HUD data via screen capture and OCR, converts chip counts and pot sizes into big blind units, and displays the results as an overlay.

## Architecture

```
Screen Capture → OCR → Parse → Convert → Overlay
     (mss)    (tesseract) (regex)  (math)  (opencv)
```

**Modules:**

| Module | Responsibility |
|---|---|
| `capture` | Screen region selection and frame grabbing at ≥30 FPS |
| `ocr` | Text extraction from captured frames using Tesseract |
| `parser` | Structured data extraction from raw OCR text (stacks, blinds, pot) |
| `converter` | Chip-to-BB arithmetic |
| `overlay` | Transparent on-screen display of converted values |
| `utils` | Shared helpers (config, logging, timing) |

## Prerequisites (macOS)

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python

```bash
brew install python@3.11
```

Verify with:

```bash
python3 --version
```

### 3. Install Tesseract OCR

```bash
brew install tesseract
```

Verify with:

```bash
tesseract --version
```

### 4. Grant Screen Recording Permission

macOS requires screen recording permission for screen capture to work.

1. Open **System Settings → Privacy & Security → Screen Recording**
2. Enable your terminal app (Terminal, iTerm2, etc.)
3. Restart the terminal after granting permission

## Setup

```bash
git clone https://github.com/parthhar/bbs-converter.git
cd bbs-converter
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
# Run with defaults (launches setup wizard on first run)
bbs-converter

# Specify capture region directly
bbs-converter --region 100,200,800,600

# Set target FPS and OCR confidence threshold
bbs-converter --fps 30 --confidence 70

# Use a custom config file
bbs-converter --config config.toml
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=bbs_converter

# Run a specific test file
pytest tests/unit/test_converter_core.py

# Run tests matching a keyword
pytest -k "parser"
```

## Linting

```bash
ruff check src/ tests/
```
