import pygame
import time

pygame.mixer.init()
sound = pygame.mixer.Sound('/home/lick/Documents/Raspberry-Pi/sound_test.wav')
sound.play()
time.sleep(sound.get_length())
pygame.mixer.quit()
