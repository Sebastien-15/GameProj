import pygame
import math
from config import *

class Damage_number(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([40,40])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 20
        
        self.image.blit(self.game.font.render('1', True, WHITE), (0,0))
    


def movement(self):
        self.dy = 0
        # print(self.rect.x, self.reset[0])
        if self.knockbacked:
            if pygame.time.get_ticks() - self.previous_hit_time > self.invincibility_time:
                self.knockbacked = False
                self.camera_reset[0] = True
            else:
                # Slowing down the knockback speed
                if self.dx > 0:
                    self.dx -= 2
                elif self.dx < 0:
                    self.dx += 2

        # Reading all of the key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and pygame.time.get_ticks() - self.game.switch_time >= 1000:
            self.game.switch_time = pygame.time.get_ticks()
            if self.game.player == self.game.enemy:
                self.game.player = self.game.original
            else:
                self.game.player = self.game.enemy
            
        if keys[pygame.K_a] and not self.knockbacked:
            if self.dx > -PLAYER_SPEED:
                self.dx += -1
            self.direction = 'left'
        if keys[pygame.K_d] and not self.knockbacked:
            if self.dx < PLAYER_SPEED:
                self.dx += 1
            self.direction = 'right'
        if keys[pygame.K_w] and not self.Jumping and not self.falling and not self.knockbacked:
            if self.state != 'attack':
                self.frame = 0
            self.Jumping = True
            self.velocity_y = -22
        if keys[pygame.K_ESCAPE]:
            self.game.running = False
            self.game.playing = False

        if keys[pygame.K_SPACE] and self.state not in ['attack', 'down_attack', 'side_attack'] and not self.knockbacked:
            if self.last_attack + 600 < pygame.time.get_ticks():
                if True in [keys[pygame.K_a], keys[pygame.K_d]]:
                    self.state = 'side_attack'
                    self.frame = 0
                elif keys[pygame.K_s] and True in [self.Jumping, self.falling]:
                    self.state = 'down_attack'
                    self.frame = 0
                else:
                    self.state = 'attack'
                    self.frame = 0 
                self.last_attack = pygame.time.get_ticks()

        if not keys[pygame.K_a] and not keys[pygame.K_d] and self.dx != 0 and not self.knockbacked:
            if self.Jumping:
                if self.dx > 0:
                    self.dx -= 0.1
                elif self.dx < 0:
                    self.dx += 0.1
            else:
                if self.dx > 0 and self.dx % 0.25 == 0:
                    self.dx -= 0.25
                elif self.dx < 0 and self.dx % 0.25 == 0:
                    self.dx += 0.25
                else:
                    self.dx = 0
        
        # if self.state == 'attack' and not self.Jumping and not self.knockbacked:
        #     self.dx = 0
        
        
        if self.state not in ['attack', 'down_attack', 'side_attack']:
            if self.dx != 0 and not self.Jumping:
                self.state = 'run'
            else:
                self.state = 'idle'
        
        # Gravity
        self.velocity_y += 1
        if self.velocity_y > 20 and self.state != 'down_attack':
            self.velocity_y = 20
        self.dy += self.velocity_y

        # Collision with the blocks
        self.collision_blocks()
        # Collision with the enemies
        # self.collision_enemies()
        
        
                            
        match self.state:
            case 'down_attack':
                if True in [self.falling, self.Jumping]:
                    self.velocity_y = 30
                    if self.direction == 'right':
                        self.dx = 15
                    else:
                        self.dx = -15
                else:
                    self.dx = 0
                    self.state = 'idle'
                    
            case 'side_attack':
                if self.frame >= 2:
                    self.frame = 0
                    self.state = 'idle'
                    self.dx = 0
                else:
                    if self.direction == 'right':
                        self.dx = 30
                    else:
                        self.dx = -30

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
        
        