import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_radius = 30
ball_vel_x = 5
ball_vel_y = 5

# Clock for FPS control
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
    
    # Update ball position
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    
    # Bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_vel_x = -ball_vel_x
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= screen_height:
        ball_vel_y = -ball_vel_y
    
    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
