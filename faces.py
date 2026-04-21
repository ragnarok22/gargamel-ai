from eyes import fb_angry, fb_closed, fb_open, fb_semi_closed
from face import Face

LX = 20
RX = 84
Y = 20


def _draw_line(oled, x0, y0, x1, y1):
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        oled.pixel(x0, y0, 1)
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _draw_polyline(oled, points):
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        _draw_line(oled, x0, y0, x1, y1)


def _smile(oled):
    _draw_polyline(oled, [(48, 49), (56, 54), (72, 54), (80, 49)])


def _smirk(oled):
    _draw_polyline(oled, [(48, 52), (62, 55), (80, 50)])


def _jagged_mouth(oled):
    _draw_polyline(
        oled,
        [(46, 50), (52, 57), (58, 50), (64, 57), (70, 50), (76, 57), (82, 50)],
    )


neutral = Face(
    [
        (fb_open, fb_open, LX, RX, Y, 3000),
        (fb_semi_closed, fb_semi_closed, LX, RX, Y, 40),
        (fb_closed, fb_closed, LX, RX, Y, 60),
        (fb_semi_closed, fb_semi_closed, LX, RX, Y, 40),
    ],
    mouth=_smile,
)

winky = Face(
    [
        (fb_open, fb_open, LX, RX, Y, 1000),
        (fb_open, fb_semi_closed, LX, RX, Y, 40),
        (fb_open, fb_closed, LX, RX, Y, 200),
        (fb_open, fb_semi_closed, LX, RX, Y, 40),
        (fb_open, fb_open, LX, RX, Y, 1000),
    ],
    mouth=_smirk,
)

scary = Face(
    [
        (fb_closed, fb_closed, LX, RX, Y, 400),  # start closed
        (fb_angry, fb_angry, LX, RX, Y, 1500),  # snap open angry
        (fb_closed, fb_angry, LX, RX, Y, 30),  # left eye twitch
        (fb_angry, fb_angry, LX, RX, Y, 60),
        (fb_angry, fb_closed, LX, RX, Y, 30),  # right eye twitch
        (fb_angry, fb_angry, LX, RX, Y, 1500),  # hold stare
    ],
    mouth=_jagged_mouth,
)
