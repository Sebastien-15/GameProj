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
        self.game_font = pygame.font.Font(None, 48)
        self.block_images = dict()
        self.vegetation_images = dict()
        
        self.background_layer_1_last_update = 0
        self.background_layer_2_last_update = -1500
    
    def CreateBlock(self):
        """Creates blocks based on the assigned letter:\n
            g for grass\n
            p for the player\n
            e for the enemy\n
            b for the border\a
            s for passthrough blocks"""
        # Background_layer_2(self, 0)
        # Background_layer_2(self, 1)
        # Background_layer_2(self, 2)
        # Background_layer_2(self, 3)
        # Background_layer_2(self, 4)
        # Background_layer_2(self, 5)
        ground_images = []
        for image in os.listdir(f'IMG/Ground1'):   
            ground_images.append(pygame.image.load(f'IMG/Ground1/{image}').convert_alpha())
        for i, row in enumerate(tilemap):
            for j, tile in enumerate(row):
                match tile:
                    case 'g':
                        Block(self, j * 40, i * 40)
                    case 'w':
                        Block(self, j * 40, i * 40, has_sides=False)
                    case 'k':
                        Block(self, j * 40, i * 40, rotation='upside_down')
                    case 'a':
                        Block(self, j * 40, i * 40, rotation='left')
                    case 'f':
                        Block(self, j * 40, i * 40, rotation='right')
                    case 'l':
                        Block(self, j * 40, i * 40, border=True)
                    case 'y':
                        Block(self, j * 40, i * 40, intersection=True)
                    case 'v':
                        Block(self, j * 40, i * 40, intersection=True, rotation='left')
                    case 'h':
                        Block(self, j * 40, i * 40, intersection=True, rotation='upside_down')
                    case 'j':
                        Block(self, j * 40, i * 40, intersection=True, rotation='right')
                    case 'u':
                        Block(self, j * 40, i * 40, border=True, rotation='left')
                    case 'd':
                        Block(self, j * 40, i * 40, border=True, rotation='upside_down')
                    case 'r':
                        Block(self, j * 40, i * 40, border=True, rotation='right')
                    case 's':
                        Block(self, j * 40, i * 40, walkthrough=True)
                    case 'c':
                        Block(self, j * 40, i * 40, asset_type= 0)
                    case 't':
                        Block(self, j * 40, i * 40, asset_type= 1)
                    case 'p':
                        self.player = Player(self, j * 40, i * 40)
                    case 'e':
                        Enemy(self, j * 40, i * 40)
                    case 'b':
                        Border(self, j * 40, i * 40)

        # for i, row in enumerate(tilemap):
            for j, tile in enumerate(row):
                match tile:
                    case '/IMG/block_01.png':
                        Block(self, i * 40, j * 40)
                    case '/IMG/block_05.png':
                        Block(self, i * 40, j * 40, has_sides=False)
                    case '/IMG/block_03.png':
                        Block(self, i * 40, j * 40, rotation='upside_down')
                    case '/IMG/block_02.png':
                        Block(self, i * 40, j * 40, rotation='left')
                    case '/IMG/block_04.png':
                        Block(self, i * 40, j * 40, rotation='right')
                    case '/IMG/intersection_01.png':
                        Block(self, i * 40, j * 40, intersection=True)
                    case '/IMG/intersection_02.png':
                        Block(self, i * 40, j * 40, intersection=True, rotation='left')
                    case '/IMG/intersection_03.png':
                        Block(self, i * 40, j * 40, intersection=True, rotation='upside_down')
                    case '/IMG/intersection_04.png':
                        Block(self, i * 40, j * 40, intersection=True, rotation='right')
                    case '/IMG/border_01.png':
                        Block(self, i * 40, j * 40, border=True)
                    case '/IMG/border_02.png':
                        Block(self, i * 40, j * 40, border=True, rotation='left')
                    case '/IMG/border_03.png':
                        Block(self, i * 40, j * 40, border=True, rotation='upside_down')
                    case '/IMG/border_04.png':
                        Block(self, i * 40, j * 40, border=True, rotation='right')
                    case '/IMG/walkthrough_01.png':
                        Block(self, i * 40, j * 40, walkthrough=True)
                    case '/IMG/tree.png':
                        Block(self, i * 40, j * 40, asset_type= 0)
                    case '/IMG/bush.png':
                        Block(self, i * 40, j * 40, asset_type= 1)
                    case '/IMG/idle_1.png':
                        self.player = Player(self, i * 40, j * 40)
                    case '/IMG/enemy_1.png':
                        Enemy(self, i * 40, j * 40)
                    case 'b':
                        Border(self, i * 40, j * 40)
                        
    

    def new(self):
        # a new game starts
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.border = pygame.sprite.LayeredUpdates()
        self.background = pygame.sprite.LayeredUpdates()
        self.enemy_projectiles = pygame.sprite.LayeredUpdates()
        self.enemy_projectiles_fast = pygame.sprite.LayeredUpdates()
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
        self.screen.fill(BG_COLORS[0])
        self.draw_background()
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.font.render(f'FPS: {self.FPS}', True, GREEN), (WIN_WIDTH / 3, WIN_HEIGHT / 3))
        self.clock.tick(FPS)
        pygame.display.update()
    
    def draw_background(self):
        # for position_offset in range(15):
        #     for background in self.background:
        #         background.draw(position_offset)
        
        if pygame.time.get_ticks() - self.background_layer_1_last_update >= 100:
            Background_layer_1(self)
            self.background_layer_1_last_update = pygame.time.get_ticks()
        # if pygame.time.get_ticks() - self.background_layer_2_last_update >= 1500:
        #     Background_layer_2(self, 0)
        #     self.background_layer_2_last_update = pygame.time.get_ticks()
    
    def load_background(self):
        "Loads the background layers, only called once"
        # Loading the full preview and getting the width and the height
        preview = pygame.image.load(f'IMG/{self.bg_name}/Preview.png').convert_alpha()
        preview_width = preview.get_width()
        
        #
        layers = pygame.image.load(f'IMG/{self.bg_name}/layers.png').convert_alpha()
        adjusted_layers_width = (layers.get_width() * WIN_WIDTH) / preview_width
        total_layer_num = layers.get_width() / preview_width
        
        for layer_num in range(int(total_layer_num)):
            offset = (layer_num / total_layer_num)
            Background_Layer(self, pygame.transform.scale(layers, (adjusted_layers_width, WIN_HEIGHT)), offset, layer_num, WIN_WIDTH)
        
        block_images = list()
        for block_image in os.listdir("IMG/Environment/01/Blocks"):
            if "block_" in block_image:
                image = pygame.image.load(f'IMG/Environment/01/Blocks/{block_image}').convert_alpha()
                block_images.append(image)
        border_image = pygame.image.load(f'IMG/Environment/01/Blocks/Border/border_01.png').convert_alpha()
        intersection_image = pygame.image.load(f'IMG/Environment/01/Blocks/Border/intersection_01.png').convert_alpha()
        self.block_images['regular'] = block_images 
        self.block_images['border'] = border_image
        self.block_images['intersection'] = intersection_image
                
        tree_images = list() 
        for tree_image in os.listdir("IMG/Environment/01/Tree"):
            if "tree_" in tree_image:
                image = pygame.image.load(f'IMG/Environment/01/Tree/{tree_image}').convert_alpha()
                scale_ratio_width = TREE_WIDTH / image.get_width()
                scale_ratio_height = TREE_HEIGHT / image.get_height()
                image = pygame.transform.scale(image, ((image.get_width() * scale_ratio_width, image.get_height() * scale_ratio_height)))
                tree_images.append(image)
        self.vegetation_images[TREE] = tree_images
        
        bush_images = list() 
        for bush_image in os.listdir("IMG/Environment/01/Bush"):
            if "bush_" in bush_image:
                image = pygame.image.load(f'IMG/Environment/01/Bush/{bush_image}').convert_alpha()
                scale_ratio_width = BUSH_WIDTH / image.get_width()
                scale_ratio_height = BUSH_HEIGHT / image.get_height()
                image = pygame.transform.scale(image, ((image.get_width() * scale_ratio_width, image.get_height() * scale_ratio_height)))
                bush_images.append(image)
        self.vegetation_images[BUSH] = bush_images

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