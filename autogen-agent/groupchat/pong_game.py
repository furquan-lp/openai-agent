# filename: pong_game.py
import pygame

# Initialize the game
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game variables
paddle_width, paddle_height = 10, 60
paddle_velocity = 5

player1_position = (screen_height - paddle_height) // 2
player2_position = (screen_height - paddle_height) // 2
ball_position = [screen_width // 2, screen_height // 2]
ball_velocity = [3, 3]

# Set up the player scores
player1_score = 0
player2_score = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_position > 0:
        player1_position -= paddle_velocity
    if keys[pygame.K_s] and player1_position < screen_height - paddle_height:
        player1_position += paddle_velocity
    if keys[pygame.K_UP] and player2_position > 0:
        player2_position -= paddle_velocity
    if keys[pygame.K_DOWN] and player2_position < screen_height - paddle_height:
        player2_position += paddle_velocity

    # Move the ball
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]

    # Detect collision with the paddles
    if ball_position[0] <= paddle_width and player1_position <= ball_position[1] <= player1_position + paddle_height:
        ball_velocity[0] = -ball_velocity[0]
    elif ball_position[0] >= screen_width - paddle_width and player2_position <= ball_position[1] <= player2_position + paddle_height:
        ball_velocity[0] = -ball_velocity[0]

    # Detect collision with the top and bottom walls
    if ball_position[1] <= 0 or ball_position[1] >= screen_height:
        ball_velocity[1] = -ball_velocity[1]

    # Update the player scores
    if ball_position[0] <= paddle_width:
        player2_score += 1
        ball_position = [screen_width // 2, screen_height // 2]
    elif ball_position[0] >= screen_width - paddle_width:
        player1_score += 1
        ball_position = [screen_width // 2, screen_height // 2]

    # Clear the screen
    screen.fill(BLACK)

    # Draw the paddles
    pygame.draw.rect(screen, WHITE, pygame.Rect(0, player1_position, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, pygame.Rect(screen_width - paddle_width, player2_position, paddle_width, paddle_height))

    # Draw the ball
    pygame.draw.circle(screen, WHITE, ball_position, 10)

    # Draw the player scores
    font = pygame.font.Font(None, 36)
    player1_score_text = font.render(str(player1_score), True, WHITE)
    player2_score_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_score_text, (screen_width // 4, 10))
    screen.blit(player2_score_text, (3 * (screen_width // 4), 10))

    # Update the display
    pygame.display.flip()

    # Set the game clock
    clock.tick(60)

# Quit the game
pygame.quit()