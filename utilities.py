import pygame
import math
from config import *

class Damage_number(pygame.sprite.Sprite):
    def __init__(self, game, x, y, damage_num = 1):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.timer = pygame.time.get_ticks()
        self.image = pygame.Surface([40,40])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 20
        
        self.image.blit(self.game.font.render(str(damage_num), True, WHITE), (0,0))
    
    def update(self):
        if pygame.time.get_ticks() - self.timer >= 1000:
            self.kill()
        else:
            self.rect.y -= 1
    

def camera_movement(self):
        # CAMERA MOVEMENT X-AXIS
        # If the player is at the edge of the screen, move the blocks instead of the player
        
        if self.rect.x >= (WIN_WIDTH * (2 / 3)):
            if self.camera_speed_x < 4:
                self.camera_speed_x += 0.3
            
        # elif self.rect.x <= (WIN_WIDTH * (1 / 3)) and self.game.border.sprites()[0].rect.x < -self.game.border.sprites()[0].width:
        elif self.rect.x <= (WIN_WIDTH * (1 / 3)):
            if self.camera_speed_x > -5:
                self.camera_speed_x -= 0.3
        else:
            if self.camera_speed_x != 0:
                if self.camera_speed_x > 0:
                    if self.camera_speed_x < 0.2:
                        self.camera_speed_x = 0
                    else:
                        self.camera_speed_x -= 0.2
                elif self.camera_speed_x < 0:
                    # if self.camera_speed_x > -0.2 or self.game.border.sprites()[0].rect.x > -self.game.border.sprites()[0].width:
                    if self.camera_speed_x > -0.2:
                        self.camera_speed_x = 0
                    else:
                        self.camera_speed_x += 0.2
        # CAMERA MOVEMENT Y-AXIS
        # If the player is at the edge of the screen, move the blocks instead of the player
        if self.rect.y >= (WIN_HEIGHT * (3/4)):
            if self.camera_speed_y < 9:
                self.camera_speed_y += 0.3
        elif self.rect.y <= (WIN_HEIGHT * (1 / 3)):
            if self.camera_speed_y > -7:
                self.camera_speed_y -= 0.3
        else:
            if self.camera_speed_y != 0:
                if self.camera_speed_y > 0:
                    if self.camera_speed_y < 0.6:
                        self.camera_speed_y = 0
                    else:
                        self.camera_speed_y -= 0.6
                elif self.camera_speed_y < 0:
                    if self.camera_speed_y > -0.2:
                        self.camera_speed_y = 0
                    else:
                        self.camera_speed_y += 0.2
                
        self.game.bg_movement = math.floor(-self.camera_speed_x)
        for sprite in self.game.all_sprites:
            sprite.rect.x -= math.ceil(self.camera_speed_x) 
            sprite.rect.y -= math.ceil(self.camera_speed_y)
        
        