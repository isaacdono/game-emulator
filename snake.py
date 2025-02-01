from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import time

# Initialize I2C (Adjust pins if necessary)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))

# Initialize OLED Display (128x64)
oled = SSD1306_I2C(128, 64, i2c)

# Test: Display "Snake Game"
oled.fill(0)  # Clear screen
oled.text("Snake Game", 10, 30)
oled.show()

time.sleep(2)
oled.fill(0)
oled.show()
