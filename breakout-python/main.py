import pygame
import sys
import os

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

# Lives setup
lives = 3

# High score setup
high_score_file = os.path.join(os.path.dirname(__file__), "highscore.txt")

# Load existing high score
try:
    with open(high_score_file, "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

def reset_ball_and_paddle():
    global ball, paddle
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    paddle.x = WIDTH // 2 - paddle.width // 2

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
        lives -= 1
        if lives <= 0:
            print("Game Over!")
            running = False
        else:
            reset_ball_and_paddle()
            pygame.time.delay(1000)  # brief pause before resuming

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

    # Check win condition
    if not bricks:
        print("You Win!")
        win_text = font.render("You Win!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 70, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        running = False
    
    # Draw everything
    screen.fill(BLACK)

    # Draw paddle and ball
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)

    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw high score
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH // 2 - 80, 10))

    # Draw lives
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 120, 10))
    
    pygame.display.flip()

pygame.quit()

# Save high score if beaten
if score > high_score:
    try:
        with open(high_score_file, "w") as f:
            f.write(str(score))
    except Exception as e:
        print("Failed to save high score:", e)

sys.exit()
