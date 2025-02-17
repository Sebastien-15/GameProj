import pygame
import os
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.reset = [640, 640]
        self.x = x
        """X-coordinate of the player"""
        self.y = y
        """Y-coordinate of the player"""
        self.dx = 0
        """Displacement in the x-axis"""
        self.dy = 0
        """Displacement in the y-axis"""
        self.width = 50
        """Width of the player"""
        self.height = 70
        """Height of the player"""
        self.camera_speed_x = 0
        self.camera_speed_y = 0
        
        # State variables
        self.direction = 'right'
        """Direction of the player"""
        self.camera_reset = [False, [0, 0]]
        """Variable containing:\n
        0: boolean to specify whether camera reset has been enabled or not\n
        1: an array containing the changes done in x and y"""
        self.knockbacked = False
        """Boolean of whether the player is knocked back"""
        self.invincibility_time = 200
        """Time the player is invincible after being hit"""
        self.Jumping = False
        """Boolean of whether the player is jumping or not"""
        self.falling = False
        """Boolean of whether the player is falling or not"""
        self.velocity_y = 20 
        """This is the velocity of the player in the y-axis"""
        self.state = 'idle'
        """Animation state of the player"""
        self.frame = 0
        """Frame of the player animation"""
        self.last_update = pygame.time.get_ticks()
        """Last time the player animation was updated"""
        self.attack = None
        """Attack object"""
        self.previous_hit_time = -self.invincibility_time
        """Last time the player was hit/damaged"""

        # Player Images
        self.idle_images = []
        self.run_images = []
        self.attack_images = []
        self.jump_images = []
        self.damaged = None
        self.load_images()

        # Player Image
        # Calculating the scale ratio for the player image

        # Loading the player image and scaling it

        # Creating the player surface where the image will be blitted onto
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(self.idle_images[0], (0,0))

        # Player Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        """Loads the player images"""
        states = os.listdir('IMG/character/Player/')
        for state in states:
            for image in os.listdir(f'IMG/character/Player/{state}'):
                if image != 'states.png':
                    image = pygame.image.load(f'IMG/character/Player/{state}/{image}').convert_alpha()
                    image_width = image.get_width() 
                    image_height = image.get_height()
                    scale_ratio_width = self.width / image_width
                    scale_ratio_height = self.height / image_height            
                    image_scaled = pygame.transform.scale(image, (math.floor(image_width * scale_ratio_width), math.floor(image_height * scale_ratio_height)))
                    match state:
                        case "Idle":
                            self.idle_images.append(image_scaled)
                        case "Run":
                            self.run_images.append(image_scaled)
                        case "Jump":
                            self.jump_images.append(image_scaled)
                        case "Attack":
                            self.attack_images.append(image_scaled)
                        case "Damaged":
                            self.damaged = image_scaled
                        

    def flip(self):
        # Flipping the player image
        if self.direction == 'right':
            self.image = pygame.transform.flip(self.image, False, False)
        else:
            self.image = pygame.transform.flip(self.image, True, False)

    def animate(self):
        if pygame.time.get_ticks() - self.last_update > 100:
            self.frame += 1
            if self.Jumping and not self.falling and not self.knockbacked and self.state != 'attack':
                if self.frame > (len(self.jump_images) - 1):
                    self.frame = len(self.jump_images) - 3
                self.last_update = pygame.time.get_ticks()
                self.image = self.jump_images[self.frame]
            elif self.falling and not self.knockbacked and self.state != 'attack':
                if self.frame > (len(self.jump_images) - 1):
                    self.frame = len(self.jump_images) - 3
                self.last_update = pygame.time.get_ticks()
                self.image = self.jump_images[self.frame]
            elif self.knockbacked and self.state != 'attack':
                self.image = self.damaged
            else:
                match self.state:
                    case 'idle':
                        if self.frame > (len(self.idle_images) - 1):
                            self.frame = 0
                        self.last_update = pygame.time.get_ticks()
                        self.image = self.idle_images[self.frame]
                    case 'run':
                        if self.frame > (len(self.run_images) - 1):
                            self.frame = 0
                        self.last_update = pygame.time.get_ticks()
                        self.image = self.run_images[self.frame]
                    case 'attack':
                        if self.frame > (len(self.attack_images) - 1):
                            self.frame = 0
                            self.state = 'idle'
                            self.attack = None
                        else:
                            if self.frame == 2 or self.frame == 4:
                                if self.direction == 'right':
                                    self.attack = Attack(self.game, self.rect.x + self.rect.width, self.rect.y, 'slash')
                                elif self.direction == 'left':
                                    self.attack = Attack(self.game, self.rect.x - self.rect.width - 10, self.rect.y, 'slash') 
                            else: 
                                self.attack = None
                            self.last_update = pygame.time.get_ticks()
                            self.image = self.attack_images[self.frame]
            self.flip()
    
    def update(self):
        self.collision_enemy_projectile()
        self.animate()
        self.movement()
        self.camera_movement()
        self.camera_shake()

    def camera_shake(self):
        # Camera shake when the player is knocked back
        if self.knockbacked:
            ran_x = random.randint(-3, 3)
            self.camera_reset[1][0] += ran_x
            ran_y = random.randint(-3, 3)
            self.camera_reset[1][1] += ran_y
            for sprite in self.game.all_sprites:
                sprite.rect.x += ran_x
                sprite.rect.y += ran_y


        elif self.camera_reset[0]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.camera_reset[1][0]
                sprite.rect.y -= self.camera_reset[1][1]
            self.camera_reset = [False, [0, 0]]
            self.reset[0] -= self.camera_reset[1][0]
            self.reset[1] -= self.camera_reset[1][1]
        
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
        
        
        self.reset[0] -= math.ceil(self.camera_speed_x) 
        self.reset[1] -= math.ceil(self.camera_speed_y)
                
    def collision_blocks(self):
        # Collision with the blocks
        for block in self.game.blocks:
            if not block.walkthrough:
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
        self.reset[0] += math.ceil(self.dx)
        self.reset[1] += math.ceil(self.dy)
    
    def collision_enemy_projectile(self):
        if not self.knockbacked:
            for projectile in self.game.enemy_projectiles:
                if projectile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.previous_hit_time = pygame.time.get_ticks()
                    if projectile.speed[0] > 0:
                        self.knockbacked = True
                        self.dx = 10 
                    else:
                        self.knockbacked = True
                        self.dx = -10
                    projectile.kill()
        if not self.knockbacked:
            for projectile in self.game.enemy_projectiles_fast:
                if projectile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.previous_hit_time = pygame.time.get_ticks()
                    if projectile.speed[0] > 0:
                        self.knockbacked = True
                        self.dx = 100 
                    else:
                        self.knockbacked = True
                        self.dx = -100
                    projectile.kill()
                

    def collision_enemies(self):
        # Collision with the enemies
        # If the player collides with the enemy, the player will be knocked back
        # The player will be knocked back for 1 second and invilnureabilty for 1 second
        if not self.knockbacked:
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
                elif enemy.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    self.previous_hit_time = pygame.time.get_ticks()
                    if self.dy > 0:
                        self.rect.y = enemy.rect.y - enemy.rect.height
                        self.velocity_y = -20
                        self.Jumping = True
                        self.falling = False
                        self.knockbacked = True
                    if self.dy < 0:
                        self.rect.y = enemy.rect.y + enemy.rect.height
                        self.velocity_y = 20
                        self.Jumping = False
                        self.falling = True
                        self.knockbacked = True
        


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
        if keys[pygame.K_r]:
            self.rect.x = self.reset[0]
            self.rect.y = self.reset[1]
            self.reset = [640, 640]
        if keys[pygame.K_a] and not self.knockbacked:
            self.dx = -PLAYER_SPEED
            self.direction = 'left'
        if keys[pygame.K_d] and not self.knockbacked:
            self.dx = PLAYER_SPEED
            self.direction = 'right'
        if keys[pygame.K_w] and not self.Jumping and not self.falling and not self.knockbacked:
            if self.state != 'attack':
                self.frame = 0
            self.Jumping = True
            self.velocity_y = -20
        if keys[pygame.K_ESCAPE]:
            self.game.running = False
            self.game.playing = False

        if keys[pygame.K_SPACE] and self.state != 'attack' and not self.knockbacked:
            self.state = 'attack'
            self.frame = 0 

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
        
        if self.state == 'attack' and not self.Jumping and not self.knockbacked:
            self.dx = 0
        
        
        if self.state != 'attack':
            if self.dx != 0 and not self.Jumping:
                self.state = 'run'
            else:
                self.state = 'idle'
        
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
    def __init__(self, game, x, y, attack_type):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.attack_type = attack_type

        self.image = pygame.Surface([60, 40])
        self.image.set_colorkey(BLACK)
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        if self.attack_type == 'slash':
            self.rect.x = x 
            self.rect.y = y + random.randint(0, 30)
        
        self.kill_timer = pygame.time.get_ticks()
        self.camera_reset = [False, [0, 0]]
    
    def collisioncheck(self):
        for enemy in self.game.enemies:
            if enemy.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                print('hit an enemy')
                

    def animate(self):
        self.collisioncheck()
        if pygame.time.get_ticks() >= self.kill_timer + 100:
            self.kill()

    def update(self):
        self.animate()
