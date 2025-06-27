import pygame
import os
import math
import random
from config import *
from utilities import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
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
        self.forceCameraShake = 0
        
        # State variables
        self.last_attack = 0
        """Cooldown for attacking"""
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
            # Trail(self.game, self.rect.x, self.rect.y, 50, 50)
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
    
    def trail(self):
        if self.state in ['down_attack', 'side_attack']:
            Trail(self.game, self.rect.x, self.rect.y, 25, 25)
            Trail(self.game, self.rect.x + 7, self.rect.y, 20, 20)
    
    def update(self):
        self.collision_enemy_projectile()
        self.animate()
        self.collision_enemies()
        # if self.game.player == self:
        self.movement()
        camera_movement(self)
        self.camera_shake()
        self.trail()
        
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
        if self.game.keys[pygame.K_a] and not self.knockbacked:
            if self.dx > -PLAYER_SPEED:
                self.dx += -1
            self.direction = 'left'
        if self.game.keys[pygame.K_d] and not self.knockbacked:
            if self.dx < PLAYER_SPEED:
                self.dx += 1
            self.direction = 'right'
        if self.game.keys[pygame.K_w] and not self.Jumping and not self.falling and not self.knockbacked:
            if self.state != 'attack':
                self.frame = 0
            self.Jumping = True
            self.velocity_y = -22
        if self.game.keys[pygame.K_ESCAPE]:
            self.game.running = False
            self.game.playing = False

        if self.game.keys[pygame.K_SPACE] and self.state not in ['attack', 'down_attack', 'side_attack'] and not self.knockbacked:
            if self.last_attack + 600 < pygame.time.get_ticks():
                if True in [self.game.keys[pygame.K_a], self.game.keys[pygame.K_d]]:
                    self.state = 'side_attack'
                    self.frame = 0
                elif self.game.keys[pygame.K_s] and True in [self.Jumping, self.falling]:
                    self.state = 'down_attack'
                    self.frame = 0
                else:
                    self.state = 'attack'
                    self.frame = 0 
                self.last_attack = pygame.time.get_ticks()

        if not self.game.keys[pygame.K_a] and not self.game.keys[pygame.K_d] and self.dx != 0 and not self.knockbacked:
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


    def camera_shake(self):
        # Camera shake when the player is knocked back
        if self.knockbacked or self.forceCameraShake + 100 >= pygame.time.get_ticks():
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
                        if self.state == 'down_attack':
                            self.dy = block.rect.top - self.rect.bottom
                            self.velocity_y = -20
                            self.forceCameraShake = pygame.time.get_ticks()
                            self.Jumping = False
                            self.falling = False
                        else:
                            self.dy = block.rect.top - self.rect.bottom
                            self.velocity_y = 0
                            self.Jumping = False
                            self.falling = False
        

        # Update the position of the player
        if self.dy > 0:
            self.falling = True
        self.rect.x += self.dx
        self.rect.y += self.dy
    
    def collision_enemy_projectile(self):
        if not self.knockbacked:
            for projectile in self.game.enemy_projectiles:
                if projectile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.previous_hit_time = pygame.time.get_ticks()
                    if projectile.speed[0] > 0:
                        self.knockbacked = True
                        self.dx = 10 
                    elif projectile.speed[0] == 0:
                        self.knockbacked = True
                        self.dx = 0
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
                        self.dx = 40 
                    else:
                        self.knockbacked = True
                        self.dx = -40
                    projectile.kill()
                

    def collision_enemies(self):
        # Collision with the enemies
        # If the player collides with the enemy, the player will be knocked back
        # The player will be knocked back for 1 second and invulnureabilty for 1 second
        if not self.knockbacked:
            for enemy in self.game.enemies:
                # Knockback in X-axis
                if enemy.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.previous_hit_time = pygame.time.get_ticks()
                    if self.rect.midleft[0] <= enemy.rect.midleft[0]:
                        self.knockbacked = True
                        self.dx = -20 
                    else:
                        print(self.rect.midleft[0], enemy.rect.midright[0])
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

class Trail(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game = game
        self._layer = PLAYER_LAYER
        self.timer = pygame.time.get_ticks()
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.set_alpha(50)
        self.image.set_colorkey(BLACK)
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    
    def update(self):
        if pygame.time.get_ticks() - self.timer > 500:
            self.kill()
        else:
            self.rect.x += random.randint(-1, 1)
            self.rect.y += random.randint(-1, 1)
        
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, attack_type):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.attack_type = attack_type
        self.damage = random.randint(1, 5)

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
