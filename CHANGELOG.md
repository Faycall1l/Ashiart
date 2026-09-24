# Changelog

All notable changes to AshiArt are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Image URLs as input: local paths and http(s) URLs work interchangeably
  in the CLI, `image_to_ascii`, and `generate_html` (stdlib download,
  no new dependency)
- Transparency compositing: RGBA, LA, and paletted images with alpha
  flatten onto white instead of decoding transparent pixels as black
- EXIF orientation: phone photos render upright via `exif_transpose`;
  load prep centralized in `prepare_image` (orient, then flatten)
- Input flexibility: `-` reads piped stdin bytes, `python -m ashiart`
  works, `NO_COLOR`/`TERM=dumb` disables ANSI color
- `--demo` renders a procedural calibration image with zero setup;
  `--open` opens `--html` output in a browser
- Default width follows the terminal size on ttys (100 elsewhere)
- Animation: GIF playback (`--play`, native frame durations, `--loop`,
  `--max-fps`), video files via optional `ashiart[video]` extra, live
  `--webcam` streaming, self-contained looping HTML export, terminal-fit
  playback sizing, `docs/images/demo.gif` sample
- Tonal controls: `--gamma` curve exponent and `--resample lanczos|box`
  downsampling choice; HTML `--bg black|white` page background
- Vectorized char mapping with 256-entry LUT semantics plus
  `examples/benchmark.py` throughput harness
- `ashiart/tonal.py`: NumPy CLAHE (`--clahe`) and Difference-of-Gaussians
  (`--dog SMALL LARGE AMPLIFY`) detail operators, dependency-free
- Quality gates: ruff check/format, mypy on `ashiart/`, pytest coverage
  floor at 80%, README python snippets executed as tests; dev tooling
  pinned in `requirements-dev.txt`; weekly Dependabot updates
- URL robustness: disk cache under `~/.cache/ashiart` (`--no-cache`
  bypasses), one retry on transient failures, fast fail on HTTP 4xx
- Docs engine: `scripts/gen_api.py` generating `docs/API.md` from
  docstrings (CI-checked), README performance table from
  `examples/benchmark.py`, `demo_outputs/index.html` gallery page
- README gallery with byte-verified per-mode outputs; download and
  last-commit badges

- Edge-aware rendering: Sobel orientation overlay (`- / | \`) on strong
  contours (`edges`, `--edges`, `--edge-threshold`, threshold 0.35);
  works in text, ANSI, and HTML paths (not braille)

### Changed

- Dense ramp reordered by measured glyph ink coverage (32 tonal
  inversions removed)
- CLI reference and README hero updated for edge overlay

### Removed

- `image_to_enhanced_ascii` and the baseline `generator.image_to_ascii`:
  a single `image_to_ascii()` entry point covers all modes and options
  (old names have no shim; update imports)

## [0.2.0] - 2026-09-20

### Added

- ANSI truecolor terminal output for `AsciiArtGenerator` (`color=True`)
  and `EnhancedAsciiArtGenerator` (`ansi=True`), including braille mode
  (block-averaged color)
- CLI: rendering modes (`--mode`), tuning flags (`--contrast`,
  `--brightness`, `--sharpness`, `--edge-enhance`, `--dithering`,
  `--invert`), `--color`, `--html`, `--font-size`, `--no-autocontrast`
- Automatic level stretching (`autocontrast`, on by default) in both
  generators, opt out via `autocontrast=False` / `--no-autocontrast`
- `docs/images/logo.svg`: header logo visualizing the brightness ramp
- `docs/images/puppy.jpg` and `docs/images/owl-face.jpg` demo inputs
- MIT `LICENSE` file
- This changelog

### Changed

- Rendering quality: LANCZOS resampling (was NEAREST), true 0.5 glyph
  aspect correction (was 0.4), space-terminated 12-level standard ramp,
  rounded (non-truncated) brightness mapping
- README rewritten: logo header, live sample output, CLI reference table,
  rendering-mode guide, project structure
- CI matrix: Python 3.8–3.11 (3.7 removed, EOL and unavailable on
  ubuntu-24.04 runners); actions refreshed to checkout@v4, setup-python@v5
- Packaging: sdist now ships `LICENSE`, docs assets, and examples README;
  project URL metadata added
- Minimum Python raised to 3.8 (`setup.py`, `setup.cfg`)

### Fixed

- CLI `--help` crash caused by unescaped `%` in `--chars` help text
- Curated `docs/images/` assets are now tracked (blanket image gitignore
  previously left every README image reference broken)
- Placeholder author email replaced in packaging metadata
