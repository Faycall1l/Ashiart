# Contributing to AshiArt

Bug reports, small fixes, and well-scoped features are welcome.
Open an issue to discuss anything beyond a typo before writing code.

## Scope

In scope: converters, rendering modes, tonal operators, input sources,
output formats, CLI ergonomics, tests, docs, packaging.

Out of scope: GUI applications, hosted services, new hard dependencies
for the core package (video and similar stay behind extras).

## Setup

```bash
git clone https://github.com/Faycall1l/Ashiart.git
cd Ashiart
pip install -e .
pip install pytest
```

## Rules

1. One behavior change per pull request; rebase onto `main` first.
2. Cover new behavior with tests. Run the suite before pushing:

   ```bash
   pytest
   ```

3. Keep the public API to two entry points: `image_to_ascii` for text
   (every mode and option lives there) and `image_to_html_ascii` for
   HTML. Do not add overlapping convenience functions; extend the
   existing signatures instead.
4. Docstrings follow PEP 257 with Google-style `Args`/`Returns`
   sections: describe semantics and contracts, never narrate the code.
   Inline comments explain *why* something non-obvious is needed, and
   only that.
5. README claims must be verifiable: exact level counts, real command
   output pasted byte-for-byte, working copy-paste commands. Sample
   ASCII blocks in docs are checked against fresh renders.
6. Update `CHANGELOG.md` under `[Unreleased]` (Added / Changed /
   Fixed / Removed) and the relevant README tables.

## Translations

`README.md` (English) is the source of truth. Translated siblings use
BCP 47 suffixes: `README.fr.md`, `README.de.md`. Rules:

- Translate prose only. Commands, code blocks, ASCII art, option names,
  badges, and links stay byte-identical to the English file.
- Mirror the section structure one-to-one; keep the language banner at
  the top pointing back to `README.md`.
- Add the language link line to the English README header.
- A translation PR should cover the whole file; partial translations
  are rejected. If the English README changes later, translators are
  expected to follow up.

## Pull request process

1. Fork, branch from `main` (`feat/...`, `fix/...`, `docs/...`).
2. Green `pytest` locally; CI must stay green.
3. Describe the problem, the approach, and how you verified it
   (commands run, outputs compared). Link any issue.
4. A maintainer merges; delete the branch afterwards.
