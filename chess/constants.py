import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
FPS = 30    # sets a constant FPS that the game will run at
WIN = pygame.display.set_mode((WIDTH + 700, HEIGHT))    # sets the window size

#defining colors in RGB
BLACK = (5, 5, 30)
WHITE = (200, 250, 250)
CYAN = (82, 15, 15)
YELLOW = (244, 180, 27)

ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
NUM = [1, 2, 3, 4, 5, 6, 7, 8]

# defines the grid as a 2D list
BLANKGRID = []
for col in ALPHA:
    for row in range(1, 9):
        BLANKGRID.append([col, row])

GW = [[], [], [], []] # bottom half of board, for white
GB = [[], [], [], []] # top half of board, for black

# maps parts of blankgrid to each half
for i in range(len(BLANKGRID)): 
    if BLANKGRID[i][1] == 1:
        GW[0].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 2:
        GW[1].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 3:
        GW[2].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 4:
        GW[3].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 5:
        GB[3].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 6:
        GB[2].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 7:
        GB[1].append(BLANKGRID[i])
    elif BLANKGRID[i][1] == 8:
        GB[0].append(BLANKGRID[i])