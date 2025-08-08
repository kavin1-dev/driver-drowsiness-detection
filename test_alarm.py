import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load the alarm file
pygame.mixer.music.load(r"C:\Users\dravi\OneDrive\Desktop\opencv_project\script\alarm.mp3")

# Play it
pygame.mixer.music.play()

# Wait for it to finish playing (adjust duration if needed)
time.sleep(5)

# Stop the music (optional)
pygame.mixer.music.stop()
