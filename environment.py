import pygame
import os
import math
import random
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, ground_images):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = 40
        self.height = 40

        # Image of the block
        # image = pygame.transform.scale(pygame.image.load('IMG/BG1/grass.png').convert_alpha(), (self.width, self.height))
        # self.image = ground_images[random.randint(0, len(ground_images) - 1)]

        self.image = pygame.Surface([self.width, self.height])

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
    def __init__(self, game, image, offset, layer_num, width):
        self.game = game
        self.groups = self.game.background
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.offset = offset
        self.layer_num = layer_num
        self.image = pygame.Surface([width - 1, WIN_HEIGHT])
        self.image.set_colorkey(BLACK)
        self.image.blit(image, (layer_num * -width, 0))
        
        self.rect = self.image.get_rect()
    
    def update(self):
        if self.game.bg_movement < 0:
            self.dx = math.floor(self.game.bg_movement * self.offset)
        else:
            self.dx = math.ceil(self.game.bg_movement * self.offset)
        self.rect.x += self.dx
    
    def draw(self, position_offset):
        self.game.screen.blit(self.image, (self.rect.x + (self.rect.width * position_offset), self.rect.y))
    
    # def update(self):
    #     for x in range(1):   
    #         for image_num in range(len(self.bg_images)):
    #             self.game.screen.blit(self.bg_images[image_num], ((1 * WIN_WIDTH) + (self.game.bg_movement * (image_num / (len(self.bg_images) + 2))), -300))

