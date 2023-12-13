import pygame
import random
from .constants import BLACK, WIN, GB, GW, ALPHA, BLANKGRID
import copy

class Piece(pygame.sprite.Sprite):
    def __init__(self, x, y, square, color, image):
        super().__init__()
        self.x = x
        self.y = y
        self.square = square
        self.color = color
        self.image = image
        self.rect = None

    def __repr__(self):
        return str(self.color)
    
class Pawn(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)
            if self.color == 'black':
                self.direction = -1
            if self.color == 'white':
                self.direction = 1
            self.untouched = True
        def __repr__(self):
            return str(self.color) + ' pawn'
class Knight(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)
        
        def __repr__(self):
            return str(self.color) + ' knight'
class Bishop(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)
        
        def __repr__(self):
            return str(self.color) + ' bishop'
class Rook(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)
        
        def __repr__(self):
            return str(self.color) + ' rook'
class Queen(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)
        
        def __repr__(self):
            return str(self.color) + ' queen'
class King(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)

        def __repr__(self):
            return str(self.color) + ' king'
        
kings = pygame.sprite.Group()
knights = pygame.sprite.Group() 
bishops = pygame.sprite.Group() 
rooks = pygame.sprite.Group() 
queens = pygame.sprite.Group()
pawns = pygame.sprite.Group() 

def set_board(win_streak):
    '''Resets the board, with material dependent on winstreak'''
    #Delete all previous pieces
    kings.empty()
    knights.empty()
    bishops.empty()
    rooks.empty()
    queens.empty()
    pawns.empty()

    #Redefine global variables as clear board
    global CURRENT_GRID 
    CURRENT_GRID = copy.deepcopy(BLANKGRID)
    global blackrows
    blackrows = copy.deepcopy(GB)
    global whiterows
    whiterows = copy.deepcopy(GW)
    # print(f'setboard 1st grid: {CURRENT_GRID}')
    
    #Populate clear board with pieces
    black_material = 20 + (6 * win_streak)
    white_material = 20 + (3 * win_streak)
    bm = create_side('black', black_material)
    wm = create_side('white', white_material)
    # print()
    # print(f'setboard 2nd grid: {CURRENT_GRID}')

    return CURRENT_GRID, bm, wm

def picksquare(color):
    '''Picks an available square, then removes that square from future available squares'''
    #use correct spawning list depending on piece color
    global whiterows
    global blackrows
    if color == 'white':
        rows = whiterows
    else:
        rows = blackrows
    
    #Fills up the back rows first, once they are full, they will spawn on the next row etc...
    row = 0
    while len(rows[row]) == 0:
        row += 1
    # print(f'rows: {rows}')
    # print(f'grid black: {GB}')
    # print(rows[row])
    # print(f'row = {row}')

    #If first spawn fails, will continue to attempt until successful
    chosen =  False
    while chosen == False: 
        choice = random.choices(rows[row])
        # print(f'choice square = {choice}')

        #checks if square exists and is available
        if choice[0] in CURRENT_GRID and len(choice[0]) == 2:
            rows[row].remove(choice[0])
            chosen = True
        else:
            rows[row].remove(choice[0])
        #implement later, when all possible spots are full ignore any attempts to create extra pieces
    
    return choice

def convertcoords(piece_square):
    '''takes the chess square a piece is on and converts it into xy coordinates'''
    x_og = ALPHA.index(piece_square[0][0])
    y_og = piece_square[0][1]

    pos_x = (x_og * 100) + 350 + 10
    pos_y = (800 - (y_og * 100)) + 10
    return pos_x, pos_y

def append_available(taken_square, piece):
    '''adds piece to the grid at its square'''
    global CURRENT_GRID
    x = CURRENT_GRID.index(taken_square)
    CURRENT_GRID[x] += [piece]

def create_k(color):
    '''creates the king, places it on the board and deletes the taken square from available spawning squares'''
    king_spawn = picksquare(color)
    pos_x, pos_y = convertcoords(king_spawn)
    king = King(pos_x, pos_y, king_spawn, color, f'{str(color).lower()}_king.png')
    append_available(king_spawn[0], king)
    kings.add(king)

