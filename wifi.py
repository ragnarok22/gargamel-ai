import time

try:
    import network
except ImportError:
    network = None

CONNECT_TIMEOUT_MS = 15000
POLL_INTERVAL_MS = 250


def _ticks_ms():
    if hasattr(time, "ticks_ms"):
        return time.ticks_ms()
    return int(time.monotonic() * 1000)


def _ticks_diff(now, then):
    if hasattr(time, "ticks_diff"):
        return time.ticks_diff(now, then)
    return now - then


def _sleep_ms(duration):
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(duration)
    else:
        time.sleep(duration / 1000)


def _notify(on_status, title, line_1="", line_2="", line_3=""):
    if on_status:
        on_status(title, line_1, line_2, line_3)


def connect_wifi(ssid, password, wlan=None, on_status=None, timeout_ms=CONNECT_TIMEOUT_MS):
    if wlan is None:
        if network is None:
            raise RuntimeError("network module missing")
        wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():
        return True

    if not ssid:
        _notify(on_status, "Weather", "Set config.py", "WIFI_SSID")
        return False

    try:
        wlan.active(True)
        wlan.connect(ssid, password)
    except OSError as error:
        print("WiFi error:", error)
        _notify(on_status, "Weather", "WiFi failed")
        return False

    _notify(on_status, "Weather", "WiFi...", ssid)

    started = _ticks_ms()
    while not wlan.isconnected():
        if _ticks_diff(_ticks_ms(), started) > timeout_ms:
            _notify(on_status, "Weather", "WiFi failed")
            return False
        _sleep_ms(POLL_INTERVAL_MS)

    return True
