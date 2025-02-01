from machine import ADC, Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import random
import time

# Initialize I2C (Adjust pins if necessary)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))

# Initialize OLED Display (128x64)
oled = SSD1306_I2C(128, 64, i2c)

# Initialize Joystick (ADC)
x_axis = ADC(Pin(27))  # GP27 -> X-axis
y_axis = ADC(Pin(26))  # GP26 -> Y-axis

# Snake initial position and movement direction
snake = [(30, 30), (25, 30), (20, 30)]  # (x, y) coordinates
direction = "RIGHT"  # Default movement
    
# Function to read joystick input
def read_joystick():
    global direction
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()

    if y_val > 60000 and direction != "DOWN":  # Up
        direction = "UP"
    elif y_val < 5000 and direction != "UP":  # Down
        direction = "DOWN"
    elif x_val > 60000 and direction != "LEFT":  # Right
        direction = "RIGHT"
    elif x_val < 5000 and direction != "RIGHT":  # Left
        direction = "LEFT"

# Function to move the snake
def move_snake():
    global snake
    head_x, head_y = snake[0]  # Get current head position

    # Update head position based on direction
    if direction == "UP":
        head_y -= 5
    elif direction == "DOWN":
        head_y += 5
    elif direction == "LEFT":
        head_x -= 5
    elif direction == "RIGHT":
        head_x += 5

    # Insert new head and remove the tail (normal movement)
    snake.insert(0, (head_x, head_y))
    snake.pop()

# Function to draw the snake on the OLED
def draw_snake():
    oled.fill(0)  # Clear screen
    for segment in snake:
        oled.pixel(segment[0], segment[1], 1)  # Draw each segment
    oled.show()  # Update display

# Main game loop
while True:
    read_joystick()  # Read input
    move_snake()  # Move snake
    draw_snake()  # Update display
    time.sleep(0.2)  # Control game speed