# Changelog

All notable changes to AshiArt are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

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
