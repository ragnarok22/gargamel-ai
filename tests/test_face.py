import unittest

import face
from face import Face


class FakeTime:
    def __init__(self):
        self.sleeps = []

    def sleep_ms(self, duration):
        self.sleeps.append(duration)


class FakeOled:
    def __init__(self):
        self.shown = 0

    def fill(self, color):
        pass

    def blit(self, framebuffer, x, y):
        pass

    def show(self):
        self.shown += 1


class FaceTest(unittest.TestCase):
    def test_animation_can_be_interrupted_during_long_frame_delay(self):
        fake_time = FakeTime()
        original_time = face.time
        face.time = fake_time
        stop_checks = []

        def should_stop():
            stop_checks.append(True)
            return len(stop_checks) > 1

        try:
            completed = Face([(object(), object(), 0, 0, 0, 3000)]).animate(
                FakeOled(),
                should_stop=should_stop,
                poll_ms=50,
            )
        finally:
            face.time = original_time

        self.assertFalse(completed)
        self.assertEqual(fake_time.sleeps, [50])


if __name__ == "__main__":
    unittest.main()
