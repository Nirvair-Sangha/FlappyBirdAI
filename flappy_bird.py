import pygame
import neat
import time
import os
import random
pygame.font.init() #gets font

WIN_WIDTH = 600
WIN_HEIGHT = 800

GEN = 0

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


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
        self.top = self.height - self.PIPE_TOP.get_height() #where the bottome of the top pipe will be
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top)) #draws top pipe
        win.blit(self.PIP_BOTTOM, (self.x, self.bottom)) #draws bottom pipe

    def collide(self, bird):
        bird_mask = bird.get_mask()#masks are what surround sprites to help determine collisions
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIP_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y)) #no decimals so round bird off
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) #if no collision returns none
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5 #need to have same velocity so they are moving in conjunction
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL # uses x1 and x2 to have moving background
        self.x2 -= self.VEL #x1 is on screen while x2 comes in moving left from right to replace x1
        #cycle repeats as x1 replaces x2 and x2 replaces x1 for the background
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0: #cycles back if off screen
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))#blit means to draw to window
    for pipe in pipes: #pipes is a list due to multiple pipes appearing on screen at once
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255)) # the color of font
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Generation: " + str(gen), 1, (255, 255, 255))  # the color of font
    win.blit(text, (10,10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = [] #create birds list for multiple birds

    for _,g in genomes: #tuple that has genome id which we ignore
        net  = neat.nn.FeedForwardNetwork.create(g, config)#makes the NN
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)


    base = Base(730)#bottom of screen
    pipes = [Pipe(600)] #spawns pipes closer
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) #shorthand of window
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)#make it much faster without rendering to screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0: #get first bird in x position it doesnt matter
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds): # every second the bird stays alive it gains a fitnes point
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),
                                       abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        #bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1 #bird incentive not to hit the pipe
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5 #go through pipes rather than making it farther in level
            pipes.append(Pipe(600)) #change this to smaller number for closer spawns

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0: #hit floor and lost
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt") #finds the absolute path
    run(config_path)

'''
Information to give NEAT algo:
Inputs: Bird y, Top pipe, Bottom pipe only need one pipe but both speed it up
Output: Jump or Dont jump
Activation Function(): TanH (more negative closer to -1 and more positive closer to 1) if val is greater than 0.5 then jump
Sigmoid is also a popular activation function ()
Population Size: 100 birds in each generation and keep breeeding best birds until only the best remain
The larger the population size the better to breed the best birds
Fitness Function: Determines which birds are better, whatever bird gets the furthest is the best
Max Generations: 30, if you dont get the perfect bird by 30, just stop and try again
'''




