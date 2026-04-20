# Repository Guidelines

## Project Structure & Module Organization

This is a small MicroPython project for rendering animated faces on an SSD1306 OLED display. Source files live at the repository root:

- `main.py` configures I2C pins, initializes the display, and runs face animations.
- `face.py` contains the reusable `Face` animation class.
- `faces.py` defines named animations and frame timing.
- `eyes.py` stores bitmap byte arrays and `framebuf.FrameBuffer` assets.
- `Makefile` wraps common `mpremote` device operations.

Keep new display assets near related bitmap data in `eyes.py`, and keep animation composition in `faces.py`.

## Build, Test, and Development Commands

- `uv sync`: install the Python tooling declared in `pyproject.toml`.
- `make help`: list available Makefile targets.
- `make run`: run `main.py` on the connected device without saving it.
- `make deploy`: copy all root-level `.py` files to the device filesystem.
- `make repl`: open a MicroPython REPL.
- `make ls`: list files on the device.
- `make reset`: soft-reset the device.

The default serial port is `/dev/cu.usbserial-0001`. Override it with `PORT=/dev/cu.your-device make run`.

## Coding Style & Naming Conventions

Use 4-space indentation and simple MicroPython-compatible Python. Prefer `snake_case` for variables, functions, and assets, and `UPPER_CASE` for shared constants like coordinates. Keep modules focused: rendering behavior belongs in `face.py`, animation sequences in `faces.py`, and raw bitmap/framebuffer data in `eyes.py`.

Do not suppress lint warnings only to get clean output. If image tooling is added, use ImageMagick 7 as `magick`, not deprecated `convert`.

## Testing Guidelines

No automated test suite is currently configured. When adding tests, place them under `tests/`, name files `test_*.py`, and expose `make test` plus `make coverage` if practical. For bug fixes, add a failing test or focused reproduction first, then prove the fix with a passing run.

For hardware changes, document the board, port, and command used, for example `PORT=/dev/cu.usbserial-0001 make run`.

## Commit & Pull Request Guidelines

Git history uses Conventional Commits, usually `feat(scope): summary` or `feat: summary`. Continue that pattern with concise, imperative summaries, such as `fix(faces): correct blink timing`.

Pull requests should include the behavior changed, validation performed, and any device-specific notes. Include photos or short clips when OLED output changes visually. Do not add co-author trailers to commits.
