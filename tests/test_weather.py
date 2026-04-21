import unittest

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

    def test_weather_service_uses_retry_delay_after_error(self):
        service = WeatherService(refresh_ms=1000, retry_ms=100)

        service.set_error("WiFi failed", now=1000)

        self.assertFalse(service.should_refresh(1050))
        self.assertTrue(service.should_refresh(1101))


if __name__ == "__main__":
    unittest.main()
