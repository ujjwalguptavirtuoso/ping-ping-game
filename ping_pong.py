import pygame
import sys
import random
from ball import Ball
from paddle import Paddle

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
SPEED = 5
FONT_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

RED = (255, 0, 0)
DARK_BLUE = (0, 0, 128)

LIGHT_BLUE = (173, 216, 230)  # A shade of light blue
LIGHT_RED = (255, 182, 193)   # A shade of light red

# Screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

def random_color():
    """Generate a random color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def draw_home_screen():
    screen.fill(BLACK)
    one_player_text = font.render("1 Player", True, WHITE)
    two_player_text = font.render("2 Players", True, WHITE)

    one_player_rect = one_player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - FONT_SIZE))
    two_player_rect = two_player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + FONT_SIZE))

    pygame.draw.rect(screen, LIGHT_BLUE, one_player_rect.inflate(20, 10))
    pygame.draw.rect(screen, LIGHT_RED, two_player_rect.inflate(20, 10))

    screen.blit(one_player_text, one_player_rect)
    screen.blit(two_player_text, two_player_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if one_player_rect.collidepoint(event.pos):
                    return "1-player"
                if two_player_rect.collidepoint(event.pos):
                    return "2-player"

# Main game loop
def game_loop(mode):
    ball = Ball(640 // 2, 480 // 2, 5, 5)
    left_paddle = Paddle(0, 480 // 2 - PADDLE_HEIGHT // 2, RED)
    right_paddle = Paddle(640 - 15, 480 // 2 - PADDLE_HEIGHT // 2, DARK_BLUE)

    if mode == "1-player":
        right_paddle.dy = 0  # Reset the initial velocity for 2-player mode

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_paddle.dy = -SPEED
                if event.key == pygame.K_s:
                    left_paddle.dy = SPEED
                if event.key == pygame.K_UP:
                    right_paddle.dy = -SPEED
                if event.key == pygame.K_DOWN:
                    right_paddle.dy = SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    left_paddle.dy = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    right_paddle.dy = 0

        ball.move()

        # If 1-player mode, make the left paddle (computer) follow the ball
        if mode == "1-player":
            ai_move(left_paddle, ball)
        #     if ball.y > left_paddle.y + PADDLE_HEIGHT // 2:
        #         left_paddle.dy = SPEED
        #     elif ball.y < left_paddle.y + PADDLE_HEIGHT // 2:
        #         left_paddle.dy = -SPEED
        #     else:
        #         left_paddle.dy = 0
        # else:
        #     left_paddle.move()

        left_paddle.move()
        right_paddle.move()

        # Ball and paddle collision
        if ball.collides_with(left_paddle) or ball.collides_with(right_paddle):
            ball.dx = -ball.dx

        # Ball out of bounds
        if ball.x - BALL_RADIUS < 0 or ball.x + BALL_RADIUS > WIDTH:
            ball = Ball(WIDTH // 2, HEIGHT // 2, SPEED, SPEED)

        screen.fill(BLACK)
        ball.draw(screen)        # Pass screen as an argument
        left_paddle.draw(screen) # Pass screen as an argument
        right_paddle.draw(screen)

        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 2 - 1, 0, 2, HEIGHT))

        pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 40, 2)  # Small center circle

        pygame.display.flip()
        clock.tick(60)

def ai_move(paddle, ball):
    # Predictive Movement
    if ball.dx < 0:  # Only move when the ball is moving towards the paddle
        if ball.y > paddle.y + PADDLE_HEIGHT // 2:
            paddle.dy = SPEED
        elif ball.y < paddle.y + PADDLE_HEIGHT // 2:
            paddle.dy = -SPEED
        else:
            paddle.dy = 0

        # Introduce Random Errors
        error_chance = random.random()
        if error_chance < 0.05:  # 5% chance to make a "mistake"
            paddle.dy = -paddle.dy
    else:
        paddle.dy = 0  # Stay still if the ball is moving away


if __name__ == "__main__":
    mode = draw_home_screen()
    game_loop(mode)
