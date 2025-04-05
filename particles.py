import pygame
import random
import math
from config import *

def particle_generator(self):
    if pygame.time.get_ticks() > self.particles_update + 100:
        Particles(self, 30, pygame.time.get_ticks(), 10, 7)
        Particles(self, 20, pygame.time.get_ticks(), 7, 5)
        Particles(self, 10, pygame.time.get_ticks(), 5, 0)
        self.particles_update = pygame.time.get_ticks()
        
class Particles(pygame.sprite.Sprite):
    def __init__(self, game, size, time, alpha, deviation = 0):
        self.game = game
        self.time = time
        self.size = size
        self.death_time = random.randint(0, 1000)
        self.groups = self.game.all_sprites
        self._layer = PLAYER_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface([size, size], pygame.SRCALPHA)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIN_WIDTH / 2) 
        self.rect.centery = (WIN_HEIGHT / 3) - deviation
        self.speed = 1000
        self.dx = 0
        self.dy = 0 
        
        pygame.draw.circle(self.image, BLUE, (size / 2, size / 2), size / 2)
        # self.image.fill(WHITE)
    
    def update(self):
        self.dy -= 0.1
        
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if pygame.time.get_ticks() > self.time + self.death_time:
            self.kill()




