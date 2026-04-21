import time

try:
    import socket as default_socket
except ImportError:
    try:
        import usocket as default_socket
    except ImportError:
        default_socket = None

try:
    import urequests as requests
except ImportError:
    try:
        import requests
    except ImportError:
        requests = None

REFRESH_MS = 10 * 60 * 1000
RETRY_MS = 30 * 1000


def _ticks_diff(now, then):
    if hasattr(time, "ticks_diff"):
        return time.ticks_diff(now, then)
    return now - then


def wttr_url(location=""):
    location = location.strip().replace(" ", "+")
    if location:
        return "http://wttr.in/{}?format=j1".format(location)
    return "http://wttr.in/?format=j1"


def fetch_current(
    location="",
    requests_module=None,
    socket_module=default_socket,
    timeout_s=8,
):
    http = requests_module or requests
    if http is None:
        raise RuntimeError("requests missing")

    response = None
    timeout_was_set = False
    try:
        if timeout_s is not None and hasattr(socket_module, "setdefaulttimeout"):
            socket_module.setdefaulttimeout(timeout_s)
            timeout_was_set = True
        response = http.get(wttr_url(location))
        payload = response.json()
        current = payload["current_condition"][0]
        return {
            "description": current["weatherDesc"][0]["value"],
            "temp_c": current["temp_C"],
            "feels_c": current["FeelsLikeC"],
            "humidity": current["humidity"],
        }
    finally:
        if response:
            response.close()
        if timeout_was_set:
            socket_module.setdefaulttimeout(None)


class WeatherService:
    def __init__(
        self,
        location="",
        requests_module=None,
        socket_module=default_socket,
        timeout_s=8,
        refresh_ms=REFRESH_MS,
        retry_ms=RETRY_MS,
    ):
        self.location = location
        self.requests = requests_module
        self.socket = socket_module
        self.timeout_s = timeout_s
        self.refresh_ms = refresh_ms
        self.retry_ms = retry_ms
        self.last_attempt = None
        self.data = None
        self.error = None

    def should_refresh(self, now):
        if self.last_attempt is None:
            return True

        delay = self.retry_ms if self.error or self.data is None else self.refresh_ms
        return _ticks_diff(now, self.last_attempt) > delay

    def refresh(self, now):
        self.last_attempt = now
        self.data = fetch_current(
            self.location,
            self.requests,
            socket_module=self.socket,
            timeout_s=self.timeout_s,
        )
        self.error = None
        return self.data

    def set_error(self, error, now):
        self.last_attempt = now
        self.error = error
