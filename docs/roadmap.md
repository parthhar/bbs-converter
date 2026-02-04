# Development Roadmap

## Component Inventory (46 components, dependency order)

### Phase 1: Foundation & Core Models

Standalone utilities and data models with zero internal dependencies. Everything else builds on this.

| # | Component | Dependencies | Complexity | Priority | Parallel Group |
|---|-----------|-------------|-----------|----------|----------------|
| 1 | `utils/exceptions.py` — Custom error hierarchy | None | S | P0 | A |
| 2 | `utils/constants.py` — Enums, defaults, magic numbers | None | S | P0 | A |
| 3 | `utils/config.py` — Config loader (TOML/dict) | None | S | P0 | A |
| 4 | `utils/logger.py` — Structured logging setup | None | S | P0 | A |
| 5 | `utils/timer.py` — Performance profiler/decorator | None | S | P1 | A |
| 6 | `models.py` — TableState dataclass | None | S | P0 | A |
| 7 | `models.py` — BBState dataclass | None | S | P0 | A |
| 8 | `models.py` — CaptureRegion (x, y, w, h) | None | S | P0 | A |
| 9 | `models.py` — PlayerInfo (name, seat, stack) | None | S | P0 | A |
| 10 | `models.py` — GameConfig (blind structure, ante) | None | S | P0 | A |

> **All 10 components can be developed in parallel (Group A).**

---

### Phase 2: Converter & Parser (Pure Logic, No I/O)

Pure functions with full test coverage. No external dependencies beyond Phase 1 models.

| # | Component | Dependencies | Complexity | Priority | Parallel Group |
|---|-----------|-------------|-----------|----------|----------------|
| 11 | `converter/core.py` — Single value chip→BB | models | S | P0 | B |
| 12 | `converter/batch.py` — Multi-player batch convert | 11 | S | P0 | B (after 11) |
| 13 | `converter/formatter.py` — Rounding & display rules (2.5bb, 100bb+) | 11 | S | P1 | B |
| 14 | `converter/history.py` — Track BB values over time | 6, 7 | M | P2 | B |
| 15 | `parser/stack_parser.py` — Regex: extract player stacks | 6, 9 | M | P0 | C |
| 16 | `parser/blind_parser.py` — Regex: extract blind levels | 6, 10 | M | P0 | C |
| 17 | `parser/pot_parser.py` — Regex: extract pot size | 6 | M | P0 | C |
| 18 | `parser/player_parser.py` — Regex: extract player names/seats | 9 | M | P1 | C |
| 19 | `parser/assembler.py` — Combine sub-parsers → TableState | 15–18 | M | P0 | C (after 15–18) |
| 20 | `parser/sanitizer.py` — Validate/clean parsed values | 1, 19 | S | P1 | C (after 19) |

> **Groups B (converter) and C (parser) can be developed in parallel with each other.**
> Within each group, leaf components come first, then composites.

---

### Phase 3: Screen Capture

I/O-bound module. Depends on Phase 1 models only, so can overlap with Phase 2 in practice.

| # | Component | Dependencies | Complexity | Priority | Parallel Group |
|---|-----------|-------------|-----------|----------|----------------|
| 21 | `capture/monitor.py` — Enumerate screens/monitors | 1 | S | P0 | D |
| 22 | `capture/region_selector.py` — Interactive region picker UI | 8, 21 | L | P0 | D (after 21) |
| 23 | `capture/grabber.py` — mss frame capture → numpy array | 8 | M | P0 | D |
| 24 | `capture/frame_buffer.py` — Thread-safe frame queue | 1 | M | P0 | D |
| 25 | `capture/fps_controller.py` — Frame rate throttle (target ≥30) | 5 | S | P1 | D |
| 26 | `capture/thread.py` — Capture thread lifecycle manager | 23, 24, 25 | M | P0 | D (after 23–25) |

> **21, 23, 24, 25 can be developed in parallel. Then 22 and 26 follow.**

---

### Phase 4: OCR Pipeline

Depends on capture output (numpy frames) and feeds into parser.

| # | Component | Dependencies | Complexity | Priority | Parallel Group |
|---|-----------|-------------|-----------|----------|----------------|
| 27 | `ocr/preprocessor.py` — Grayscale conversion | None (numpy) | S | P0 | E |
| 28 | `ocr/threshold.py` — Adaptive binarization | 27 | M | P0 | E |
| 29 | `ocr/denoise.py` — Noise reduction filters | 27 | M | P1 | E |
| 30 | `ocr/roi.py` — Region-of-interest extraction | 8 | M | P0 | E |
| 31 | `ocr/engine.py` — Tesseract pytesseract wrapper | 1 | M | P0 | E |
| 32 | `ocr/confidence.py` — OCR confidence scoring/filtering | 31 | S | P1 | E (after 31) |
| 33 | `ocr/cache.py` — Frame-diff cache (skip unchanged) | 31 | M | P2 | E (after 31) |
| 34 | `ocr/pipeline.py` — Chain: preprocess→threshold→denoise→ROI→engine | 27–33 | L | P0 | E (after all) |

