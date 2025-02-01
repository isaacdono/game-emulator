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
    
# Generate random food position
def generate_food():
    while True:
        food_x = random.randint(0, 24) * 5  # Grid of 5px steps
        food_y = random.randint(0, 12) * 5  
        if (food_x, food_y) not in snake:  # Ensure food is not inside the snake
            return (food_x, food_y)

food = generate_food()
score = 0

# Max and Min values readings
# Y: 29415  X: 33064 -> Center
# Y: 65215  X: 35048 -> Up
# Y: 160  X: 35240 -> Down
# Y: 32407  X: 65199 -> Right
# Y: 21669  X: 160 -> Left

# Function to read joystick input
def read_joystick():
    global direction
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()

    if y_val > 40000 and direction != "DOWN":  # Up
        direction = "UP"
    elif y_val < 20000 and direction != "UP":  # Down
        direction = "DOWN"
    elif x_val > 40000 and direction != "LEFT":  # Right
        direction = "RIGHT"
    elif x_val < 20000 and direction != "RIGHT":  # Left
        direction = "LEFT"

# Function to move the snake
def move_snake():
    global snake, food, score

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

    # Check for collisions
    if (head_x, head_y) in snake or head_x < 0 or head_x >= 128 or head_y < 0 or head_y >= 64:
        snake[:] = [(30, 30), (25, 30), (20, 30)]  # Reset snake
        return False

    # Insert new head
    snake.insert(0, (head_x, head_y))

    # Check if snake eats food
    if (head_x, head_y) == food:
        score += 1
        food = generate_food()  # Generate new food
    else:
        snake.pop()  # Remove tail if no food eaten
    
    return True


# Function to draw the snake and food
def draw_game():
    oled.fill(0)  # Clear screen

    # Draw food
    oled.pixel(food[0], food[1], 1)

    # Draw snake
    for segment in snake:
        oled.pixel(segment[0], segment[1], 1)

    oled.show()  # Update display

# Main game logic
def start_game():
    oled.fill(0)
    oled.text("SNAKE GAME", 25, 30)
    oled.show()
    time.sleep(3)
    return

def load_game():
    while True:
        read_joystick()  # Read input
        if not move_snake():  # Move snake
            return
        draw_game()  # Update display
        time.sleep(0.25)  # Control game speed
        
def game_over():
    global score
    oled.fill(0)
    oled.text("GAME OVER!", 25, 20)
    oled.text("Score: " + str(score), 25, 40)
    score = 0
    oled.show()
    time.sleep(3)
    return

def game_control():
    while True:
        start_game()
        load_game()
        game_over()

game_control()
