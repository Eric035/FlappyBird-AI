import pygame
import random
import neat
import time
import os

CANVAS_WIDTH = 600      # Width of the canvas
CANVAS_HEIGHT = 800     # Height of the canvas
BIRD_MOTIONS = []       # List to store the motions of our flappy bird

for i, bird_img in zip(range(1, 4), os.listdir('images')):
    bird_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images", f"bird{i}.png")))
    BIRD_MOTIONS.append(bird_img)

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))


