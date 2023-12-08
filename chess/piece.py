import pygame
import random
from .constants import BLACK, WIN, GB, GW, ALPHA, GRID, BLANKGRID

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
            if self.color == BLACK:
                self.direction = 1
            else:
                self.direction = -1
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
    '''will reset the board depending on the level'''
    #first delete all previous pieces
    kings.empty()
    knights.empty()
    bishops.empty()
    rooks.empty()
    queens.empty()
    pawns.empty()
    global GRID 
    GRID = []
    for col in ALPHA:
        for row in range(1, 9):
            GRID.append([col, row])
    
    print(GRID)
    print()
    #print(BLANKGRID)
    global GW
    global GB
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
    
    black_material = 20 + (6 * win_streak)
    white_material = 20 + (3 * win_streak)
    create_side('black', black_material)
    create_side('white', white_material)
    print()
    print()
    print(GRID)

def picksquare(color):
    '''picks an available square, then removes that square from future available squares'''
    if color == 'white':
        rows = GW
    else:
        rows = GB
    chosen =  False
    row = 0
    print(rows)
    while len(rows[row]) == 0:
        row += 1
    #print(rows[row])
    #print(f'row = {row}')
    while chosen == False: 
        choice = random.choices(rows[row])
        #print(f'choice square = {choice}')

        if choice[0] in GRID and len(choice[0]) == 2:
            rows[row].remove(choice[0])
            chosen = True
        else:
            rows[row].remove(choice[0])
        #implement later, when all possible spots are full ignore any attempts to create extra pieces
    return choice

def convertcoords(piece_square):
    '''takes the chess square the piece is on and converts it into xy coordinates'''
    x_og = ALPHA.index(piece_square[0][0])
    y_og = piece_square[0][1]

    pos_x = (x_og * 100) + 350 + 10
    pos_y = (800 - (y_og * 100)) + 10
    return pos_x, pos_y

def append_available(taken_square, piece):
    '''adds object to the grid'''
    global GRID
    x = GRID.index(taken_square)
    GRID[x] += [piece]

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
    global GRID
    
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
