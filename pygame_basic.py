import pygame
import sys

# Initialize Pygame
pygame.init()

# Set display resolution
screen_width = 1024  # Change this to your screen's width
screen_height = 600  # Change this to your screen's height

# Create the screen surface
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set the text and font
font = pygame.font.Font(None, 100)
text = font.render("Hello, Yaks!", True, WHITE)

# Get the text rectangle and center it on the screen
text_rect = text.get_rect()
text_rect.center = (screen_width // 2, screen_height // 2)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(BLACK)  # Fill the screen with a black background
    screen.blit(text, text_rect)  # Blit the text onto the screen

    pygame.display.flip()

# Quit Pygame
pygame.quit()

# Exit the program
sys.exit()
