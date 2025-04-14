import pygame
import random
from config import *
from utilities import *

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
        self.dx = 0
        self.dy = 0
        self.velocity_y = 0
        self.falling = False
        self.last_knockback = -1000
        self.camera_reset = [False, [0, 0]]
        self.attack = None
        self.damage_num = None
        
        self.camera_speed_x = 0
        self.camera_speed_y = 0
        
        # State variables
        self.health = 3
        """Health of the enemy"""
        self.direction = 'right'
        """Direction of the player"""
        self.camera_reset = [False, [0, 0]]
        """Variable containing:\n
        0: boolean to specify whether camera reset has been enabled or not\n
        1: an array containing the changes done in x and y"""
        self.invincibility_time = 1000
        """Time the enemy is invincible after being hit"""
        self.Jumping = False
        """Boolean of whether the player is jumping or not"""
        self.velocity_y = 20 
        """This is the velocity of the player in the y-axis"""
        self.state = 'idle'
        """Animation state of the player"""
        self.frame = 0
        """Frame of the player animation"""
        self.last_update = pygame.time.get_ticks()
        """Last time the player animation was updated"""
        self.previous_hit_time = -self.invincibility_time
        """Last time the player was hit/damaged"""
        

        # Image of the block
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(PINK)

        # Rectangle of the block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def knockbacked(self):
        if pygame.time.get_ticks() >= self.last_knockback:
            return False
        return True
    
    def gravity(self):
        # Gravity
        self.velocity_y += 1
        if self.velocity_y > 20:
            self.velocity_y = 20
        self.dy += self.velocity_y

    def collision_blocks(self):
        # Collision with the blocks
        for block in self.game.blocks:
            if not block.walkthrough:
                # Collision in X-axis
                if block.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.dx = 0
                # Collision in Y-axis
                elif block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.velocity_y < 0:
                        self.dy = block.rect.bottom - self.rect.top
                        self.velocity_y = 0
                        self.Jumping = False
                        self.falling = True
                    if self.velocity_y > 0:
                        self.dy = block.rect.top - self.rect.bottom
                        self.velocity_y = 0
                        self.Jumping = False
                        self.falling = False
        

        # Update the position of the player
        if self.dy > 0:
            self.falling = True
        self.rect.x += self.dx
        self.rect.y += self.dy

    
    def update(self):
        self.collision_blocks()
        self.damaged()
        self.camera_shake()
        self.gravity()
        self.movement()
        if self.health <= 0:
            self.kill()
        
    def camera_shake(self):
        # Camera shake when the player is knocked back
        if self.knockbacked():
            ran_x = random.randint(-1, 1)
            self.camera_reset[1][0] += ran_x
            ran_y = random.randint(0, 0)
            self.camera_reset[1][1] += ran_y
            for sprite in self.game.all_sprites:
                sprite.rect.x += ran_x
                sprite.rect.y += ran_y


        elif self.camera_reset[0]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.camera_reset[1][0]
                sprite.rect.y -= self.camera_reset[1][1]
            self.camera_reset = [False, [0, 0]]

    def damaged(self):
        player_attack = self.game.player.attack
        if player_attack:
            if self.rect.colliderect(player_attack.rect.x, player_attack.rect.y, player_attack.rect.width, player_attack.rect.height):
                self.last_knockback = pygame.time.get_ticks() + self.invincibility_time
                self.damage_num = Damage_number(self.game,self.rect.x, self.rect.y, self.game.player.attack.damage)
                self.health -= self.game.player.attack.damage
                if self.game.player.direction == 'left':
                    self.rect.x = player_attack.rect.x - player_attack.rect.width
                    self.dx = -20 
                else:
                    self.rect.x = player_attack.rect.x + player_attack.rect.width
                    self.dx = 20
    
    def movement(self):
        """If Player attack hits the enemy, they will be knockbacked. Also kills the damage number object"""
        if self.dx != 0 and self.knockbacked():
            if self.dx < 0:
                self.dx += 1
            else:   
                self.dx -= 1
        else:
            if self.damage_num:
                self.last_knockback = pygame.time.get_ticks() + self.invincibility_time
                self.camera_reset[0] = True
                self.damage_num = None
    
    
                    
