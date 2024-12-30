import pygame
import sys
from player import *
from config import *
from environment import *
from enemies import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.FPS = 0
        self.running = True
        self.bg_movement = 0
        self.bg_name = 'BG2'
        pygame.font.init()
        self.font = pygame.font.Font(None, 32)
    
    def CreateBlock(self):
        """Creates blocks based on the assigned letter:\n
            g for grass\n
            p for the player\n
            e for the enemy\n
            b for the border"""
        ground_images = []
        for image in os.listdir(f'IMG/Ground1'):   
            ground_images.append(pygame.image.load(f'IMG/Ground1/{image}').convert_alpha())

        for i, row in enumerate(tilemap):
            for j, tile in enumerate(row):
                    if tile == 'g':
                        Block(self, j * 40, i * 40, ground_images)
                    elif tile == 'p':
                        self.player = Player(self, j * 40, i * 40)
                    elif tile == 'e':
                        Enemy(self, j * 40, i * 40)
                    elif tile == 'b':
                        Border(self, j * 40, i * 40)
    

    def new(self):
        # a new game starts
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.border = pygame.sprite.LayeredUpdates()
        self.background = pygame.sprite.LayeredUpdates()
        self.load_background()
        self.CreateBlock()
    
    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
        self.FPS = math.floor(self.clock.get_fps())
    
    def update(self):
        # Game Loop - Update    
        self.all_sprites.update()
        if self.bg_movement:
            self.background.update()

    def draw(self):
        # Game Loop - Draw
        self.draw_background()
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.font.render(f'FPS: {self.FPS}', True, GREEN), (0, 0))
        self.clock.tick(FPS)
        pygame.display.update()
    
    def draw_background(self):
        for position_offset in range(5):
            for background in self.background:
                background.draw(position_offset)
    
    def load_background(self):
        "Loads the background layers, only called once"
        # Loading the full preview and getting the width and the height
        preview = pygame.image.load(f'IMG/{self.bg_name}/Preview.png')
        preview_width = preview.get_width()
        preview_height = preview.get_height()
        
        #
        layers = pygame.image.load(f'IMG/{self.bg_name}/layers.png')
        layers_width = layers.get_width()
        total_layer_num = layers_width / preview_width
        
        for layer_num in range(int(total_layer_num)):
            if layer_num == 0:
                offset = 0.05
            else:
                offset = (layer_num / (total_layer_num + 2))
            Background_Layer(self, pygame.transform.scale(layers, (layers_width, WIN_HEIGHT)), offset, layer_num, preview_width, preview_height)
        # bg_image_list = os.listdir(f'IMG/{self.bg_name}')
        # for image_num in range(len(bg_image_list)):
        #     if image_num == 0:
        #         offset = 0.05
        #     else:
        #         offset = (image_num / (len(bg_image_list) + 2))
        #     if bg_image_list[image_num] == 'layer-12.png':
        #         Background_Layer(self, pygame.transform.scale(pygame.image.load(f'IMG/{self.bg_name}/{bg_image_list[image_num]}').convert_alpha(), (WIN_WIDTH, WIN_HEIGHT + 280)), offset) 
        #     else:   
        #         Background_Layer(self, pygame.transform.scale(pygame.image.load(f'IMG/{self.bg_name}/{bg_image_list[image_num]}').convert_alpha(), (WIN_WIDTH, WIN_HEIGHT + 300)), offset)


    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False    


if __name__ == "__main__":
    game = Game()
    game.new()
    while game.running:
        game.main()
    pygame.quit()
    sys.exit()