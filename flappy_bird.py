import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # how much the bird tilts
    ROT_VEL = 20 # how much the bird rotates every frame
    ANIMATION_TIME = 5 # how long to show each bird animation, speed of flapping

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0 # bird is flat til it starts moving
        self.tick_count = 0 #physics of bird
        self.vel = 0 #0 because its not moving
        self.height = self.y
        self.img_count = 0 # what image we showing
        self.img = self.IMGS[0] #refers to the first bird img which is stationary looking

    def jump(self):
        self.vel = -10.5 #gravity
        self.tick_count = 0 #keeps track of when we last jumped
        self.height = self.y

    def move(self):
        self.tick_count +=1 # how many times moved since last jump

        d = self.vel*self.tick_count + 1.5*self.tick_count**2 #displacement equation from physics
        #tick count is time while vel is velocity

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2 #when moving upwards, move up a little more

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1 # how many times does the while loop run
        #check what image to show based on image count
        if self.img_count < self.ANIMATION_TIME: #try to make more efficient
            self.img = self.IMGS[0] #if less than 5 play first animation
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]# if less than 10 play second animation
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]# if less than 15 show last animation
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1] #not flapping its wings when falling
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200 #gap between pipes
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0 # where top pipe is
        self.bottom = 0 # where bottom pipe is
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) #inverted pipe (Coming from ceiling_
        self.PIP_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIP_TOP.get_height() #where the bottome of the top pipe will be
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top)) #draws top pipe
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom)) #draws bottom pipe

    def collide(self, bird, win):



def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))#blit means to draw to window
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200,200) #create bird object
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) #shorthand of window
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(win, bird)

    pygame.quit()
    quit()

main()






