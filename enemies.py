import pygame
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

        # Image of the block
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(PINK)

        # Rectangle of the block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        # print(self.game.bg_movement, self.rect.x)
        pass
