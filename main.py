import time
import ssd1306
from machine import I2C, Pin
from faces import neutral, winky, scary

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

pir = Pin(27, Pin.IN)


def main():
    while True:
        print(pir.value())
        if pir.value():
            scary.animate(oled)
            winky.animate(oled)
        else:
            neutral.animate(oled)
            time.sleep_ms(200)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
