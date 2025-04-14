import pygame
import random
from utilities import *
from .enemies import Enemy

class Shooter(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(BLUE)
        self.last_shot = pygame.time.get_ticks()
        self.last_move = pygame.time.get_ticks()
        self.health = 10
        
        """Last time the enemy shot"""
        self.direction = 1
        """Direction of the enemy"""
    
    def update(self):
        super().update()
        self.shoot()
        
    
    def movement(self):
        super().movement()
        if pygame.time.get_ticks() > self.last_move + 5000:
            if pygame.time.get_ticks() > self.last_move + 7000:
                self.dx = 0
                self.last_move = pygame.time.get_ticks()
                if self.direction == 0:
                    self.direction = 1
                else:
                    self.direction = 0
            else:
                if self.direction == 0:
                    self.dx = 2
                else:
                    self.dx = -2
    
    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot >= 1000:
            speed_x = 0
            if self.game.player.rect.x <= self.rect.x:
                speed_x = -9
            else:
                speed_x = 9
            Enemy_projectile_fast(self.game, self.rect.center[0], self.rect.center[1], speed_x)
            self.last_shot = pygame.time.get_ticks()
            
        # if pygame.time.get_ticks() - self.last_shot >= 25:
        #     speed_x = 0
        #     if self.game.player.rect.x <= self.rect.x:
        #         speed_x = -9
        #     else:
        #         speed_x = 9
        #     Enemy_projectile(self.game, self.rect.center[0], self.rect.center[1], speed_x)
        #     self.last_shot = pygame.time.get_ticks()
        
          
class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed_x):
        self.game = game
        self._layer = PLAYER_LAYER
        
       
        self.groups = self.game.all_sprites, self.game.enemy_projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface([4, 4])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = [speed_x, random.randint(-3, 3)]
    
    def update(self):
        self.rect.y += self.speed[1]
        self.rect.x += self.speed[0]
        if self.rect.x <= 0 or self.rect.x >= WIN_WIDTH:
            self.kill()
            
class Enemy_projectile_fast(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed_x):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemy_projectiles_fast
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface([12, 5])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = [speed_x * 4, 0]
    
    def update(self):
        self.rect.y += self.speed[1]
        self.rect.x += self.speed[0]
        if self.rect.x <= 0 or self.rect.x >= WIN_WIDTH:
            self.kill()