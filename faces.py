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


def _big_smile(oled):
    _draw_polyline(oled, [(44, 48), (52, 56), (64, 58), (76, 56), (84, 48)])


def _smirk(oled):
    _draw_polyline(oled, [(48, 52), (62, 55), (80, 50)])


def _flat_mouth(oled):
    _draw_line(oled, 50, 53, 78, 53)


def _open_mouth(oled):
    _draw_polyline(
        oled,
        [(58, 49), (70, 49), (76, 55), (70, 61), (58, 61), (52, 55), (58, 49)],
    )


def _sleepy_mouth(oled):
    _draw_polyline(oled, [(52, 53), (58, 55), (64, 53), (70, 55), (76, 53)])
    _draw_polyline(oled, [(88, 43), (96, 43), (88, 50), (96, 50)])
    _draw_polyline(oled, [(96, 32), (103, 32), (96, 38), (103, 38)])


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

happy = Face(
    [
        (fb_open, fb_open, LX, RX, Y, 600),
        (fb_semi_closed, fb_semi_closed, LX, RX, Y, 900),
        (fb_open, fb_open, LX, RX, Y, 600),
    ],
    mouth=_big_smile,
)

sleepy = Face(
    [
        (fb_semi_closed, fb_semi_closed, LX, RX, Y, 1200),
        (fb_closed, fb_closed, LX, RX, Y, 900),
        (fb_semi_closed, fb_closed, LX, RX, Y, 700),
    ],
    mouth=_sleepy_mouth,
)

surprised = Face(
    [
        (fb_closed, fb_closed, LX, RX, Y, 120),
        (fb_open, fb_open, LX, RX, Y, 1400),
        (fb_semi_closed, fb_semi_closed, LX, RX, Y, 120),
        (fb_open, fb_open, LX, RX, Y, 700),
    ],
    mouth=_open_mouth,
)

suspicious = Face(
    [
        (fb_semi_closed, fb_open, LX, RX, Y, 900),
        (fb_angry, fb_semi_closed, LX, RX, Y, 900),
        (fb_semi_closed, fb_open, LX, RX, Y, 700),
    ],
    mouth=_flat_mouth,
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
