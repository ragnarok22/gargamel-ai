import ssd1306
from machine import I2C, Pin
from faces import neutral

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    neutral.animate(oled)
