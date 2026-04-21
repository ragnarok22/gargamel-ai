import time
import network
import ssd1306
from machine import I2C, Pin
from faces import neutral, winky, scary

try:
    import config
except ImportError:
    config = None

try:
    import urequests as requests
except ImportError:
    try:
        import requests
    except ImportError:
        requests = None

WIFI_SSID = getattr(config, "WIFI_SSID", "")
WIFI_PASSWORD = getattr(config, "WIFI_PASSWORD", "")
WTTR_LOCATION = getattr(config, "WTTR_LOCATION", "")
WEATHER_REFRESH_MS = 10 * 60 * 1000

# --- DEFINITIONS OF PINS ---
# screen
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# presence
pir = Pin(27, Pin.IN)

# button
button = Pin(26, Pin.IN, Pin.PULL_DOWN)

wlan = network.WLAN(network.STA_IF)
last_weather_fetch = 0
weather_data = None
weather_error = None


def face():
    print(pir.value())
    if pir.value():
        scary.animate(oled)
        winky.animate(oled)
    else:
        neutral.animate(oled)
        time.sleep_ms(200)


def draw_message(title, line_1="", line_2="", line_3=""):
    oled.fill(0)
    oled.text(title[:16], 0, 0)
    if line_1:
        oled.text(line_1[:16], 0, 18)
    if line_2:
        oled.text(line_2[:16], 0, 32)
    if line_3:
        oled.text(line_3[:16], 0, 46)
    oled.show()


def connect_wifi():
    if wlan.isconnected():
        return True

    if not WIFI_SSID:
        draw_message("Weather", "Set config.py", "WIFI_SSID")
        return False

    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    draw_message("Weather", "WiFi...", WIFI_SSID)

    started = time.ticks_ms()
    while not wlan.isconnected():
        if time.ticks_diff(time.ticks_ms(), started) > 15000:
            draw_message("Weather", "WiFi failed")
            return False
        time.sleep_ms(250)

    return True


def wttr_url():
    location = WTTR_LOCATION.strip().replace(" ", "+")
    if location:
        return "http://wttr.in/{}?format=j1".format(location)
    return "http://wttr.in/?format=j1"


def fetch_weather():
    if requests is None:
        raise RuntimeError("requests missing")

    response = None
    try:
        response = requests.get(wttr_url())
        payload = response.json()
        current = payload["current_condition"][0]
        description = current["weatherDesc"][0]["value"]
        return {
            "description": description,
            "temp_c": current["temp_C"],
            "feels_c": current["FeelsLikeC"],
            "humidity": current["humidity"],
        }
    finally:
        if response:
            response.close()


def weather():
    global last_weather_fetch, weather_data, weather_error

    now = time.ticks_ms()
    should_fetch = (
        weather_data is None
        or time.ticks_diff(now, last_weather_fetch) > WEATHER_REFRESH_MS
    )

    if should_fetch:
        last_weather_fetch = now
        if not connect_wifi():
            time.sleep_ms(500)
            return

        draw_message("Weather", "Fetching wttr")
        try:
            weather_data = fetch_weather()
            weather_error = None
        except Exception as error:
            weather_error = error

    oled.fill(0)
    oled.text("Weather", 0, 0)

    if weather_error:
        oled.text("Fetch error", 0, 18)
        oled.text("Check WiFi/API", 0, 32)
        print("Weather error:", weather_error)
    elif weather_data:
        oled.text(weather_data["description"][:16], 0, 14)
        oled.text("Temp: {} C".format(weather_data["temp_c"]), 0, 28)
        oled.text("Feels:{} C".format(weather_data["feels_c"]), 0, 40)
        oled.text("Hum:  {} %".format(weather_data["humidity"]), 0, 52)
    else:
        oled.text("No data", 0, 18)

    oled.show()
    time.sleep_ms(200)


def main():
    screens = ["face", "weather"]
    current_screen = 0
    button_was_pressed = False

    while True:
        button_is_pressed = button.value()
        if button_is_pressed and not button_was_pressed:
            current_screen = (current_screen + 1) % len(screens)
            time.sleep_ms(200)
        button_was_pressed = button_is_pressed

        if screens[current_screen] == "face":
            face()
        elif screens[current_screen] == "weather":
            weather()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
