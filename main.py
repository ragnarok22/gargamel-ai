import time

import ssd1306
from machine import I2C, Pin

from faces import happy, neutral, scary, sleepy, surprised, suspicious, winky
from weather import WeatherService
from wifi import connect_wifi

try:
    import config
except ImportError:
    config = None

WIFI_SSID = getattr(config, "WIFI_SSID", "")
WIFI_PASSWORD = getattr(config, "WIFI_PASSWORD", "")
WTTR_LOCATION = getattr(config, "WTTR_LOCATION", "")

# --- DEFINITIONS OF PINS ---
# screen
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# presence
pir = Pin(27, Pin.IN)

# built-in BOOT button
button = Pin(0, Pin.IN, Pin.PULL_UP)

weather_service = WeatherService(WTTR_LOCATION)
next_screen_requested = False
idle_face_index = 0
active_face_index = 0
IDLE_FACES = (neutral, sleepy, suspicious)
ACTIVE_FACES = (surprised, happy, winky, suspicious, scary)


def button_pressed():
    return not button.value()


def request_next_screen():
    global next_screen_requested

    if button_pressed():
        next_screen_requested = True
        return True
    return False


def face():
    global active_face_index, idle_face_index

    is_someone = pir.value() == 1
    print(f"{'There is someone' if is_someone else 'There is no one'}")

    if not is_someone:
        current_face = IDLE_FACES[idle_face_index]
        idle_face_index = (idle_face_index + 1) % len(IDLE_FACES)

        def _should_stop():
            return request_next_screen() or pir.value() == 1

        completed = current_face.animate(oled, should_stop=_should_stop)
        if completed:
            time.sleep_ms(200)

        is_someone = pir.value() == 1

    if is_someone:
        current_face = ACTIVE_FACES[active_face_index]
        active_face_index = (active_face_index + 1) % len(ACTIVE_FACES)
        current_face.animate(oled, should_stop=request_next_screen)


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


def show_weather():
    now = time.ticks_ms()
    if weather_service.should_refresh(now):
        if not connect_wifi(WIFI_SSID, WIFI_PASSWORD, on_status=draw_message):
            weather_service.set_error("WiFi failed", now)
        else:
            draw_message("Weather", "Fetching wttr")
            try:
                weather_service.refresh(now)
            except Exception as error:
                print("Weather error:", error)
                weather_service.set_error(error, now)

    oled.fill(0)
    oled.text("Weather", 0, 0)

    if weather_service.error:
        oled.text(str(weather_service.error)[:16], 0, 18)
        oled.text("Check WiFi/API", 0, 32)
    elif weather_service.data:
        oled.text(weather_service.data["description"][:16], 0, 14)
        oled.text("Temp: {} C".format(weather_service.data["temp_c"]), 0, 28)
        oled.text("Feels:{} C".format(weather_service.data["feels_c"]), 0, 40)
        oled.text("Hum:  {} %".format(weather_service.data["humidity"]), 0, 52)
    else:
        oled.text("No data", 0, 18)

    oled.show()
    time.sleep_ms(200)


def weather():
    show_weather()


def main():
    global next_screen_requested

    screens = ["face", "weather"]
    current_screen = 0
    button_was_pressed = False

    while True:
        button_is_pressed = button_pressed()
        print(f"Button: {button_is_pressed}")

        if next_screen_requested or (button_is_pressed and not button_was_pressed):
            current_screen = (current_screen + 1) % len(screens)
            next_screen_requested = False
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
