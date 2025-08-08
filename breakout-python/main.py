import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

# Paddle settings
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)
paddle_speed = 8

# Ball settings
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [5, -5]

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1
    if ball.bottom >= HEIGHT:
        print("Game Over!")
        running = False

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    pygame.display.flip()

pygame.quit()
sys.exit()
