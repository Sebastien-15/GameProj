import pygame
import os
import math
import random
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, walkthrough, asset_type):
        self.game = game
        if walkthrough:
            self._layer = WALKTHROUGH_LAYER
        else:
            self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.walkthrough = walkthrough
        # Image of the block=

        self.image = pygame.Surface([self.width, self.height])
        if self.walkthrough:
            self.image.fill(GRAY)
        else: 
            self.image.blit(self.game.block_images[random.randint(0, len(self.game.block_images) - 1)])
        self.image.set_colorkey(BLACK)

        # Rectangle of the block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if asset_type == 10: 
            Vegetation(self.game, asset_type, self.rect.x, self.rect.y)
    

class Border(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.border
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = -self.width
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


class Vegetation(pygame.sprite.Sprite):
    def __init__(self, game, asset_type, x, y):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.frame = 0
        self.asset_type = asset_type
        self.last_update = pygame.time.get_ticks()
        
        match asset_type:
            case 10:
                self.width = TREE_WIDTH
                self.height = TREE_HEIGHT
        
                self.image = pygame.Surface([self.width, self.height])
                self.image.set_colorkey(BLACK)
                self.image.blit(self.game.vegetation_images[asset_type][self.frame], (0, 0))
                
                self.rect = self.image.get_rect()
                self.rect.x = x 
                self.rect.y = y - self.height 
        
    def animate(self):
        if pygame.time.get_ticks() - self.last_update > 125:
            self.frame +=1
            self.last_update = pygame.time.get_ticks()
            if self.frame == len(self.game.vegetation_images[self.asset_type]) - 1:
                self.frame = 0
        self.image = self.game.vegetation_images[self.asset_type][self.frame]
                
    def update(self):
        if self.asset_type == 10:
            self.animate()