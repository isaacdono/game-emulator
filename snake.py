from machine import ADC, Pin, SoftI2C
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

# ---------------------------------------------------------

# Initialize Joystick (ADC)
x_axis = ADC(Pin(26))  # GP26 -> X-axis
y_axis = ADC(Pin(27))  # GP27 -> Y-axis

while True:
    x_val = x_axis.read_u16()  # Read X (0-65535)
    y_val = y_axis.read_u16()  # Read Y (0-65535)

    print("X:", x_val, " Y:", y_val)  # Print values
    time.sleep(0.2)  # Small delay

