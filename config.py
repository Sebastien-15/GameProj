from tilemap import *
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255,192,203)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
GRAY = (192,192,192)
BG_COLORS = [(193, 149, 77)]
BLACK_2 = (0, 0, 0, 25)

WIN_HEIGHT = 720
WIN_WIDTH = 1280
FPS = 120
BLOCK_WIDTH = 40
BLOCK_HEIGHT = 40

TREE = 0
TREE_WIDTH = 480
TREE_HEIGHT = 768

BUSH = 1
BUSH_WIDTH = 200
BUSH_HEIGHT = 320

FLOWER = 2

PLAYER_LAYER = 3
PLAYER_SPEED = 5
WALKTHROUGH_LAYER = 2
BLOCK_LAYER = 4
BACKGROUND_LAYER = 3
# tilemap = grid
tilemap = [
    'b...............................................',
    '................................lgr.............',
    '................................ukd.............',
    '................................................',
    '..................yvhj..........................',
    '............................................g....',
    '..........c.............................t..g.....',
    '................p.......]...e............g............................................................',
    '.............lgcggrgggglggggggg..ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg......................',
    '............lawwwwfssssahkkkkkk...................',
    '...........lyawwwwfssssaf.........gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggw...........',
    '..........lywukkkkdssssud.........................',
    '..........awwwwwwwdssss............................................................................................................................................',
    '..........awwwwwwd.ssss..........w.................................................................................................................................',
    '..........ukkkkkd..lggggggggggggg..............................................................................................................................................',
    '...................ukkkkkkkkkkkkk..................................................gg..gg............................................................................................',
    '...................ukkkkkkkkkkkkk....ggggggggggggggggggggggggggggggggggggggggggggggggggggggg..............................................gg..gg............................................................................................',
]


# class shump():
#     def __init__(self):
#         self.lol = 2
    
#     def print(self):
#         print(self.lol)

# class shump2(shump):
#     def __init__(self):
#         self.o = 2
#         super().__init__()
    
#     def print(self):
#         print(self.lol * 5)
        
# c = shump()
# d = shump2()
# d.print()
# c.print()
