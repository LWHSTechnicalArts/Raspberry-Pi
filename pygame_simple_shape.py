import pygame
import sys

# Initialize Pygame
pygame.init()

# Set display dimensions
screen_width = 800
screen_height = 600

# Create the screen surface
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
PINK = (255, 182, 193)

# Define circle parameters
circle_radius = 100
circle_x = screen_width // 2
circle_y = screen_height // 2

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Draw a pink circle in the center
    pygame.draw.circle(screen, PINK, (circle_x, circle_y), circle_radius)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

# Exit the program
sys.exit()
