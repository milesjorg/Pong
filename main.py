import pygame, sys
from pygame.locals import *
import random
from random import randint
#Initialize game
pygame.init()

#Define FPS
FPS = 60
FramesPerSec = pygame.time.Clock()

#Default colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Themes
class Theme:
    def classic(self):
        pass
    def tennis(self):
        pass
    def pokemon(self):
        pass
    def wireframe(self):
        pass
    def dvd(self):
        pass

#Creating paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y > screen_size[1]:
            self.rect.y = screen_size[1]

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y < 0:
            self.rect.y = 0

#Create ball class
class ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        x = randint(4,8)
        y = randint(-8, 8)
        self.velocity = [x, y]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

#Creating game window
screen_size = (800, 800)
DISPLAYSURF = pygame.display.set_mode(screen_size)
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("P O N G")

#Create instance of player Paddle
PaddlePlayer = Paddle(WHITE, 10, 100)
PaddlePlayer.rect.x = 20
PaddlePlayer.rect.y = (screen_size[1]//2) - 50

#Create instance of player Paddle
PaddleAI = Paddle(WHITE, 10, 100)
PaddleAI.rect.x = screen_size[0] - 30
PaddleAI.rect.y = (screen_size[1]//2) - 50

#Create instance of ball sprite
Ball = ball(WHITE, 10, 10)
Ball.rect.x = screen_size[0]//2
Ball.rect.y = screen_size[1]//2

#Create list of all sprites (player and AI paddles and ball)
all_sprites = pygame.sprite.Group()

#Add player and AI sprite to sprites list
all_sprites.add(PaddlePlayer)
all_sprites.add(PaddleAI)
all_sprites.add(Ball)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    #Check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        PaddlePlayer.moveUp(screen_size[1]//100)
    if keys[pygame.K_DOWN]:
        PaddlePlayer.moveDown(screen_size[1]//100)

    all_sprites.update()

    #Check if ball should bounce
    if Ball.rect.y >= screen_size[1]//8 - 10:
        Ball.velocity[1] = -Ball.velocity[1]
    if Ball.rect.y <= 0:
        Ball.velocity[1] = -Ball.velocity[1]

    #Call bounce method
    if pygame.sprite.collide_mask(PaddlePlayer, Ball) or pygame.sprite.collide_mask(PaddleAI, Ball):
        Ball.bounce()

    DISPLAYSURF.fill(BLACK)
    pygame.draw.line(DISPLAYSURF, WHITE, (screen_size[0]//2, 0), (screen_size[0]//2,screen_size[1]))
    pygame.draw.line(DISPLAYSURF, WHITE, (0, screen_size[1]//8), (screen_size[0], screen_size[1]//8))
    all_sprites.draw(DISPLAYSURF)
    pygame.display.flip()
    FramesPerSec.tick(FPS)
pygame.quit()
