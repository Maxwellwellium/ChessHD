import pygame
import random
from .constants import WIN, GB, GW, ALPHA, BLANKGRID
import copy

# superclass for all pieces
# piece is a subclass of pygame's Sprite class, which allows extra functionality
class Piece(pygame.sprite.Sprite):
    def __init__(self, x, y, square, color, image):
        super().__init__()
        self.x = x  # actual x coordinate within the window
        self.y = y  # actual y coordinate within the window
        self.square = square    # the square the piece is on
        self.color = color  # whether the piece is white or black
        self.image = image  # the png it uses when bliting
        self.rect = None

    def __repr__(self):
        return str(self.color)
    
class Pawn(Piece):
        def __init__(self, x, y, square, color, image):
            super().__init__(x, y, square, color, image)
            
            # determines the direction pawns are allowed to move in depending on their color
            if self.color == 'black':
                self.direction = -1
            if self.color == 'white':
                self.direction = 1

            # determines if the pawn can move forward two squares
            self.untouched = True

            # not implemented but this on the first & last ranks, pawns should promote

        def __repr__(self):
            return str(self.color) + ' pawn'

# All other subclasses act the same
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

# each variable becomes a list holding all of one type of piece   
kings = pygame.sprite.Group()
knights = pygame.sprite.Group() 
bishops = pygame.sprite.Group() 
rooks = pygame.sprite.Group() 
queens = pygame.sprite.Group()
pawns = pygame.sprite.Group() 


def set_board(win_streak):
    '''Wipes the board and regenerates it with material dependent on winstreak'''
    #Delete all previous pieces
    kings.empty()
    knights.empty()
    bishops.empty()
    rooks.empty()
    queens.empty()
    pawns.empty()

    #Redefine global variables as a clear board
    global CURRENT_GRID 
    CURRENT_GRID = copy.deepcopy(BLANKGRID)
    global blackrows
    blackrows = copy.deepcopy(GB)
    global whiterows
    whiterows = copy.deepcopy(GW)
    
    # populate clear board with pieces
    # normal chess has a material of 39 per side
    black_material = 20 + (6 * win_streak)
    white_material = 20 + (3 * win_streak)
    bm = create_side('black', black_material)
    wm = create_side('white', white_material)

    # bm & wm are returned to accurately see how much material was generated for each side*
    # * = up until there are so many pieces generated that extras are deleted
    return CURRENT_GRID, bm, wm

def picksquare(color):
    '''Picks an available square, then removes that square from future available squares'''
    # use correct spawning list depending on piece color
    global whiterows
    global blackrows
    if color == 'white':
        rows = whiterows
    else:
        rows = blackrows
    
    # Fills up the back rows first, once they are full, they will spawn on the next row etc...
    row = 0
    try:
        while len(rows[row]) == 0:
            row += 1
    except IndexError:  # when there are no more spots left to generate pieces, ignore extras
        choice = None
        return choice

    #continuously tries to pick a square until it is successful
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
    return choice

def convertcoords(piece_square):
    '''takes the chess square a piece is on and converts it into xy coordinates'''
    x_og = ALPHA.index(piece_square[0][0])
    y_og = piece_square[0][1]

    pos_x = (x_og * 100) + 350 + 10
    pos_y = (800 - (y_og * 100)) + 10
    return pos_x, pos_y

def append_available(taken_square, piece):
    '''adds piece to the current grid at its square'''
    global CURRENT_GRID
    x = CURRENT_GRID.index(taken_square)
    CURRENT_GRID[x] += [piece]

def create_k(color):
    '''creates the king, this is done first to ensure the king is generated on the back row'''
    king_spawn = picksquare(color)
    pos_x, pos_y = convertcoords(king_spawn)
    king = King(pos_x, pos_y, king_spawn, color, f'{str(color).lower()}_king.png')
    append_available(king_spawn[0], king)
    kings.add(king)

def create(piece, color):
    piece_spawn = picksquare(color)
    pos_x, pos_y = convertcoords(piece_spawn)
    global CURRENT_GRID
    
    # all pieces are placed the same
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
    '''generates pawns on the board, this is done last to ensure pawns are infront of other pieces'''
    pawn_spawn = picksquare(color)
    if pawn_spawn != None:
        pos_x, pos_y = convertcoords(pawn_spawn)
        pawn = Pawn(pos_x, pos_y, pawn_spawn, color, f'{str(color).lower()}_pawn.png')
        pawns.add(pawn)
        append_available(pawn_spawn[0], pawn)

def draw_pieces():
    '''actually draws the sprites onto the screen for every piece'''
    # the code is the same for all pieces
    for king in kings:
        pos_x = getattr(king, 'x')
        pos_y = getattr(king, 'y')
        color = getattr(king, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_king.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        king.rect = piece_image.get_rect()
        WIN.blit(piece_image, (pos_x, pos_y))
        # black king is a bald version of me

    for knight in knights:
        pos_x = getattr(knight, 'x')
        pos_y = getattr(knight, 'y')
        color = getattr(knight, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_knight.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        knight.rect = piece_image.get_rect()
        WIN.blit(piece_image, (pos_x, pos_y))
        # black knight is a horse of unknown origin

    for bishop in bishops:
        pos_x = getattr(bishop, 'x')
        pos_y = getattr(bishop, 'y')
        color = getattr(bishop, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_bishop.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))
        # black bishop is Bishop Doug Fischer of the Episcopal Diocese of Western Massachusetts

    for rook in rooks:
        pos_x = getattr(rook, 'x')
        pos_y = getattr(rook, 'y')
        color = getattr(rook, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_rook.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))
        # black rook is a castle of unknown origin

    for queen in queens:
        pos_x = getattr(queen, 'x')
        pos_y = getattr(queen, 'y')
        color = getattr(queen, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_queen.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))
        # black queen is that one girl from queens gambit

    for pawn in pawns:
        pos_x = getattr(pawn, 'x')
        pos_y = getattr(pawn, 'y')
        color = getattr(pawn, 'color')
        raw_image = pygame.image.load(f'{str(color).lower()}_pawn.png').convert()
        piece_image = pygame.transform.scale(raw_image, (80, 80))
        WIN.blit(piece_image, (pos_x, pos_y))
        # black pawn is Rick Harrison of Pawn Stars

def create_side(color, amount):
    '''generates every piece for the black side until piece values exceed amount given'''
    create_k(color)
    piece_list = []
    pawn_list = []
    total = 0
    while total < amount:

        # pieces are mapped to their real-chess value equivalent
        worth = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9}
        # randomly chooses a piece based of its weight
        z = random.choices(list(worth.items()), weights = [50, 15, 15, 12, 8])
        
        # appends piece to correct list depending on if its a pawn or not
        if z[0][0] == 'pawn':
            pawn_list.append(z[0][0])
        else:
            piece_list.append(z[0][0])

        # adds piece value to total to break while loop
        total += z[0][1]

    # print(f'pieces: {piece_list}')
    # print(f'pawns: {pawn_list}')

    # generates an actual piece/pawn for every piece in its list
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
            WIN.blit(gamewon, (0, 0))   #draws the game won screen    
            # WIN.blit(newround, (0, 0))
        
            winstreak += 1
            print('game won')
        else:
            gamelost = pygame.image.load(f'gamelost.png').convert_alpha()
            gamelost = pygame.transform.scale(gamelost, (1500, 800))
            WIN.blit(gamelost, (0, 0))  #draws the game lost screen
            
            winstreak = 0   # reset winstreak
            print('game lost')
        
        # not implemented but any screens that appear after a game is over should stay on screen for a longer amount of time

        over = True # signals that game is over
    return over, winstreak