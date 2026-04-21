import unittest

import weather
from weather import WeatherService, fetch_current, wttr_url


class FakeResponse:
    def __init__(self):
        self.closed = False

    def json(self):
        return {
            "current_condition": [
                {
                    "FeelsLikeC": "31",
                    "humidity": "66",
                    "temp_C": "29",
                    "weatherDesc": [{"value": "Partly cloudy"}],
                }
            ]
        }

    def close(self):
        self.closed = True


class FakeRequests:
    def __init__(self):
        self.response = FakeResponse()
        self.url = None

    def get(self, url):
        self.url = url
        return self.response


class FakeSocket:
    def __init__(self):
        self.timeouts = []

    def setdefaulttimeout(self, timeout):
        self.timeouts.append(timeout)


class FakeRawSocket:
    def __init__(self):
        self.timeout = None
        self.address = None
        self.request = b""
        self.closed = False
        self._chunks = [
            b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n",
            b'{"current_condition":[{"FeelsLikeC":"31","humidity":"66",',
            b'"temp_C":"29","weatherDesc":[{"value":"Partly cloudy"}]}]}',
            b"",
        ]

    def settimeout(self, timeout):
        self.timeout = timeout

    def connect(self, address):
        self.address = address

    def write(self, data):
        self.request += data

    def read(self, size):
        return self._chunks.pop(0)

    def close(self):
        self.closed = True


class FakeSocketModule:
    SOCK_STREAM = 1

    def __init__(self):
        self.sock = FakeRawSocket()
        self.lookup = None

    def getaddrinfo(self, host, port, family=0, socket_type=0):
        self.lookup = (host, port, family, socket_type)
        return [(None, None, None, None, ("1.2.3.4", 80))]

    def socket(self):
        return self.sock


class WeatherTest(unittest.TestCase):
    def test_wttr_url_uses_location_when_present(self):
        self.assertEqual(
            wttr_url("Santo Domingo"),
            "http://wttr.in/Santo+Domingo?format=j1",
        )

    def test_wttr_url_uses_ip_location_when_empty(self):
        self.assertEqual(wttr_url(""), "http://wttr.in/?format=j1")

    def test_fetch_current_parses_and_closes_response(self):
        requests = FakeRequests()

        data = fetch_current("Santo Domingo", requests)

        self.assertEqual(requests.url, "http://wttr.in/Santo+Domingo?format=j1")
        self.assertTrue(requests.response.closed)
        self.assertEqual(
            data,
            {
                "description": "Partly cloudy",
                "temp_c": "29",
                "feels_c": "31",
                "humidity": "66",
            },
        )

    def test_fetch_current_bounds_request_with_socket_timeout(self):
        requests = FakeRequests()
        socket = FakeSocket()

        fetch_current("Santo Domingo", requests, socket_module=socket, timeout_s=8)

        self.assertEqual(socket.timeouts, [8, None])

    def test_fetch_current_uses_socket_timeout_without_requests(self):
        socket = FakeSocketModule()
        original_requests = weather.requests
        weather.requests = None

        try:
            data = weather.fetch_current(
                "Santo Domingo",
                socket_module=socket,
                timeout_s=8,
            )
        finally:
            weather.requests = original_requests

        self.assertEqual(socket.lookup, ("wttr.in", 80, 0, socket.SOCK_STREAM))
        self.assertEqual(socket.sock.timeout, 8)
        self.assertEqual(socket.sock.address, ("1.2.3.4", 80))
        self.assertTrue(socket.sock.closed)
        self.assertIn(b"GET /Santo+Domingo?format=j1 HTTP/1.0", socket.sock.request)
        self.assertEqual(data["description"], "Partly cloudy")

    def test_weather_service_uses_retry_delay_after_error(self):
        service = WeatherService(refresh_ms=1000, retry_ms=100)

        service.set_error("WiFi failed", now=1000)

        self.assertFalse(service.should_refresh(1050))
        self.assertTrue(service.should_refresh(1101))


if __name__ == "__main__":
    unittest.main()
