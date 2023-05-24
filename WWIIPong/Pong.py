import pygame
import random

pygame.init()
WIDTH = 800
HEIGHT = 400
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, WINDOW_SIZE)
ball_img = pygame.image.load("Nuke.png")
paddle_left_img = pygame.image.load("AMERIMA.png")
paddle_right_img = pygame.image.load("JAPAN.png")
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
PADDLE_SPEED = 5
PADDLE_DISTANCE = 20
paddle_left = pygame.Rect(PADDLE_DISTANCE, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - PADDLE_DISTANCE - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
BALL_RADIUS = 20
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = BALL_SPEED_X * random.choice([-1, 1])
ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])
score_left = 0
score_right = 0
font = pygame.font.Font(None, 36)

def rotate_ball(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(ball.x, ball.y)).center)
    return rotated_image, new_rect

show_winner = False
winner_text = ""
restart_text = font.render("Press Enter to restart", True, (255, 255, 255))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and show_winner:
                show_winner = False
                score_left = 0
                score_right = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_left.y > 0:
        paddle_left.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle_left.y < HEIGHT - PADDLE_HEIGHT:
        paddle_left.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle_right.y > 0:
        paddle_right.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_right.y < HEIGHT - PADDLE_HEIGHT:
        paddle_right.y += PADDLE_SPEED
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.colliderect(paddle_left) or ball.colliderect(paddle_right):
        ball_speed_x *= -1
    if ball.y <= 0 or ball.y >= HEIGHT - BALL_RADIUS:
        ball_speed_y *= -1
    if ball.x < 0:
        score_right += 1
        if score_right == 5:
            show_winner = True
            winner_text = font.render("Player 2 Lost!", True, (255, 255, 255))
        else:
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= random.choice([-1, 1])
            ball_speed_y *= random.choice([-1, 1])
    if ball.x > WIDTH:
        score_left += 1
        if score_left == 5:
            show_winner = True
            winner_text = font.render("Player 1 Lost!", True, (255, 255, 255))
        else:
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= random.choice([-1, 1])
            ball_speed_y *= random.choice([-1, 1])
    angle = -pygame.math.Vector2(ball_speed_x, ball_speed_y).angle_to(pygame.math.Vector2(1, 0))
    rotated_ball_img, rotated_ball_rect = rotate_ball(ball_img, angle)
    screen.blit(background_img, (0, 0))
    screen.blit(paddle_left_img, paddle_left)
    screen.blit(paddle_right_img, paddle_right)
    screen.blit(rotated_ball_img, rotated_ball_rect)
    score_text = font.render(f"{score_left} : {score_right}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    if show_winner:
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + winner_text.get_height() // 2))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
