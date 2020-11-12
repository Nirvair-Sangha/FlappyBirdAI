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






