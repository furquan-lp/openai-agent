# filename: snake_game.py

import pygame
import random

# Window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Snake and food size
BLOCK_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Function to display the score
def display_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    window.blit(text, [WINDOW_WIDTH - 140, 10])

# Function to draw the snake
def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(window, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

# Function to generate a new food location
def generate_food():
    food_x = random.randint(1, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
    food_y = random.randint(1, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
    return food_x, food_y

# Main game loop
def game_loop():
    game_over = False
    game_exit = False

    # Initial starting position for the snake
    snake_x = WINDOW_WIDTH // 2
    snake_y = WINDOW_HEIGHT // 2

    # Initial velocity of the snake
    velocity_x = 0
    velocity_y = 0

    # Snake body (initially just the head)
    snake_body = []
    snake_length = 1

    # Generate the initial food location
    food_x, food_y = generate_food()

    while not game_exit:
        while game_over:
            # Display game over message and score
            window.fill(BLACK)
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over", True, RED)
            window.blit(text, [(WINDOW_WIDTH // 2) - 120, (WINDOW_HEIGHT // 2) - 50])
            display_score(snake_length - 1)
            pygame.display.update()

            # Wait for user input to restart or quit the game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_r:
                        game_loop()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and velocity_y != BLOCK_SIZE:
                    velocity_x = 0
                    velocity_y = -BLOCK_SIZE
                if event.key == pygame.K_DOWN and velocity_y != -BLOCK_SIZE:
                    velocity_x = 0
                    velocity_y = BLOCK_SIZE
                if event.key == pygame.K_LEFT and velocity_x != BLOCK_SIZE:
                    velocity_x = -BLOCK_SIZE
                    velocity_y = 0
                if event.key == pygame.K_RIGHT and velocity_x != -BLOCK_SIZE:
                    velocity_x = BLOCK_SIZE
                    velocity_y = 0

        # Update snake position
        snake_x += velocity_x
        snake_y += velocity_y

        # Check for collision with window boundaries
        if snake_x >= WINDOW_WIDTH or snake_x < 0 or snake_y >= WINDOW_HEIGHT or snake_y < 0:
            game_over = True

        # Check for collision with own body
        snake_head = [snake_x, snake_y]
        if snake_head in snake_body[1:]:
            game_over = True

        # Check for collision with food
        if snake_x == food_x and snake_y == food_y:
            snake_length += 1
            food_x, food_y = generate_food()

        # Update snake body
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Update the game window
        window.fill(BLACK)
        draw_snake(snake_body)
        pygame.draw.rect(window, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        display_score(snake_length - 1)
        pygame.display.update()

        # Control the frame rate
        clock.tick(12)

    pygame.quit()

# Start the game loop
game_loop()