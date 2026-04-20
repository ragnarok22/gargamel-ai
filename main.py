import time

from eyes import draw_eyes, fb_open, fb_semi_closed, fb_closed
import ssd1306
from machine import I2C, Pin

# --- SCREEN CONFIGURATION ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# If you encounter a size error, change 64 to 32, as some screens in this kit are 128x32
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


def draw(expresssion):
    oled.fill(0)  # clean buffer
    if expresssion == "happy":
        oled.text("^   ^", 44, 20)
        oled.text("\\___/", 44, 40)
    elif expresssion == "fear":
        oled.text("o   o", 44, 20)
        oled.text(" ~~~ ", 44, 40)
    elif expresssion == "gretty":
        oled.text(">   <", 44, 20)
        oled.text("HOLA!", 44, 40)
    else:
        oled.text("-   -", 44, 20)
        oled.text(" ... ", 44, 40)

    oled.show()  # Send to the screen


emotions = ["happy", "gretty", "idle", "fear"]

index = 0

print("Initiating rotation of faces (1 each 5 seconds)...")

while True:
    draw_eyes(oled, fb_open)
    time.sleep(3)

    draw_eyes(oled, fb_semi_closed)
    time.sleep_ms(40)

    draw_eyes(oled, fb_closed)
    time.sleep_ms(60)

    draw_eyes(oled, fb_semi_closed)
    time.sleep_ms(40)
