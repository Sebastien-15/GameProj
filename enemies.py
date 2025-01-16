import pygame
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
        self.knockbacked = False

        # Image of the block
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(PINK)

        # Rectangle of the block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.display_damage_numbers()
        self.damaged()
        self.movement()
        collision_blocks(self)
        gravity(self)

    def display_damage_numbers(self):
        if self.knockbacked:
            self.game.screen.blit(self.game.font.render('1', True, RED), (self.rect.x, self.rect.y - 20))
    
    def damaged(self):
        player_attack = self.game.player.attack
        if player_attack:
            if self.rect.colliderect(player_attack.rect.x, player_attack.rect.y, player_attack.rect.width, player_attack.rect.height):
                self.knockbacked = True
                if self.game.player.direction == 'left':
                    self.rect.x = player_attack.rect.x - player_attack.rect.width
                    self.dx = -20 
                else:
                    self.rect.x = player_attack.rect.x + player_attack.rect.width
                    self.dx = 20
    
    def movement(self):
        # Collision with the enemies
        # If the player collides with the enemy, the player will be knocked back
        # The player will be knocked back for 1 second and invilnureabilty for 1 second
        if self.dx != 0 and self.knockbacked:
            if self.dx < 0:
                self.dx += 1
            else:   
                self.dx -= 1
        else:
            self.knockbacked = False
                    
