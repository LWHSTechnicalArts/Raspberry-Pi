#!/usr/bin/env python3
import pygame
import threading
import queue
from groq import Groq

# Initialize Groq client (get free key from https://console.groq.com/)
client = Groq(api_key="your-groq-api-key-here")

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Groq AI Chatbot")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
LIGHT_BLUE = (230, 240, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (76, 175, 80)

# Fonts
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 40)

# Chat settings
input_text = ""
chat_history = []
max_display_messages = 20
is_thinking = False

# Queue for AI responses
response_queue = queue.Queue()

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def get_ai_response(prompt):
    """Get response from Groq API"""
    global is_thinking
    is_thinking = True
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant running on a Raspberry Pi. Keep responses concise and friendly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        response_queue.put(bot_response)
        
    except Exception as e:
        response_queue.put(f"Error: {str(e)}")
    
    is_thinking = False

def send_message():
    """Send user message and get AI response"""
    global input_text
    
    if not input_text.strip():
        return
    
    # Add user message to chat
    chat_history.append(("You", input_text))
    user_message = input_text
    input_text = ""
    
    # Start AI response in separate thread
    thread = threading.Thread(target=get_ai_response, args=(user_message,))
    thread.daemon = True
    thread.start()

def draw_chat_window():
    """Draw the chat history"""
    chat_y = 80
    visible_messages = chat_history[-max_display_messages:]
    
    for sender, message in visible_messages:
        # Determine color based on sender
        if sender == "You":
            color = WHITE
            bg_color = BLUE
        else:
            color = BLACK
            bg_color = LIGHT_BLUE
        
        # Wrap text
        wrapped_lines = wrap_text(message, font, WIDTH - 100)
        
        for line in wrapped_lines:
            # Draw background bubble
            text_surface = font.render(line, True, color)
            padding = 10
            
            x_pos = 40 if sender == "You" else 20
            rect = pygame.Rect(
                x_pos,
                chat_y,
                text_surface.get_width() + padding * 2,
                text_surface.get_height() + padding
            )
            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            
            # Draw text
            screen.blit(text_surface, (rect.x + padding, chat_y + padding // 2))
            chat_y += text_surface.get_height() + padding + 5
        
        chat_y += 10  # Space between messages
        
        # Stop if we've gone off screen
        if chat_y > HEIGHT - 150:
            break

def draw_input_box():
    """Draw the input text box"""
    input_rect = pygame.Rect(20, HEIGHT - 70, WIDTH - 140, 50)
    pygame.draw.rect(screen, WHITE, input_rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, input_rect, 2, border_radius=10)
    
    # Draw input text
    display_text = input_text[-50:]  # Show last 50 chars
    text_surface = font.render(display_text, True, BLACK)
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 12))
    
    # Draw cursor
    if pygame.time.get_ticks() % 1000 < 500:
        cursor_x = input_rect.x + 10 + text_surface.get_width()
        pygame.draw.line(screen, BLACK, 
                        (cursor_x, input_rect.y + 10),
                        (cursor_x, input_rect.y + 40), 2)

def draw_send_button():
    """Draw the send button"""
    button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 70, 90, 50)
    button_color = GRAY if is_thinking else GREEN
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    
    text = "Send" if not is_thinking else "..."
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    return button_rect

# Main game loop
clock = pygame.time.Clock()
running = True

# Add welcome message
chat_history.append(("Bot", "Hello! I'm powered by Groq AI. Ask me anything!"))

while running:
    # Check for AI responses
    try:
        while not response_queue.empty():
            response = response_queue.get_nowait()
            chat_history.append(("Bot", response))
    except queue.Empty:
        pass
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not is_thinking:
                send_message()
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                # Add character to input
                if len(input_text) < 200:  # Limit input length
                    input_text += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            send_button = pygame.Rect(WIDTH - 110, HEIGHT - 70, 90, 50)
            if send_button.collidepoint(mouse_pos) and not is_thinking:
                send_message()
    
    # Drawing
    screen.fill(WHITE)
    
    # Draw title
    title_surface = title_font.render("⚡ Groq AI Chatbot", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))
    
    # Draw separator line
    pygame.draw.line(screen, GRAY, (20, 70), (WIDTH - 20, 70), 2)
    
    # Draw chat window
    draw_chat_window()
    
    # Draw input box
    draw_input_box()
    
    # Draw send button
    send_button_rect = draw_send_button()
    
    # Draw thinking indicator
    if is_thinking:
        thinking_text = font.render("Thinking...", True, DARK_GRAY)
        screen.blit(thinking_text, (20, HEIGHT - 100))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
