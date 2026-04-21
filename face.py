import time


class Face:
    def __init__(self, frames, mouth=None):
        # frames: list of (left_fb, right_fb, left_x, right_x, y, duration_ms)
        self._frames = frames
        self._mouth = mouth

    def _sleep_frame(self, duration, should_stop=None, poll_ms=50):
        if not should_stop:
            time.sleep_ms(duration)
            return True

        if poll_ms <= 0:
            poll_ms = duration

        remaining = duration
        while remaining > 0:
            if should_stop():
                return False

            sleep_for = poll_ms
            if sleep_for > remaining:
                sleep_for = remaining

            time.sleep_ms(sleep_for)
            remaining -= sleep_for
            if should_stop():
                return False

        return True

    def animate(self, oled, should_stop=None, poll_ms=50):
        for left_fb, right_fb, lx, rx, y, duration in self._frames:
            oled.fill(0)
            oled.blit(left_fb, lx, y)
            oled.blit(right_fb, rx, y)
            if self._mouth:
                self._mouth(oled)
            oled.show()
            if not self._sleep_frame(duration, should_stop, poll_ms):
                return False

        return True
