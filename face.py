import time


class Face:
    def __init__(self, frames):
        # frames: list of (left_fb, right_fb, left_x, right_x, y, duration_ms)
        self._frames = frames

    def animate(self, oled):
        for left_fb, right_fb, lx, rx, y, duration in self._frames:
            oled.fill(0)
            oled.blit(left_fb, lx, y)
            oled.blit(right_fb, rx, y)
            oled.show()
            time.sleep_ms(duration)
