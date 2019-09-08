import pygame
import random
import neat
import time
import os

CANVAS_WIDTH = 500      # Width of the canvas
CANVAS_HEIGHT = 700     # Height of the canvas
BIRD_MOTIONS = []       # List to store the motions of our flappy bird

for i, bird_img in zip(range(1, 4), os.listdir('images')):
    bird_img = pygame.transform.scale2x(
        pygame.image.load(os.path.join("images", f"bird{i}.png")))
    BIRD_MOTIONS.append(bird_img)

GROUND_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "bg.png")))
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "pipe.png")))

class Bird:
    MOTIONS = BIRD_MOTIONS
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0       # Default 0, since bird will be flying horizontally at the beginning
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.motion_count = 0
        self.motion = self.MOTIONS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2
        MAX_VEL = 16

        if displacement >= MAX_VEL:
            displacement = MAX_VEL

        if displacement < 0:
            displacement -= 2

        self.y += displacement      # Update bird's height
        if displacement < 0 or self.y < self.height + 50:   # Case when bird's flying up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:                                               # Case where bird's coming down
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, canvas):
        self.motion_count += 1

        '''
        Keeping the motions of our bird consistent as each frame goes by.
        '''
        if self.motion_count <= self.ANIMATION_TIME:
            self.motion = self.MOTIONS[0]
        elif self.motion_count <= self.ANIMATION_TIME * 2:
            self.motion = self.MOTIONS[1]
        elif self.motion_count <= self.ANIMATION_TIME * 3:
            self.motion = self.MOTIONS[2]
        elif self.motion_count <= self.ANIMATION_TIME * 4:
            self.motion = self.MOTIONS[1]
        elif self.motion_count == self.ANIMATION_TIME * 4 + 1:
            self.motion = self.MOTIONS[0]
            self.motion_count = 0

        if self.tilt <= -80:
            self.motion = self.MOTIONS[1]
            self.motion_count = self.ANIMATION_TIME * 2

        rotated_img = pygame.transform.rotate(self.motion, self.tilt)
        new_rect = rotated_img.get_rect(
            center=self.motion.get_rect(topleft=(self.x, self.y)).center)
        canvas.blit(rotated_img, new_rect.topleft)

    def get_mask(self):         # Class for handling collisions
        return pygame.mask.from_surface(self.motion)


class Pipe:
    pass


# Main functions of game script 
def draw_canvas(canvas, bird):
    canvas.blit(BG_IMG, (0, 0))
    bird.draw(canvas)
    pygame.display.update()


def main():
    bird = Bird(100, 200)
    canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        draw_canvas(canvas, bird)
    pygame.quit()
    quit()


main()
