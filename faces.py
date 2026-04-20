from face import Face
from eyes import fb_open, fb_semi_closed, fb_closed

LX = 20
RX = 84
Y = 20

neutral = Face([
    (fb_open,        fb_open,        LX, RX, Y, 3000),
    (fb_semi_closed, fb_semi_closed, LX, RX, Y,   40),
    (fb_closed,      fb_closed,      LX, RX, Y,   60),
    (fb_semi_closed, fb_semi_closed, LX, RX, Y,   40),
])
