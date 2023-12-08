import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

FPS = 30    #sets a constant FPS that the game will run at

WIN = pygame.display.set_mode((WIDTH + 700, HEIGHT))

#defining colors in RGB
BLACK = (10, 10, 40)
WHITE = (200, 250, 250)
CYAN = (48, 84, 84)
YELLOW = (200, 200, 0)

ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

BLANKGRID = []
for col in ALPHA:
    for row in range(1, 9):
        BLANKGRID.append([col, row])
GRID = BLANKGRID.copy()

GW = [[], [], [], []] #bottom half of board
GB = [[], [], [], []] #top half of board

for i in range(len(GRID)): 
    if GRID[i][1] == 1:
        GW[0].append(GRID[i])
    elif GRID[i][1] == 2:
        GW[1].append(GRID[i])
    elif GRID[i][1] == 3:
        GW[2].append(GRID[i])
    elif GRID[i][1] == 4:
        GW[3].append(GRID[i])
    elif GRID[i][1] == 5:
        GB[3].append(GRID[i])
    elif GRID[i][1] == 6:
        GB[2].append(GRID[i])
    elif GRID[i][1] == 7:
        GB[1].append(GRID[i])
    elif GRID[i][1] == 8:
        GB[0].append(GRID[i])