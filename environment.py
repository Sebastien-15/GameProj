import pygame
import math
import random
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, has_sides = True, walkthrough = False, asset_type = -1, border = False, intersection = False, rotation = 'standard'):
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

        self.image = pygame.Surface([self.width, self.height])
        if not has_sides:
            self.image.fill((118, 87, 65))
        else:
            if walkthrough:
                self.image.fill(GRAY)
            elif not border and not intersection:
                self.image.blit(self.game.block_images['regular'][random.randint(0, len(self.game.block_images) - 1)])
            elif border:
                self.image.blit(self.game.block_images['border'])
            elif intersection:
                self.image.blit(self.game.block_images['intersection'])

        # Rectangle of the block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if asset_type >= 0: 
            Vegetation(self.game, asset_type, self.rect.x, self.rect.y)
            
        match rotation:
            case 'standard':
                pass
            case 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            case 'upside_down':
                self.image = pygame.transform.rotate(self.image, 180)
            case 'right':
                self.image = pygame.transform.rotate(self.image, 270)
        self.image.set_colorkey(BLACK)
            
    

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
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.frame = 0
        self.asset_type = asset_type
        self.last_update = pygame.time.get_ticks()
        
        match asset_type:
            case 0:
                self.width = TREE_WIDTH
                self.height = TREE_HEIGHT
                self.animation_speed = 125
            case 1:
                self.width = BUSH_WIDTH
                self.height = BUSH_HEIGHT
                self.animation_speed = 150
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(self.game.vegetation_images[asset_type][self.frame], (0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x - (self.width / 2)
        self.rect.y = y - self.height 
        
    def animate(self):
        if pygame.time.get_ticks() - self.last_update > self.animation_speed:
            self.frame +=1
            self.last_update = pygame.time.get_ticks()
            if self.frame == len(self.game.vegetation_images[self.asset_type]) - 1:
                self.frame = 0
        self.image = self.game.vegetation_images[self.asset_type][self.frame]
                
    def update(self):
        self.animate()

class Background_rectangles(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = 0
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = random.choice([20, 20, 20, 20, 20, 80, 80, 80, 80, 160,])
        self.rotation = 0
        self.rotation_speed = 2
        self.last_update = pygame.time.get_ticks()
        self.fall_speed = random.randint(3, 5)
        
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-400, WIN_WIDTH + 400)
        self.rect.y = -self.size
        self.original = self.image
        
        self.rectangle = pygame.Rect((0, 0, self.size, self.size))

        pygame.draw.rect(self.image, BLACK, self.rectangle, random.choice([4, 4, 4, 10, 10, 10, 10, 10, 10, 10,]))
    
    def update(self):
        self.rotate()
        self.movement()
        if self.rect.y >= WIN_HEIGHT + self.size:
            self.kill()
        
    def rotate(self):
        if pygame.time.get_ticks() - self.last_update >= 10:
            old_center = self.rect.center
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            self.image = pygame.transform.rotate(self.original, self.rotation)
            self.rect = self.image.get_rect()
            self.last_update = pygame.time.get_ticks()
            self.rect.center = old_center
    
    def movement(self):
        self.rect.y += self.fall_speed
        
        
        