import sys
import unittest
from unittest.mock import MagicMock

# Mock MicroPython-specific modules before importing main
for _mod in ("framebuf", "machine", "ssd1306"):
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import main  # noqa: E402


class FakeFace:
    def __init__(self):
        self.received_should_stop = None

    def animate(self, oled, should_stop=None):
        self.received_should_stop = should_stop
        return False  # simulate interrupted animation


class MainFaceTest(unittest.TestCase):
    def setUp(self):
        self._orig_idle = main.IDLE_FACES
        self._orig_active = main.ACTIVE_FACES
        self._orig_pir = main.pir
        self._orig_oled = main.oled
        main.idle_face_index = 0
        main.active_face_index = 0
        main.next_screen_requested = False

    def tearDown(self):
        main.IDLE_FACES = self._orig_idle
        main.ACTIVE_FACES = self._orig_active
        main.pir = self._orig_pir
        main.oled = self._orig_oled

    def test_idle_animation_interrupted_when_movement_detected(self):
        fake_idle = FakeFace()
        fake_pir = MagicMock()
        fake_pir.value.return_value = 0  # no one present initially

        main.IDLE_FACES = (fake_idle,)
        main.ACTIVE_FACES = (MagicMock(),)
        main.pir = fake_pir
        main.oled = MagicMock()

        main.face()

        should_stop = fake_idle.received_should_stop
        self.assertIsNotNone(
            should_stop, "idle face must receive a should_stop callback"
        )

        fake_pir.value.return_value = 0
        self.assertFalse(should_stop())

        fake_pir.value.return_value = 1
        self.assertTrue(should_stop())


if __name__ == "__main__":
    unittest.main()
