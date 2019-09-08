import pygame
import random
import neat
import time
import os
pygame.font.init()

CANVAS_WIDTH = 285      # Width of the canvas
CANVAS_HEIGHT = 510     # Height of the canvas

# BIRD_MOTIONS = []       # List to store the motions of our flappy bird

# for i, bird_img in zip(range(1, 4), os.listdir('images')):
#     bird_img = pygame.transform.scale2x(
#         pygame.image.load(os.path.join("images", f"bird{i}.png")))
#     BIRD_MOTIONS.append(bird_img)

# GROUND_IMG = pygame.transform.scale2x(
#     pygame.image.load(os.path.join("images", "base.png")))
# BG_IMG = pygame.transform.scale2x(
#     pygame.image.load(os.path.join("images", "bg.png")))
# PIPE_IMG = pygame.transform.scale2x(
#     pygame.image.load(os.path.join("images", "pipe.png")))

BIRD_MOTIONS2 = []
for i, bird_img in zip(range(1, 4), os.listdir('images')):
    bird_img = pygame.image.load(os.path.join("images", f"bird{i}.png"))
    BIRD_MOTIONS2.append(bird_img)

GROUND_IMG2 = pygame.image.load(os.path.join("images", "base.png"))
BG_IMG2 = pygame.image.load(os.path.join("images", "bg.png"))
PIPE_IMG2 = pygame.image.load(os.path.join("images", "pipe.png"))

STAT_FONT = pygame.font.SysFont("comicsans", 30)

class Bird:
    MOTIONS = BIRD_MOTIONS2
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
    GAP = 160
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        # self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(
            PIPE_IMG2, False, True)    # Flip pipe image upside down
        self.PIPE_BOTTOM = PIPE_IMG2

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(0, 300)
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
    VELOCITY = 5
    WIDTH = GROUND_IMG2.get_width()
    IMG = GROUND_IMG2

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, canvas):
        canvas.blit(self.IMG, (self.x1, self.y))
        canvas.blit(self.IMG, (self.x2, self.y))


# Main functions of game script
def draw_canvas(canvas, bird, pipes, ground, score):
    canvas.blit(BG_IMG2, (0, 0))
    
    # Draw the ground of our game
    ground.draw(canvas)
    
    # Draw pipes into our canvas
    for pipe in pipes:
        pipe.draw(canvas)
    
    text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    canvas.blit(text, (CANVAS_WIDTH - 10 - text.get_width(), 10))

    bird.draw(canvas)
    pygame.display.update()


def main():
    bird = Bird(50, 200)
    ground = Ground(450)
    pipes = [Pipe(700)]

    canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0   # Keep track of user's score
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        add_pipe = False
        rem_pipes = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # Check whether the pipe has lest the canvas
                rem_pipes.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(410))
        
        for rp in rem_pipes:
            pipes.remove(rp)

        if bird.y + bird.motion.get_height() >= 450:    # Bird hit the ground
            pass

        ground.move()
        draw_canvas(canvas, bird, pipes, ground, score)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
