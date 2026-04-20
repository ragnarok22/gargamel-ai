import ssd1306
from machine import I2C, Pin

# 1. Inicializar el bus I2C en los pines que conectamos
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# 2. Inicializar la pantalla OLED (128x64 píxeles)
# Si te da error de tamaño, cambia 64 por 32, algunas pantallas de ese kit son 128x32
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 3. Dibujar la primera expresión
oled.fill(0)  # Pintar toda la pantalla de negro (borrar)
oled.text("^   ^", 44, 20)  # Dibujar ojos en la coordenada X:44, Y:20
oled.text("\___/", 44, 40)  # Dibujar boca en X:44, Y:40
oled.show()  # Enviar los datos del buffer a la pantalla física

print("Rostro inicializado con éxito.")
