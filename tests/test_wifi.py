import importlib
import sys
import types
import unittest


class FakePin:
    IN = 0
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(self, *args):
        pass

    def value(self):
        return 0


class FakeI2C:
    def __init__(self, *args, **kwargs):
        pass


class FakeOled:
    def fill(self, color):
        pass

    def text(self, text, x, y):
        pass

    def show(self):
        pass


class FakeFace:
    def animate(self, oled):
        pass


class FailingWlan:
    def isconnected(self):
        return False

    def active(self, enabled):
        pass

    def connect(self, ssid, password):
        raise OSError("wifi radio unavailable")


def load_main():
    sys.modules.pop("main", None)
    sys.modules["machine"] = types.SimpleNamespace(Pin=FakePin, I2C=FakeI2C)
    sys.modules["network"] = types.SimpleNamespace(
        STA_IF=0,
        WLAN=lambda interface: FailingWlan(),
    )
    sys.modules["ssd1306"] = types.SimpleNamespace(
        SSD1306_I2C=lambda width, height, i2c: FakeOled(),
    )
    sys.modules["faces"] = types.SimpleNamespace(
        neutral=FakeFace(),
        winky=FakeFace(),
        scary=FakeFace(),
    )
    return importlib.import_module("main")


class ConnectWifiTest(unittest.TestCase):
    def test_connect_wifi_handles_connect_error(self):
        main = load_main()
        messages = []

        main.WIFI_SSID = "test-network"
        main.WIFI_PASSWORD = "test-password"
        main.wlan = FailingWlan()
        main.draw_message = lambda *parts: messages.append(parts)

        self.assertFalse(main.connect_wifi())
        self.assertIn(("Weather", "WiFi failed"), messages)


if __name__ == "__main__":
    unittest.main()
