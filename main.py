import time
import ssd1306
from machine import I2C, Pin
from faces import neutral, winky, scary

# --- DEFINITIONS OF PINS ---
# screen
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# presence
pir = Pin(27, Pin.IN)

# button
button = Pin(26, Pin.IN)


def face():
    print(pir.value())
    if pir.value():
        scary.animate(oled)
        winky.animate(oled)
    else:
        neutral.animate(oled)
        time.sleep_ms(200)


def weather():
    print("Weather")


def main():
    screens = ["face", "weather"]
    current_screen = 0

    while True:
        if button.value():
            current_screen = (current_screen + 1) % len(screens)

        if screens[current_screen] == "face":
            face()
        elif screens[current_screen] == "weather":
            weather()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
