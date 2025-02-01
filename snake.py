from machine import Pin, I2C
import ssd1306
import time

# Initialize I2C (Adjust pins if necessary)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  

# Initialize OLED Display (128x64)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Test: Display "Snake Game"
oled.fill(0)  # Clear screen
oled.text("Snake Game", 10, 30)
oled.show()

time.sleep(2)
oled.fill(0)
oled.show()
