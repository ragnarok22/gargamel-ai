from face import Face
from eyes import fb_open, fb_semi_closed, fb_closed, fb_angry

LX = 20
RX = 84
Y = 20

neutral = Face([
    (fb_open,        fb_open,        LX, RX, Y, 3000),
    (fb_semi_closed, fb_semi_closed, LX, RX, Y,   40),
    (fb_closed,      fb_closed,      LX, RX, Y,   60),
    (fb_semi_closed, fb_semi_closed, LX, RX, Y,   40),
])

winky = Face([
    (fb_open, fb_open,        LX, RX, Y, 1000),
    (fb_open, fb_semi_closed, LX, RX, Y,   40),
    (fb_open, fb_closed,      LX, RX, Y,  200),
    (fb_open, fb_semi_closed, LX, RX, Y,   40),
    (fb_open, fb_open,        LX, RX, Y, 1000),
])

scary = Face([
    (fb_closed, fb_closed, LX, RX, Y,  400),  # start closed
    (fb_angry,  fb_angry,  LX, RX, Y, 1500),  # snap open angry
    (fb_closed, fb_angry,  LX, RX, Y,   30),  # left eye twitch
    (fb_angry,  fb_angry,  LX, RX, Y,   60),
    (fb_angry,  fb_closed, LX, RX, Y,   30),  # right eye twitch
    (fb_angry,  fb_angry,  LX, RX, Y, 1500),  # hold stare
])
