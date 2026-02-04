# Architecture

## Pipeline

The application runs a continuous pipeline at ≥30 FPS:

```
┌─────────┐    ┌─────┐    ┌────────┐    ┌───────────┐    ┌─────────┐
│ Capture  │───▶│ OCR │───▶│ Parser │───▶│ Converter │───▶│ Overlay │
└─────────┘    └─────┘    └────────┘    └───────────┘    └─────────┘
```

### 1. Capture (`bbs_converter.capture`)

- Uses `mss` for cross-platform screen capture
- User selects a screen region on first run
- Delivers frames as NumPy arrays to the OCR stage
- Target: ≥30 FPS capture rate

### 2. OCR (`bbs_converter.ocr`)

- Preprocesses frames (grayscale, threshold, denoise) for OCR accuracy
- Runs Tesseract via `pytesseract` to extract text
- Returns raw text strings per frame

### 3. Parser (`bbs_converter.parser`)

- Extracts structured data from raw OCR text using regex patterns
- Identifies: player stacks, blind levels, pot size
- Outputs a `TableState` dataclass

### 4. Converter (`bbs_converter.converter`)

- Takes `TableState` and the current big blind value
- Converts all chip amounts to BB units
- Pure arithmetic — no I/O, fully testable

### 5. Overlay (`bbs_converter.overlay`)

- Renders converted values on a transparent window positioned over the poker client
- Uses OpenCV for rendering

## Data Flow

```python
@dataclass
class TableState:
    big_blind: float
    small_blind: float
    pot: float
    stacks: dict[str, float]  # player_name -> chip_count

@dataclass
class BBState:
    pot_bb: float
    stacks_bb: dict[str, float]  # player_name -> bb_count
```

## Performance Budget

| Stage | Target |
|---|---|
| Capture | ≤5ms |
| OCR | ≤20ms |
| Parse | ≤1ms |
| Convert | ≤1ms |
| Overlay | ≤5ms |
| **Total** | **≤33ms (30 FPS)** |

## Threading Model

- Capture runs on a dedicated thread, pushing frames to a queue
- OCR + Parse + Convert runs on the main processing thread
- Overlay runs on the main GUI thread
- Thread-safe queue connects capture to processing
