# Pygame template - skeleton for a new pygame project
import pygame
import random
import os
from math import fabs
from math import sqrt

width = 800
height = 600
FPS = 50

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

def trap(x1, y1, x2, y2, x3, y3):
        if (x2 < x1 < x3) and (y2 < y1 < y3):
            x1 = x3 - x2
            y1 = y3 - y2
            return True

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, color, center, up = 0, right = 0, down = 0, left = 0, flag = 1):
        pygame.sprite.Sprite.__init__(self)
        self.vx, self.vy = vx, vy = 0, 0
        self.side = 40
        self.image = pygame.Surface((self.side, self.side))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.flag = flag
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.color = color
        self.shield = 100

    def update(self):
        """Update Player state"""
        pressed = pygame.key.get_pressed()
        self.vx, self.vy = 0, 0
        if pressed[self.left] and not pressed[self.down] and not pressed[self.up] and not pressed[self.right]:
            self.vx = -1
            self.vy = 0
        if pressed[self.right] and not pressed[self.down] and not pressed[self.left] and not pressed[self.up]:
            self.vx = 1
            self.vy = 0
        if pressed[self.up] and not pressed[self.down] and not pressed[self.left] and not pressed[self.right]:
            self.vy = -1
            self.vx = 0
        if pressed[self.down] and not pressed[self.left] and not pressed[self.right] and not pressed[self.up]:
            self.vy = 1
            self.vx = 0

        self.rect.x += self.vx
        self.rect.y += self.vy

        """Do not let Tank get out of the Game window"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.bottom > height:
            self.rect.bottom = height
            
        if self.flag != 0:
            if pressed[self.up] and not pressed[self.down] and not pressed[self.left] and not pressed[self.right]:
                self.flag = 1
            if self.flag == 1:
                pygame.draw.rect(screen, [150, 100, 0], [self.rect.left + self.side / 2 - 4, self.rect.top - 15, 8, 15], 0)
            if pressed[self.right] and not pressed[self.down] and not pressed[self.left] and not pressed[self.up]:
                self.flag = 2
            if self.flag == 2:
                pygame.draw.rect(screen, [150, 100, 0], [self.rect.right, self.rect.top + self.side / 2 - 4, 15, 8], 0)
            if pressed[self.left] and not pressed[self.down] and not pressed[self.up] and not pressed[self.right]:
                self.flag = 4
            if self.flag == 4:
                pygame.draw.rect(screen, [150, 100, 0], [self.rect.left - 15, self.rect.top + self.side / 2 - 4, 15, 8], 0)
            if pressed[self.down] and not pressed[self.left] and not pressed[self.right] and not pressed[self.up]:
                self.flag = 3
            if self.flag == 3:
                pygame.draw.rect(screen, [150, 100, 0], [self.rect.left + self.side / 2 - 4, self.rect.bottom, 8, 15], 0)

    def hurt(self, Player):
        if Player.flag != 0:
            all_sprites.add(Player)
            if pygame.sprite.spritecollide(Player, bullets, True):
                Player.shield -= 20
            print Player.shield
            if Player.shield <= 0:
                all_sprites.remove(Player)
                Player.flag = 0

    def shot(self, Player):
        if Player.flag != 0:
            if self.flag == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, Player)
            if self.flag == 2:
                bullet = Bullet(self.rect.right, self.rect.centery, Player)
            if self.flag == 3:
                bullet = Bullet(self.rect.centerx, self.rect.bottom, Player)
            if self.flag == 4:
                bullet = Bullet(self.rect.left, self.rect.centery, Player)
            all_sprites.add(bullet)
            bullets.add(bullet)
            pygame.sprite.spritecollide(bullet, players, True)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.player = player

        if self.player.flag == 1:
            self.rect.bottom = y
            self.rect.centerx = x
        if self.player.flag == 2:
            self.rect.centery = y
            self.rect.left = x
        if self.player.flag == 3:
            self.rect.top = y
            self.rect.centerx = x
        if self.player.flag == 4:
            self.rect.centery = y
            self.rect.right = x

        self.v = 10
        self.flag1 = 0
        self.epsilon = 4

    def update(self):
        if self.rect.centerx == self.player.rect.centerx:
            if fabs(self.rect.bottom - self.player.rect.top) < self.epsilon:
                self.flag1 = 1
            if fabs(self.rect.top - self.player.rect.bottom) < self.epsilon:
                self.flag1 = 3
        if self.rect.centery == self.player.rect.centery:
            if fabs(self.rect.left - self.player.rect.right) < self.epsilon:
                self.flag1 = 2
            if fabs(self.rect.right - self.player.rect.left) < self.epsilon:
                self.flag1 = 4

        if self.flag1 == 1:
            self.rect.y -= self.v
        if self.rect.bottom < 0:
            self.kill()
        if self.flag1 == 2:
            self.rect.x += self.v
        if self.rect.left > width:
            self.kill()
        if self.flag1 == 3:
            self.rect.y += self.v
        if self.rect.top > height:
            self.kill()
        if self.flag1 == 4:
            self.rect.x -= self.v
        if self.rect.right < 0:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, sidex, sidey):
        pygame.sprite.Sprite.__init__(self)
        self.sidex = sidex
        self.sidey = sidey
        self.delta = 1
        self.image = pygame.Surface((self.sidex, self.sidey))
        self.image.fill((250, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.epsilon = 1

    def block(self):
        w11 = Wall(self.rect.x, self.rect.y)
        w12 = Wall(self.rect.x + self.side + self.delta, self.rect.y)
        w21 = Wall(self.rect.x, self.rect.y + self.side + self.delta)
        w22 = Wall(self.rect.x + self.side + self.delta, self.rect.y + self.side + self.delta)
        all_sprites.add(w11)
        all_sprites.add(w12)
        all_sprites.add(w21)
        all_sprites.add(w22)

    def stop(self, Wall, Player):
        if Player.flag != 0:
            if (Player.rect.bottom > Wall.rect.top) and (Player.rect.top < Wall.rect.bottom):
                if (Wall.rect.right > Player.rect.left) and (Player.rect.right > Wall.rect.left):
                    if Wall.rect.left < Player.rect.right < Wall.rect.right and Player.flag == 2:
                        Player.rect.right = Wall.rect.left
                    if Wall.rect.left < Player.rect.left < Wall.rect.right and Player.flag == 4:
                        Player.rect.left = Wall.rect.right
                    if Wall.rect.top < Player.rect.bottom < Wall.rect.bottom and Player.flag == 3:
                        Player.rect.bottom = Wall.rect.top
                    if Wall.rect.top < Player.rect.top < Wall.rect.bottom and Player.flag == 1:
                        Player.rect.top = Wall.rect.bottom
            pygame.sprite.spritecollide(Wall, bullets, True)
            pygame.sprite.spritecollide(Player, bullets, True)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TANKS")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
players = pygame.sprite.Group()

w1 = Wall(550, 150, 50, 400)
w2 = Wall(100, 50, 600, 50)
w3 = Wall(200, 150, 50, 400)
all_sprites.add(w1)
all_sprites.add(w2)
all_sprites.add(w3)

player = Player(BROWN, (60, 60), pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT)
player1 = Player(GREEN, (740, 540), pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a)

#w1.block()
#w2.block()
#w3.block()
#w4.block()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_L:
                player.shot(player)
            if event.key == pygame.K_SPACE:
                player1.shot(player1)

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    player1.update()
    player.update()

    player.hurt(player1)
    player1.hurt(player)

    w1.stop(w1, player)
    w2.stop(w2, player)
    w3.stop(w3, player)
    w1.stop(w1, player1)
    w2.stop(w2, player1)
    w3.stop(w3, player1)
    w1.stop(player1, player)
    w1.stop(player, player1)
    all_sprites.draw(screen)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
