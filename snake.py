import random
import time
from machine import ADC, Pin, SoftI2C
from ssd1306 import SSD1306_I2C

class SnakeGame:
    def __init__(self):
        # Initialize Display
        i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
        self.oled = SSD1306_I2C(128, 64, i2c)

        # Initialize Joystick
        self.x_axis = ADC(Pin(27))  # GP27 -> X-axis
        self.y_axis = ADC(Pin(26))  # GP26 -> Y-axis

        # Snake Initial State
        self.snake = [(30, 30), (25, 30), (20, 30)]
        self.direction = "RIGHT"
        self.food = self.generate_food()
        self.score = 0
        self.running = True  # Game running flag

    def generate_food(self):
        """Generates a new random food position."""

        while True:
            food_x = random.randint(0, 24) * 5  # Grid of 5px steps
            food_y = random.randint(0, 12) * 5  
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)

    def read_joystick(self):
        """Reads the joystick and updates the snake's direction."""

        x_val = self.x_axis.read_u16()
        y_val = self.y_axis.read_u16()

        if y_val > 40000 and self.direction != "DOWN":
            self.direction = "UP"
        elif y_val < 20000 and self.direction != "UP":
            self.direction = "DOWN"
        elif x_val > 40000 and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif x_val < 20000 and self.direction != "RIGHT":
            self.direction = "LEFT"

    def move_snake(self):
        """Moves the snake in the current direction."""

        head_x, head_y = self.snake[0]

        if self.direction == "UP":
            head_y -= 5
        elif self.direction == "DOWN":
            head_y += 5
        elif self.direction == "LEFT":
            head_x -= 5
        elif self.direction == "RIGHT":
            head_x += 5

        # Collision detection (walls or itself)
        if (head_x, head_y) in self.snake or head_x < 0 or head_x >= 128 or head_y < 0 or head_y >= 64:
            self.running = False
            return

        # Insert new head
        self.snake.insert(0, (head_x, head_y))

        # Check if food is eaten
        if (head_x, head_y) == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()  # Remove tail if no food eaten

    def draw_game(self):
        """Renders the snake and food on the OLED."""

        self.oled.fill(0)

        # Draw food
        self.oled.pixel(self.food[0], self.food[1], 1)

        # Draw snake
        for segment in self.snake:
            self.oled.pixel(segment[0], segment[1], 1)

        self.oled.show()
    
    def start_game(self):
        """Initial game screen."""

        self.oled.fill(0)
        self.oled.text("SNAKE GAME", 25, 30)
        self.oled.show()
        time.sleep(3)

    def game_over(self):
        """Handles game over screen and resets the game."""

        self.oled.fill(0)
        self.oled.text("GAME OVER!", 25, 20)
        self.oled.text(f"Score: {self.score}", 25, 40)
        self.oled.show()
        time.sleep(3)

        # Reset game state
        self.snake = [(30, 30), (25, 30), (20, 30)]
        self.direction = "RIGHT"
        self.food = self.generate_food()
        self.score = 0
        self.running = True

    def game_loop(self):
        """Main game loop."""
        
        while True:
            self.running = True  # Start a new round
            self.start_game()

            while self.running:
                self.read_joystick()
                self.move_snake()
                self.draw_game()
                time.sleep(0.25)  # Game speed

            self.game_over()


# Start the game
game = SnakeGame()
game.game_loop()
