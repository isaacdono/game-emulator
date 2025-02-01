from machine import ADC, Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import time

# Initialize I2C (Adjust pins if necessary)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))

# Initialize OLED Display (128x64)
oled = SSD1306_I2C(128, 64, i2c)

# Initialize Joystick (ADC)
x_axis = ADC(Pin(27))  # GP27 -> X-axis
y_axis = ADC(Pin(26))  # GP26 -> Y-axis

# Test Direction
THRESHOLD = 3000  # Sensitivity range

while True:
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()

    if y_val > 60000:  # Up
        print("UP")
    elif y_val < 5000:  # Down
        print("DOWN")
    elif x_val > 60000:  # Right
        print("RIGHT")
    elif x_val < 5000:  # Left
        print("LEFT")

    time.sleep(0.5)  # Small delay