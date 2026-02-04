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

## Requirements

- Python 3.10+
- Tesseract OCR installed on the system
- A running poker client with visible HUD

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
bbs-converter
```

## Testing

```bash
pytest
pytest --cov=bbs_converter
```
