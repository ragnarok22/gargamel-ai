import unittest

from wifi import connect_wifi


class FailingWlan:
    def isconnected(self):
        return False

    def active(self, enabled):
        pass

    def connect(self, ssid, password):
        raise OSError("wifi radio unavailable")


class ConnectedWlan:
    def isconnected(self):
        return True

    def active(self, enabled):
        raise AssertionError("active should not be called when already connected")

    def connect(self, ssid, password):
        raise AssertionError("connect should not be called when already connected")


class ConnectWifiTest(unittest.TestCase):
    def test_handles_connect_error(self):
        messages = []

        connected = connect_wifi(
            "test-network",
            "test-password",
            wlan=FailingWlan(),
            on_status=lambda *parts: messages.append(parts),
        )

        self.assertFalse(connected)
        self.assertIn(("Weather", "WiFi failed", "", ""), messages)

    def test_returns_true_when_already_connected(self):
        self.assertTrue(connect_wifi("", "", wlan=ConnectedWlan()))

    def test_missing_ssid_shows_config_message(self):
        messages = []

        connected = connect_wifi(
            "",
            "",
            wlan=FailingWlan(),
            on_status=lambda *parts: messages.append(parts),
        )

        self.assertFalse(connected)
        self.assertIn(("Weather", "Set config.py", "WIFI_SSID", ""), messages)


if __name__ == "__main__":
    unittest.main()
