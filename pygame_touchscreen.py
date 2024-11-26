import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Touchscreen Button Example")

# Colors
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Button properties
button_rect = pygame.Rect(412, 250, 200, 100)  # Centered on the screen
button_color = BLACK

# Fonts
font = pygame.font.Font(None, 36)
button_text = font.render("Touch Me!", True, WHITE)

# List to store hearts
hearts = []

# Function to draw a realistic heart
def draw_heart(surface, x, y, size):
    # Draw the top-left and top-right circles
    pygame.draw.circle(surface, RED, (x - size // 4, y), size // 4)
    pygame.draw.circle(surface, RED, (x + size // 4, y), size // 4)

    # Draw the bottom triangle
    points = [
        (x, y + size // 2),  # Bottom point
        (x - size // 2, y),  # Left point
        (x + size // 2, y),  # Right point
    ]
    pygame.draw.polygon(surface, RED, points)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit on Escape key
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the button was touched
            if button_rect.collidepoint(event.pos):
                print("Thank you for interacting!")
                # Add a new heart with random position and size
                heart_x = random.randint(50, SCREEN_WIDTH - 50)
                heart_y = random.randint(50, SCREEN_HEIGHT - 50)
                heart_size = random.randint(40, 80)  # Larger size for visibility
                hearts.append((heart_x, heart_y, heart_size))

    # Clear the screen with the pink background
    screen.fill(PINK)

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    # Draw all hearts
    for heart in hearts:
        draw_heart(screen, heart[0], heart[1], heart[2])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
