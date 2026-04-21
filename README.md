# Gargamel AI

MicroPython face animations for an SSD1306 OLED display. The project renders
simple eye expressions on a 128x64 screen using `framebuf` assets and a small
animation abstraction.

## Requirements

- A MicroPython-compatible board with I2C support
- SSD1306 OLED display wired to `scl=Pin(22)` and `sda=Pin(21)`
- [`uv`](https://docs.astral.sh/uv/) for Python tool management
- USB serial access to the board

Install the host-side tooling:

```sh
uv sync
```

## Running on a Device

The Makefile uses `mpremote` through `uv run`. By default it connects to
`/dev/cu.usbserial-0001`; override this with `PORT` when needed.

```sh
make help
make run
PORT=/dev/cu.your-device make run
```

Useful device commands:

```sh
make deploy  # copy all .py files to the board
make repl    # open a MicroPython REPL
make ls      # list files on the board
make reset   # soft-reset the board
```

## Weather Setup

The weather screen fetches current conditions from `wttr.in` over WiFi. Create a
local `config.py` from the example and fill in your network details:

```sh
cp config.example.py config.py
```

Set `WTTR_LOCATION` to a city, airport code, or coordinates. Leave it empty to
let `wttr.in` infer the location from the public IP address.

## Project Layout

- `main.py`: initializes I2C, creates the OLED display, and plays animations.
- `face.py`: defines the reusable `Face` class.
- `faces.py`: composes named expressions such as `neutral`, `winky`, and `scary`.
- `eyes.py`: stores eye bitmap byte arrays and `framebuf.FrameBuffer` objects.
- `Makefile`: wraps common `mpremote` workflows.

## Development Notes

Keep animation timing and expression sequencing in `faces.py`. Add or edit raw
bitmap assets in `eyes.py`, then expose them as framebuffer objects for reuse.

No automated test suite is configured yet. For behavior changes, prefer adding a
focused reproduction or test harness before changing implementation details, and
document the hardware command used to validate the result.
