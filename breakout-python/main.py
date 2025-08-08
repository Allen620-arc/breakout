import pygame
import sys
import json
import os
import time

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

# Font
font = pygame.font.SysFont(None, 36)

# Leaderboard file
leaderboard_file = os.path.join(os.path.dirname(__file__), "leaderboard.json")

# Load leaderboard
def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_leaderboard(entries):
    with open(leaderboard_file, "w") as f:
        json.dump(entries, f)

# Input name
def get_player_name():
    name = ""
    input_active = True
    while input_active:
        screen.fill(BLACK)
        prompt = font.render("Enter your name (press Enter to confirm):", True, WHITE)
        name_surface = font.render(name, True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - 250, HEIGHT // 2 - 50))
        screen.blit(name_surface, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
    return name.strip()

# Leaderboard screen
def show_leaderboard_screen(leaderboard):
    showing = True
    while showing:
        screen.fill(BLACK)
        title = font.render("Top 10 Scores", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 100, 50))

        for i, entry in enumerate(leaderboard):
            text = font.render(f"#{i + 1}: {entry['name']} - {entry['score']}", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 150, 100 + i * 30))

        instructions = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(instructions, (WIDTH // 2 - 200, HEIGHT - 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    main()

# Reset bricks
def create_bricks():
    bricks = []
    brick_rows = 5
    brick_cols = 10
    brick_width = WIDTH // brick_cols
    brick_height = 30
    brick_padding = 5

    for row in range(brick_rows):
        for col in range(brick_cols):
            x = col * brick_width + brick_padding
            y = row * (brick_height + brick_padding) + brick_padding
            brick = pygame.Rect(x, y, brick_width - brick_padding * 2, brick_height)
            bricks.append((brick, BRICK_COLORS[row % len(BRICK_COLORS)]))
    return bricks

# Main game loop
def main():
    player_name = get_player_name()
    leaderboard = load_leaderboard()

    score = 0
    lives = 3
    final_score = 0

    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)
    paddle_speed = 8
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
    ball_speed = [5, -5]

    def reset_ball_and_paddle():
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        paddle.x = WIDTH // 2 - paddle.width // 2

    bricks = create_bricks()
    clock = pygame.time.Clock()
    running = True

    # Timer
    start_time = time.time()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # Ball movement
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] *= -1
        if ball.top <= 0:
            ball_speed[1] *= -1
        if ball.bottom >= HEIGHT:
            lives -= 1
            if lives <= 0:
                final_score = score * lives  # 0 if lost
                break
            else:
                reset_ball_and_paddle()
                pygame.time.delay(1000)

        if ball.colliderect(paddle):
            ball_speed[1] *= -1

        for i, (brick, color) in enumerate(bricks):
            if ball.colliderect(brick):
                ball_speed[1] *= -1
                del bricks[i]
                score += 100
                break

        if not bricks:
            win_text = font.render("You Win!", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - 70, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, RED, ball)

        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 120, 10))

        elapsed_now = round(time.time() - start_time, 2)
        timer_text = font.render(f"Time: {elapsed_now}s", True, WHITE)
        screen.blit(timer_text, (WIDTH // 2 - 50, 10))

        pygame.display.flip()

    # Finalize score after game ends
    elapsed_time = round(time.time() - start_time, 2)
    if final_score == 0:
        final_score = score * lives  # Can still be 0 if no bricks hit

    # Save score
    leaderboard.append({
        "name": player_name,
        "time": elapsed_time,
        "score": final_score
    })
    
    leaderboard.sort(key=lambda x: (x["time"], -x["score"]))
    leaderboard = leaderboard[:10]
    save_leaderboard(leaderboard)
    show_leaderboard_screen(leaderboard)

# Run game
if __name__ == "__main__":
    main()