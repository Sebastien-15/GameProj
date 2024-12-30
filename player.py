import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        # State variables
        self.direction = 'right'
        self.knockbacked = False
        self.invincibility_time = 500
        self.Jumping = False
        self.falling = False
        self.velocity_y = 20
        self.camera_reset = False

        self.previous_hit_time = pygame.time.get_ticks()

        # Player Image
        image = pygame.image.load('player_idle.png')
        self.image = pygame.Surface([30, 40])
        self.image.set_colorkey(BLACK)
        self.image.blit(image, (0, 0))

        # Player Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.width)
    
    def update(self):
        self.movement()
        self.camera_movement()
        self.camera_shake()

    def camera_shake(self):
        # Camera shake when the player is knocked back
        if self.knockbacked:
            ran_x = random.randint(-3, 3)
            ran_y = random.randint(-3, 3)
            for sprite in self.game.all_sprites:
                if sprite not in self.game.background:
                    sprite.rect.x += ran_x
                    sprite.rect.y += ran_y
        
    def camera_movement(self):
        # CAMERA MOVEMENT X-AXIS
        # If the player is at the edge of the screen, move the blocks instead of the player
        if self.dx > 0 and self.rect.x >= (WIN_WIDTH * (2 / 3)):
            self.game.bg_movement -= self.dx
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.dx
        if self.dx < 0 and self.rect.x <= (WIN_WIDTH * (1 / 3)) and (self.game.border.sprites()[0].rect.x - self.dx) <= -5:
            self.game.bg_movement -= self.dx
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.dx
        # CAMERA MOVEMENT Y-AXIS
        # If the player is at the edge of the screen, move the blocks instead of the player
        if self.dy > 0 and self.rect.y >= (WIN_HEIGHT - 80):
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.dy
        if self.dy < 0 and self.rect.y <= (WIN_WIDTH * (1 / 3)):
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.dy
                
    def collision_blocks(self):
        # Collision with the blocks
        for block in self.game.blocks:
            # Collision in X-axis
            if block.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0
            # Collision in Y-axis
            if block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.velocity_y < 0:
                    self.dy = block.rect.bottom - self.rect.top
                    self.velocity_y = 0
                    self.Jumping = False
                    self.falling = True
                elif self.velocity_y >= 0:
                    self.dy = block.rect.top - self.rect.bottom
                    self.velocity_y = 0
                    self.Jumping = False
                    self.falling = False
        

        # Update the position of the player
        if self.dy > 0:
            self.falling = True
        self.rect.x += self.dx
        self.rect.y += self.dy

    def collision_enemies(self):
        # Collision with the enemies
        # If the player collides with the enemy, the player will be knocked back
        # The player will be knocked back for 1 second and invilnureabilty for 1 second
        if pygame.time.get_ticks() - self.previous_hit_time > self.invincibility_time:
            for enemy in self.game.enemies:
                # Knockback in X-axis
                if enemy.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.previous_hit_time = pygame.time.get_ticks()
                    if self.dx > 0:
                        self.rect.x = enemy.rect.x - enemy.rect.width
                        self.knockbacked = True
                        self.dx = -20 
                    elif self.dx < 0:
                        self.rect.x = enemy.rect.x + enemy.rect.width
                        self.knockbacked = True
                        self.dx = 20
                # Knockback in Y-axis
                # elif enemy.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                #     self.previous_hit_time = pygame.time.get_ticks()
                #     if self.dy > 0:
                #         self.rect.y = enemy.rect.y - enemy.rect.height
                #         self.velocity_y = -20
                #         self.Jumping = True
                #         self.falling = False
                #         self.knockbacked = True
                #     if self.dy < 0:
                #         self.rect.y = enemy.rect.y + enemy.rect.height
                #         self.velocity_y = 20
                #         self.Jumping = False
                #         self.falling = True
                #         self.knockbacked = True
        


    def movement(self):
        if not self.knockbacked:
            # Resetting displacement values
            self.dx = 0
            self.dy = 0
        else:
            if self.dx == 0:
                self.knockbacked = False
            else:
                # Slowing down the knockback speed
                if self.dx > 0:
                    self.dx -= 2
                if self.dx < 0:
                    self.dx += 2

        # Reading all of the key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.knockbacked:
            self.dx = -PLAYER_SPEED
            self.direction = 'left'
        if keys[pygame.K_d] and not self.knockbacked:
            self.dx = PLAYER_SPEED
            self.direction = 'right'
        if keys[pygame.K_w] and not self.Jumping and not self.falling and not self.knockbacked:
            self.Jumping = True
            self.velocity_y = -20
        if keys[pygame.K_ESCAPE]:
            self.game.running = False
            self.game.playing = False

        if keys[pygame.K_SPACE]:
            if self.direction == 'right':
                Attack(self.game, self.rect.x + self.rect.width, self.rect.y)
            if self.direction == 'left':
                Attack(self.game, self.rect.x - self.rect.width, self.rect.y)   

        # Gravity
        self.velocity_y += 1
        if self.velocity_y > 20:
            self.velocity_y = 20
        self.dy += self.velocity_y

        # Collision with the blocks
        self.collision_blocks()
        # Collision with the enemies
        self.collision_enemies()
        
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y

        self.image = pygame.Surface([40, 40])
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y
        print(self.rect.width)

    def animate(self):
        self.kill()

    def update(self):
        self.animate()
