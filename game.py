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
    GAP = 200 
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)    # Flip pipe image upside down
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, canvas):
        canvas.blit(self.PIPE_TOP, (self.x, self.top))
        canvas.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        # Offsets for collision
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        
        hasCollied = True if (top_point or bottom_point) else False
        return hasCollied
    
class Ground:
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

if __name__ == "__main__":
    main()