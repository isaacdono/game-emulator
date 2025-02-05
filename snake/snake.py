import random
import time
from machine import ADC, PWM, Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import neopixel

RED = (25, 0, 0)
GREEN = (0, 25, 0)
BLUE = (0, 0, 50)
YELLOW = (30, 30, 0)
MAGENTA = (30, 0, 30)
CYAN = (0, 30, 30)
WHITE = (25, 25, 25)
BLACK = (0, 0, 0)
NUM_LEDS = 25

class SnakeGame:
    def __init__(self):
        
        # Initialize LED Matrix
        self.np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

        # Initialize Display
        i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
        self.oled = SSD1306_I2C(128, 64, i2c)

        # Initialize Joystick
        self.x_axis = ADC(Pin(27))  # GP27 -> X-axis
        self.y_axis = ADC(Pin(26))  # GP26 -> Y-axis
    
        # Initialize Buttons
        self.button_a = Pin(5, Pin.IN, Pin.PULL_UP)
        self.button_b = Pin(6, Pin.IN, Pin.PULL_UP)

        # Initialize Left Buzzer (GP21)
        self.buzzer = PWM(Pin(21))
        self.buzzer.duty_u16(0)  # Start off

        # Snake Initial State
        self.snake = [(30, 30), (25, 30), (20, 30)]
        self.direction = "RIGHT"
        self.food = self.generate_food()
        self.score = 0
        self.running = True  # Game running flag

    def light_leds(self):
        colors = [
            BLACK, BLACK, GREEN, GREEN, GREEN, # Mirrored sequence
            BLACK, BLACK, GREEN, BLACK, BLACK, # Mirrored sequence
            GREEN, GREEN, GREEN, BLACK, BLACK, # Mirrored sequence
            BLACK, BLACK, BLACK, BLACK, GREEN,
            RED, BLACK, BLACK, BLACK, BLACK
        ]

        for i, color in enumerate(colors):
            self.np[i] = color

        self.np.write()

    def clear_all(self):
        for i in range(len(self.np)):
            self.np[i] = BLACK
        self.np.write()

    def generate_food(self):
        """Generates a new random food position."""

        while True:
            food_x = random.randint(1, 24) * 5  # Grid of 5px steps
            food_y = random.randint(1, 12) * 5  
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)
            
    def play_tone(self, frequency, duration):
        """Plays a tone on the buzzer (only for passive buzzers)."""

        self.buzzer.freq(frequency)
        self.buzzer.duty_u16(20000)  # Set duty cycle (<50%)
        time.sleep(duration)
        self.buzzer.duty_u16(0)  # Turn off buzzer

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
        if (head_x, head_y) in self.snake or head_x < 1 or head_x >= 127 or head_y < 1 or head_y >= 63:
            self.play_tone(200, 0.3)  # Game Over sound
            self.running = False
            return

        # Insert new head
        self.snake.insert(0, (head_x, head_y))

        # Check if food is eaten
        if (head_x, head_y) == self.food:
            self.score += 1
            self.food = self.generate_food()
            self.play_tone(660, 0.1)  # Food eaten sound
        else:
            self.snake.pop()  # Remove tail if no food eaten

    def draw_game(self):
        """Renders the snake and food on the OLED."""

        self.oled.fill(0)

        # Draw rectangle 
        self.oled.rect(0, 0, 128, 64, 1)  # (x, y, width, height, color)

        # Draw food
        self.oled.pixel(self.food[0], self.food[1], 1)

        # Draw snake
        for segment in self.snake:
            self.oled.pixel(segment[0], segment[1], 1)

        self.oled.show()
    
    def start_game(self):
        """Initial game screen."""

        self.oled.fill(0)

        # Text
        self.oled.text("SNAKE GAME", 25, 10)
        self.oled.text("Press A: Start", 10, 30)
        self.oled.text("Press B: Exit", 10, 40)
        self.oled.show()

        # Play or Close
        while True:
            if not self.button_a.value():
                self.running = True
                return
            elif not self.button_b.value():
                self.running = False
                return

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

    def game_loop(self):
        """Main game loop."""

        self.light_leds()
        while True:
            self.start_game() # Start or Exit options

            if not self.running: # Player closed the game
                self.oled.fill(0)
                self.oled.show()
                self.clear_all()
                return

            while self.running:
                self.read_joystick()
                self.move_snake()
                self.draw_game()
                time.sleep(0.25)  # Game speed
            
            self.game_over()


# Start the game
game = SnakeGame()
game.game_loop()
