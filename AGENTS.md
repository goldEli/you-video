# Repository Guidelines

## Project Structure & Module Organization
`main.py` orchestrates the pipeline and should stay lean—just CLI parsing and sequencing. Place reusable logic in `src/` (`downloader.py` for yt-dlp, `translator.py` for Whisper + translation, `compositor.py` for MoviePy). Keep generated media inside `downloads/` (or a user-provided dir) so source folders remain clean. Any helper scripts or docs live at the repo root beside `README.md` and `pyproject.toml`.

## Build, Test, and Development Commands
```bash
uv pip install -e .          # Install dependencies in editable mode for local hacking
uv run python main.py "<shorts-url>" --output-dir ./downloads  # Full pipeline run
uv run python test_imports.py # Quick check that moviepy, yt_dlp, etc. import cleanly
uv run python -m pytest      # Placeholder for future tests; keep new suites under tests/
```
Use `uv run` so the virtual environment matches `pyproject.toml`. The pipeline also requires FFmpeg on PATH—confirm with `ffmpeg -version` before debugging media errors.

## Coding Style & Naming Conventions
Stick to Python 3.13, 4-space indentation, and descriptive snake_case identifiers (`process_video_with_subtitles`). Favor short, typed functions with docstrings that explain side effects. Log absolute paths when reading/writing files so CLI users can trace artifacts. Run a formatter such as `ruff format` or `black` before opening a PR, even though it is not enforced yet.

## Testing Guidelines
Exercise downloader, translator, and compositor modules independently to avoid full pipeline waits. Use `pytest` fixtures to stub services (patch `yt_dlp.YoutubeDL`, `GoogleTranslator`) and store media samples under `tests/fixtures/`. Cover CLI flags like `--skip-download`, large Whisper models, and font failures. Every bug fix should ship with a regression test or at least an automated smoke case.

## Commit & Pull Request Guidelines
There is no formal history yet, so use short imperative subjects: `Add compositor font fallback`, `Fix downloader cookie flag`. Reference issues in the body (`Closes #12`) and list the commands you ran (`Test: uv run python test_imports.py`). PRs need a scenario summary, flag changes, and screenshots or console excerpts for UX-affecting work. Keep PRs focused—split media, translation, and CLI updates into separate reviews for easy tracing.
