import pygame
import sys
import board
import adafruit_vl53l1x

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Distance Sensor Controlled Image")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# Initialize sensor
i2c = board.I2C()
vl53 = adafruit_vl53l1x.VL53L1X(i2c)
vl53.distance_mode = 1
vl53.timing_budget = 100
vl53.start_ranging()

# Load and scale the image (fixed size, no scaling during runtime)
try:
    ball_image = pygame.image.load("squirrel.png").convert_alpha()
    ball_image = pygame.transform.scale(ball_image, (300, 120)) 
except pygame.error as e:
    print(f"Error loading image: {e}")
    print("Make sure 'ball.png' exists in the same directory as your script")
    sys.exit()

# Get image dimensions
ball_rect = ball_image.get_rect()
ball_width = ball_rect.width
ball_height = ball_rect.height

# Ball properties
ball_x = screen_width // 2 - ball_width // 2  # Center horizontally
ball_y = screen_height - ball_height  # Start at bottom

# Distance mapping
min_distance = 1   # cm - closest distance (ball at bottom)
max_distance = 80  # cm - farthest distance (ball at top)

# Initialize distance variable
distance = 1

# Font for displaying distance
font = pygame.font.Font(None, 36)

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
    
    # Read distance from sensor
    if vl53.data_ready:
        sensor_distance = vl53.distance
        vl53.clear_interrupt()
        
        if sensor_distance is not None:
            distance = sensor_distance
            distance = max(min_distance, min(distance, max_distance))
            
            # Map to screen height - INVERTED
            normalized = (distance - min_distance) / (max_distance - min_distance)
            ball_y = int((1 - normalized) * (screen_height - ball_height))
    
    # Draw everything with WHITE background
    screen.fill(WHITE)
    
    # Draw the image
    screen.blit(ball_image, (ball_x, ball_y))
    
    # Draw distance text in BLACK
    distance_text = font.render(f"Distance: {distance:.1f} cm", True, BLACK)
    screen.blit(distance_text, (10, 10))
    
    # Draw reference lines
    # Bottom line (min distance)
    pygame.draw.line(screen, RED, (0, screen_height - 2), (screen_width, screen_height - 2), 2)
    bottom_text = font.render(f"Min: {min_distance} cm", True, BLACK)
    screen.blit(bottom_text, (10, screen_height - 40))
    
    # Top line (max distance)
    pygame.draw.line(screen, BLUE, (0, 10), (screen_width, 10), 2)
    top_text = font.render(f"Max: {max_distance} cm", True, BLACK)
    screen.blit(top_text, (10, 50))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Clean up
vl53.stop_ranging()
pygame.quit()
sys.exit()
