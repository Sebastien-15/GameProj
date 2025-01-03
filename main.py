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
        pygame.display.set_caption("Project X")
        self.clock = pygame.time.Clock()
        self.FPS = 0
        self.running = True
        self.bg_movement = 0
        self.bg_name = 'BG1'
        self.last_update = 0
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
        if self.last_update < pygame.time.get_ticks():    
            self.all_sprites.update()
            if self.bg_movement:
                self.background.update()
            self.last_update = pygame.time.get_ticks() + 10

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BLACK)
        self.draw_background()
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.font.render(f'FPS: {self.FPS}', True, GREEN), (0, 0))
        self.clock.tick(FPS)
        pygame.display.update()
    
    def draw_background(self):
        for position_offset in range(15):
            for background in self.background:
                background.draw(position_offset)
    
    def load_background(self):
        "Loads the background layers, only called once"
        # Loading the full preview and getting the width and the height
        preview = pygame.image.load(f'IMG/{self.bg_name}/Preview.png')
        preview_width = preview.get_width()
        
        #
        layers = pygame.image.load(f'IMG/{self.bg_name}/layers.png')
        adjusted_layers_width = (layers.get_width() * WIN_WIDTH) / preview_width
        total_layer_num = layers.get_width() / preview_width
        
        for layer_num in range(int(total_layer_num)):
            offset = (layer_num / total_layer_num)
            Background_Layer(self, pygame.transform.scale(layers, (adjusted_layers_width, WIN_HEIGHT)), offset, layer_num, WIN_WIDTH)

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