def create(piece, color):
    piece_spawn = picksquare(color)
    pos_x, pos_y = convertcoords(piece_spawn)
    global CURRENT_GRID
    
    if piece == 'knight':
        piece = Knight(pos_x, pos_y, piece_spawn, color, f'{str(color).lower()}_knight.png')
        knights.add(piece)
        append_available(piece_spawn[0], piece)

    elif piece == 'bishop':
        piece = Bishop(pos_x, pos_y, piece_spawn, color, f'{str(color).lower()}_bishop.png')
        bishops.add(piece)
        append_available(piece_spawn[0], piece)

    elif piece == 'rook':
        piece = Rook(pos_x, pos_y, piece_spawn, color, f'{str(color).lower()}_rook.png')
        rooks.add(piece)
        append_available(piece_spawn[0], piece)

    elif piece == 'queen':
        piece = Queen(pos_x, pos_y, piece_spawn, color, f'{str(color).lower()}_queen.png')
        queens.add(piece)
        append_available(piece_spawn[0], piece)

def create_p(color):
    pawn_spawn = picksquare(color)
    pos_x, pos_y = convertcoords(pawn_spawn)
    pawn = Pawn(pos_x, pos_y, pawn_spawn, color, f'{str(color).lower()}_pawn.png')
    pawns.add(pawn)
    append_available(pawn_spawn[0], pawn)

def draw_pieces():
    '''actually draws the sprite onto the screen for every piece'''
    for king in kings:
        pos_x = getattr(king, 'x')
        pos_y = getattr(king, 'y')
        color = getattr(king, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_king.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        king.rect = piece_image.get_rect()
        WIN.blit(piece_image, (pos_x, pos_y))

    for knight in knights:
        pos_x = getattr(knight, 'x')
        pos_y = getattr(knight, 'y')
        color = getattr(knight, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_knight.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        knight.rect = piece_image.get_rect()
        WIN.blit(piece_image, (pos_x, pos_y))

    for bishop in bishops:
        pos_x = getattr(bishop, 'x')
        pos_y = getattr(bishop, 'y')
        color = getattr(bishop, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_bishop.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))

    for rook in rooks:
        pos_x = getattr(rook, 'x')
        pos_y = getattr(rook, 'y')
        color = getattr(rook, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_rook.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))

    for queen in queens:
        pos_x = getattr(queen, 'x')
        pos_y = getattr(queen, 'y')
        color = getattr(queen, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_queen.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))

    for pawn in pawns:
        pos_x = getattr(pawn, 'x')
        pos_y = getattr(pawn, 'y')
        color = getattr(pawn, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_pawn.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))

def create_side(color, amount):
    '''generates every piece for the black side until piece values exceed amount given'''
    create_k(color)
    piece_list = []
    pawn_list = []
    total = 0
    while total < amount:
        worth = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9}
        z = random.choices(list(worth.items()), weights = [50, 15, 15, 12, 8])
        
        if z[0][0] == 'pawn':
            pawn_list.append(z[0][0])
        else:
            piece_list.append(z[0][0])
        total += z[0][1]
    print(f'pieces: {piece_list}')
    print(f'pawns: {pawn_list}')
    for piece in piece_list:
        create(piece, color)
    for pawn in pawn_list:
        create_p(color)
        return total

def game_over(winstreak):
    '''test'''
    kingleft = []

    over = False
    for king in kings:
        color = getattr(king, 'color')
        kingleft.append(color)
    if len(kingleft) == 1:
        if kingleft[0] == 'white':
            gamewon = pygame.image.load(f'enemylegiondefeated.png').convert_alpha()
            gamewon = pygame.transform.scale(gamewon, (1500, 800))
            newround = pygame.image.load(f'newround.png').convert_alpha()
            newround = pygame.transform.scale(newround, (1500, 800))
            # x = 150
            # while x > 0:
            WIN.blit(gamewon, (0, 0))
                # pygame.time.wait(500)
                # x -= 1
            # y = 150
            # while y > 0:
            WIN.blit(newround, (0, 0))
                # pygame.time.wait(500)
                # y -= 1
            winstreak += 1
            print('game won')
        else:
            gamelost = pygame.image.load(f'gamelost.png').convert_alpha()
            gamelost = pygame.transform.scale(gamelost, (1500, 800))
            # z = 150
            # while z > 0:
            WIN.blit(gamelost, (0, 0))
                # z -= 1
            winstreak = 0
            print('game lost')
        over = True
    return over, winstreak