> **27, 30, 31 can start in parallel. 28, 29 follow 27. 32, 33 follow 31. 34 is last.**

---

### Phase 5: Overlay & Display

Depends on converter output (BBState). Independent of OCR internals.

| # | Component | Dependencies | Complexity | Priority | Parallel Group |
|---|-----------|-------------|-----------|----------|----------------|
| 35 | `overlay/window.py` — Transparent always-on-top window | 1 | L | P0 | F |
| 36 | `overlay/renderer.py` — Text rendering (OpenCV putText) | 7 | M | P0 | F |
| 37 | `overlay/positioning.py` — Map BB values to poker client coords | 8, 36 | M | P0 | F (after 36) |
| 38 | `overlay/colorizer.py` — Color-code by stack depth | 7, 13 | S | P2 | F |
| 39 | `overlay/loop.py` — Overlay refresh loop (sync with pipeline) | 35, 37 | M | P0 | F (after 35, 37) |

> **35 and 36 can be developed in parallel. 37, 38 follow. 39 is last.**

---

### Phase 6: Integration, CLI & Pipeline Orchestration

Wires everything together. Depends on all prior phases.

| # | Component | Dependencies | Complexity | Priority | Parallel Group |
|---|-----------|-------------|-----------|----------|----------------|
| 40 | `pipeline/orchestrator.py` — Main loop: capture→OCR→parse→convert→overlay | 26, 34, 19, 12, 39 | L | P0 | G |
| 41 | `pipeline/thread_pool.py` — Thread pool for pipeline stages | 26, 40 | M | P0 | G |
| 42 | `pipeline/queue.py` — Inter-stage thread-safe queues | 24 | M | P0 | G |
| 43 | `pipeline/recovery.py` — Error recovery, retry, graceful degradation | 1, 40 | M | P1 | G (after 40) |
| 44 | `main.py` — CLI argument parser (argparse) | 3, 40 | S | P0 | H |
| 45 | `cli/setup_wizard.py` — First-run setup (select region, verify OCR) | 22, 31, 44 | M | P1 | H (after 44) |
| 46 | `cli/status.py` — Live status dashboard (FPS, confidence, errors) | 5, 40 | M | P2 | H (after 44) |

> **40, 41, 42 can be developed together. 43 follows 40. CLI items (44–46) are sequential.**

---

## Critical Path

Three parallel branches converge at the orchestrator (#40). The longest branch determines the critical path.

```
Branch A (Capture):  8 → 23 → 26 ──────────────────╮
Branch B (OCR):      1 → 31 → 34 ──────────────────├──▶ 40 → 44
Branch C (Parser):   6 → 15 → 19 ──────────────────╯
Branch D (Overlay):  7 → 36 → 37 → 39 ─────────────╯
```

| Branch | Chain | Depth |
|--------|-------|-------|
| A (Capture) | 8 → 23 → 26 | 3 |
| B (OCR) | 1 → 31 → 34 | 3 |
| C (Parser) | 6 → 15 → 19 | 3 |
| D (Overlay) | 7 → 36 → 37 → 39 | 4 |

**Critical path:** 7 → 36 → 37 → 39 → 40 → 44 (depth 6, Branch D + integration)

All four branches must complete before #40 can start. Delays to **any** branch delay the project, but Branch D (Overlay) has the deepest chain. All branch roots (1, 6, 7, 8) are Phase 1 components with no dependencies — start them immediately.

---

## Parallel Development Map

```
Phase 1:  [A: all 10 components] ─────────────────────────────────────────►
Phase 2:  ·········[B: converter]──────►  [C: parser]──────────►
Phase 3:  ·········[D: capture]────────────────────►
Phase 4:  ·····················[E: OCR]────────────────────────►
Phase 5:  ·····················[F: overlay]─────────────────────►
Phase 6:  ··············································[G+H: integration]►
```

**Maximum parallelism opportunities:**
- Phase 1 is fully parallel (10 components, Group A)
- Phases 2+3 can run simultaneously (Groups B, C, D are independent)
- Phases 4+5 can run simultaneously (Groups E, F are independent)
- Phase 6 is sequential and depends on all prior phases

With 2 developers: one takes Capture+OCR path, other takes Parser+Converter+Overlay path, merge at Phase 6.

---

## Complexity Summary

| Complexity | Count | Components |
|-----------|-------|-----------|
| **S** | 20 | #1–13, 20, 21, 25, 27, 32, 38, 44 |
| **M** | 22 | #14–19, 23–24, 26, 28–31, 33, 36–37, 39, 41–43, 45–46 |
| **L** | 4 | #22, 34, 35, 40 |

## Already Complete

| # | Component | Status |
|---|-----------|--------|
| 6 | `models.py` — TableState | Done |
| 7 | `models.py` — BBState | Done |
