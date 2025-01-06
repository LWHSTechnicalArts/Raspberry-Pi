import pygame
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firestore-key.json")  # Replace with your JSON key file
firebase_admin.initialize_app(cred)
db = firestore.client()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Yes/No survey with reset")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Button dimensions
button_width = 120
button_height = 60
yes_button = pygame.Rect(50, 120, button_width, button_height)
no_button = pygame.Rect(230, 120, button_width, button_height)
reset_button = pygame.Rect(140, 250, button_width, button_height)

# Fonts
font = pygame.font.Font(None, 36)

# Initialize counts
yes_count = 0
no_count = 0

def send_to_firebase(choice):
    """Send Yes or No to Firestore and update counts."""
    global yes_count, no_count
    db.collection("responses").add({
        "response": choice,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print(f"Sent '{choice}' to Firebase!")
    # Update counts
    update_counts()

def update_counts():
    """Retrieve Yes and No counts from Firestore."""
    global yes_count, no_count
    yes_count = len(db.collection("responses").where("response", "==", "Yes").get())
    no_count = len(db.collection("responses").where("response", "==", "No").get())
    print(f"Yes: {yes_count}, No: {no_count}")

def reset_database():
    """Delete all entries from Firestore and reset counts."""
    docs = db.collection("responses").stream()
    for doc in docs:
        doc.reference.delete()
    global yes_count, no_count
    yes_count = 0
    no_count = 0
    print("Database reset!")

# Initial count update
update_counts()

# Main loop
running = True
while running:
    # Fill the screen with a white background
    screen.fill(WHITE)

    # Draw buttons
    pygame.draw.rect(screen, GREEN, yes_button)
    pygame.draw.rect(screen, RED, no_button)
    pygame.draw.rect(screen, ORANGE, reset_button)

    # Add text to buttons
    yes_text = font.render("YES", True, BLACK)
    no_text = font.render("NO", True, BLACK)
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(yes_text, (yes_button.x + 30, yes_button.y + 15))
    screen.blit(no_text, (no_button.x + 40, no_button.y + 15))
    screen.blit(reset_text, (reset_button.x + 30, reset_button.y + 15))

    # Display counts
    yes_count_text = font.render(f"Yes: {yes_count}", True, BLACK)
    no_count_text = font.render(f"No: {no_count}", True, BLACK)
    screen.blit(yes_count_text, (50, 50))
    screen.blit(no_count_text, (50, 90))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if yes_button.collidepoint(event.pos):
                send_to_firebase("Yes")
            elif no_button.collidepoint(event.pos):
                send_to_firebase("No")
            elif reset_button.collidepoint(event.pos):
                reset_database()

    # Update the display after all rendering
    pygame.display.flip()

pygame.quit()

