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
BRICK_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255)]

# Score setup
score = 0
font = pygame.font.SysFont(None, 36)

# Paddle settings
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)
paddle_speed = 8

# Ball settings
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [5, -5]

# Clock
clock = pygame.time.Clock()

# Brick settings
brick_rows = 5
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 30
brick_padding = 5

bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        x = col * brick_width + brick_padding
        y = row * (brick_height + brick_padding) + brick_padding
        brick = pygame.Rect(x, y, brick_width - brick_padding * 2, brick_height)
        bricks.append((brick, BRICK_COLORS[row % len(BRICK_COLORS)]))  # include color with each brick

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

    # Ball collision with bricks
    for i, (brick, color) in enumerate(bricks):
        if ball.colliderect(brick):
            ball_speed[1] *= -1
            del bricks[i]
            score += 100
            break

    # Draw everything
    screen.fill(BLACK)

    # Draw paddle and ball
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)

    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
