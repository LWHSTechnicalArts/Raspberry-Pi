import pygame
import sys
import board
import adafruit_vl53l1x

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Distance Sensor Controlled Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# Initialize VL53L1X sensor
i2c = board.I2C()
vl53 = adafruit_vl53l1x.VL53L1X(i2c)
vl53.distance_mode = 1  # Short distance mode
vl53.timing_budget = 100
vl53.start_ranging()

# Ball properties - Define ball_radius FIRST
ball_radius = 30
ball_x = screen_width // 2
ball_y = screen_height - ball_radius  # Start at bottom
ball_color = GREEN

# Distance mapping (adjust these based on your sensor range)
min_distance = 1   # cm - closest distance (ball at bottom)
max_distance = 80  # cm - farthest distance (ball at top)

# Initialize distance variable
distance = 1  # Default starting distance (bottom)

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
        
        # Check if distance is valid (not None)
        if sensor_distance is not None:
            distance = sensor_distance
            
            # Clamp distance to our range
            distance = max(min_distance, min(distance, max_distance))
            
            # Map to screen height - INVERTED
            # Low distance = high y value (bottom of screen)
            # High distance = low y value (top of screen)
            normalized = (distance - min_distance) / (max_distance - min_distance)
            ball_y = int((1 - normalized) * (screen_height - 2 * ball_radius)) + ball_radius
            
            # Change ball color based on distance
            if distance < 50:
                ball_color = RED
            elif distance < 100:
                ball_color = GREEN
            else:
                ball_color = BLUE
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw ball
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
    
    # Draw distance text
    distance_text = font.render(f"Distance: {distance:.1f} cm", True, WHITE)
    screen.blit(distance_text, (10, 10))
    
    # Draw reference lines
    # Bottom line (min distance)
    pygame.draw.line(screen, RED, (0, screen_height - ball_radius), (screen_width, screen_height - ball_radius), 2)
    bottom_text = font.render(f"Min: {min_distance} cm", True, RED)
    screen.blit(bottom_text, (10, screen_height - 40))
    
    # Top line (max distance)
    pygame.draw.line(screen, BLUE, (0, ball_radius), (screen_width, ball_radius), 2)
    top_text = font.render(f"Max: {max_distance} cm", True, BLUE)
    screen.blit(top_text, (10, ball_radius + 10))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Clean up
vl53.stop_ranging()
pygame.quit()
sys.exit()
