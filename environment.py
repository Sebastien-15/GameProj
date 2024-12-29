import pygame
import os
import random
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, ground_images):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

        # Image of the block
        # image = pygame.transform.scale(pygame.image.load('IMG/BG1/grass.png').convert_alpha(), (self.width, self.height))
        self.image = ground_images[random.randint(0, len(ground_images) - 1)]

        # Rectangle of the block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Border(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.border
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    

class Background_Layer(pygame.sprite.Sprite):
    def __init__(self, game, image, offset):
        self.game = game
        self.groups = self.game.background
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.offset = offset
        self.image = image
        self.rect = self.image.get_rect()
        self.witdh = self.image.get_width()

        self.image.blit(image, (0, 0))

        self.rect.x = 0
        self.rect.y = -300
    
    def update(self):
        self.rect.x = (self.game.bg_movement * self.offset)
    
    def draw(self, position_offset):
        self.game.screen.blit(self.image, (self.rect.x + (self.witdh * position_offset), self.rect.y))
    
    # def update(self):
    #     for x in range(1):   
    #         for image_num in range(len(self.bg_images)):
    #             self.game.screen.blit(self.bg_images[image_num], ((1 * WIN_WIDTH) + (self.game.bg_movement * (image_num / (len(self.bg_images) + 2))), -300))

