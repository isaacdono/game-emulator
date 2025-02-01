# Snake Game

## Key Parts of the Code  

### Joystick Input Handling  
Reads joystick values and maps movement directions.  
```python
def read_joystick():
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()

    if y_val > 40000:
        return "UP"
    elif y_val < 20000:
        return "DOWN"
    elif x_val > 40000:
        return "RIGHT"
    elif x_val < 20000:
        return "LEFT"
```

### Game Rendering (OLED Display)  
Clears screen and draws snake, food, and borders.  
```python
def draw_game():
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)  # Draw border
    oled.pixel(food[0], food[1], 1)  # Draw food
    for segment in snake:
        oled.pixel(segment[0], segment[1], 1)  # Draw snake
    oled.show()
```

### Snake Movement
Moves the snake and detects collisions.  
```python
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
```

