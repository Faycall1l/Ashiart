# Changelog

All notable changes to AshiArt are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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
