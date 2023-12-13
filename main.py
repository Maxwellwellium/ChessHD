import pygame
import copy
import random
from chess.constants import YELLOW, ALPHA, NUM, WIN, FPS, BLANKGRID
from chess.board import Board, Button
from chess.piece import King, Pawn, Bishop, Knight, Rook, Queen, draw_pieces, set_board, convertcoords, game_over

# modifies the game window's title and icon
pygame.display.set_caption('ChessHD')
icon = pygame.image.load('black_king.png')
pygame.display.set_icon(icon)

def cursor_coordinates():
    '''takes the coordinates of the cursor while its on the grid, and returns the file, rank and square its over'''
    pos_x, pos_y = pygame.mouse.get_pos()
    if pos_x > 350 and pos_x < 1150 and pos_y > 0:    # ignores if the mouse isn't over the board
        coord_x = int(((pos_x - 350) / 100))    # converts x position to its corresponding file
        coord_y = int(8 - (pos_y / 100))    # converts y position to its corresponding rank
        z = [ALPHA[coord_x], coord_y + 1]   # combines x & y to form the actual square
        return coord_x, coord_y, z
    
def print_coords(x, y, z):
        '''Prints the specific square both on the square itself, and off to the side'''
        pos_x, pos_y = pygame.mouse.get_pos()
        if pos_x > 350 and pos_x < 1150 and pos_y > 0:  # ignores if the mouse isn't over the board
            font = pygame.font.Font(None, 30)   # initialize the font
            chess_coord = font.render(f'Square: {z[0] + str(z[1])}', True, YELLOW)
            WIN.blit(chess_coord, (1200, 750))  # prints square off to the side
            WIN.blit(font.render(f'{z[0] + str(z[1])}', True, YELLOW), (x * 100 + 352, 702 - y * 100))  # prints square on itself
            return z

def print_info(winstreak, bm, wm):
    '''prints all up to date relevant info on the left side of the screen'''
    font = pygame.font.Font(None, 30)   # initialize the font
    # reference all relevant global variables
    global currentsquare
    global legalmoves
    global whiteturn
    global choosingpiece

    offset = 50  # used to offset all the text
    length = len(legalmoves) # used to find the amount of legal moves there are

    # extra variables for if there are a lot of legal moves
    var6 = None
    var7 = None
    var8 = None
    var9 = None
    var10 = None
    var11 = None
    var12 = None

    # determines whose turn it is and references the accurate message
    if whiteturn == True:
        var1 = font.render(f'White to Move', True, YELLOW) 
    else:
        var1 = font.render(f'Black to Move', True, YELLOW)

    # determines if a piece has been chosen to move, 
    if choosingpiece == None:
        var2 = font.render(f'Piece Not Selected', True, YELLOW)
    else:
        var2 = font.render(f'Moving {choosingpiece} on {currentsquare}', True, YELLOW)
        # if a piece has been chosen to move, print all of its legal moves on different lines to avoid them not showing up
        # 'There has to be a better way of doing this' - Confucius 
        if length < 3:
            var6 = font.render(f'Legal Moves: {legalmoves[0: 2]}', True, YELLOW)
        elif length < 7:
            var6 = font.render(f'Legal Moves: {legalmoves[0:2]}', True, YELLOW)
            var7 = font.render(f'{legalmoves[2:6]}', True, YELLOW)
        elif length < 11:
            var6 = font.render(f'Legal Moves: {legalmoves[0:2]}', True, YELLOW)
            var7 = font.render(f'{legalmoves[2:6]}', True, YELLOW)
            var8 = font.render(f'{legalmoves[6:10]}', True, YELLOW)
        elif length < 15:
            var6 = font.render(f'Legal Moves: {legalmoves[0:2]}', True, YELLOW)
            var7 = font.render(f'{legalmoves[2:6]}', True, YELLOW)
            var8 = font.render(f'{legalmoves[6:10]}', True, YELLOW)
            var9 = font.render(f'{legalmoves[10:14]}', True, YELLOW)
        elif length < 19:
            var6 = font.render(f'Legal Moves: {legalmoves[0:2]}', True, YELLOW)
            var7 = font.render(f'{legalmoves[2:6]}', True, YELLOW)
            var8 = font.render(f'{legalmoves[6:10]}', True, YELLOW)
            var9 = font.render(f'{legalmoves[10:14]}', True, YELLOW)
            var10 = font.render(f'{legalmoves[14:18]}', True, YELLOW)
        elif length < 23:
            var6 = font.render(f'Legal Moves: {legalmoves[0:2]}', True, YELLOW)
            var7 = font.render(f'{legalmoves[2:6]}', True, YELLOW)
            var8 = font.render(f'{legalmoves[6:10]}', True, YELLOW)
            var9 = font.render(f'{legalmoves[10:14]}', True, YELLOW)
            var10 = font.render(f'{legalmoves[14:18]}', True, YELLOW)
            var11 = font.render(f'{legalmoves[18:22]}', True, YELLOW)
        else:
            var6 = font.render(f'Legal Moves: {legalmoves[0:2]}', True, YELLOW)
            var7 = font.render(f'{legalmoves[2:6]}', True, YELLOW)
            var8 = font.render(f'{legalmoves[6:10]}', True, YELLOW)
            var9 = font.render(f'{legalmoves[10:14]}', True, YELLOW)
            var10 = font.render(f'{legalmoves[14:18]}', True, YELLOW)
            var11 = font.render(f'{legalmoves[18:22]}', True, YELLOW)
            var12 = font.render(f'{legalmoves[22:]}', True, YELLOW)
    
    # determines if there is a winstreak and references the accurate message
    if winstreak == 0:
        var3 = font.render(f'No Winstreak', True, YELLOW)
    else:
        var3 = font.render(f'Current Winstreak: {winstreak}', True, YELLOW)   
    # take the total material generated from both sides and references it 
    var4 = font.render(f'Starting Black Material: {bm}', True, YELLOW)
    var5 = font.render(f'Starting White Material: {wm}', True, YELLOW)
    
    # if the extra variables were used, add them to the list of all variables
    extra_vars = [var6, var7, var8, var9, var10, var11, var12]
    variables = [var1, var2, var3, var4, var5]
    for var in extra_vars:
        if var != None:
            variables.append(var)

    #for each variable, display it and offset the next variable by offset amount
    for var in variables:
        WIN.blit(var, (1175, offset))
        offset += 50

def square_select():
    '''detects which square the player has clicked and selects the piece on it if there is one'''
    # reference all relevant global variables
    global square_selected
    global currentsquare
    global legalmoves
    global whiteturn
    global choosingpiece
    pos_x, pos_y = pygame.mouse.get_pos()

    if pos_x > 350 and pos_x < 1150 and pos_y > 0:  # ignores if the mouse isn't over the board
        square_selected = True  # a square has now been selected
        
        # gets the square that was clicked on and makes a copy to reference
        output = cursor_coordinates()
        square = output[2]
        newsquare = square.copy()

        # if the player clicks a square twice, it will deselect the square
        if square_selected == True and currentsquare != None:
            if currentsquare == newsquare:
                # resets variables to when no square is selected
                square_selected == False
                choosingpiece = None
                legalmoves = []
                return None # currentsquare becomes None

        # determines if the player has clicked a piece to move, or clicked to move a piece
        if choosingpiece == None:
            return pick_piece(square)
        else:
            return move_piece(square)

def pick_piece(square):
    '''selects the piece at the clicked square and finds all of its legal moves'''
    # reference all relevant global variables
    global choosingpiece
    newsquare = square.copy()

    # detects whether or not theres a piece at the clicked square
    piece = piece_detect(square)
    if piece != None:
        # determines if it's the piece's turn or not
        piece_color = getattr(piece, 'color')
        if (piece_color == 'white' and whiteturn == True) or (piece_color == 'black' and whiteturn == False):
            legal_moves(piece, square)  # gets all legal moves of the piece 
            choosingpiece = piece   # choosingpiece becomes the piece at the square clicked
            return newsquare
        
def move_piece(square):
    '''checks to see if clicked square is a legal move, or if it unselects the piece'''
    # reference all relevant global variables
    global square_selected
    global currentsquare
    global legalmoves
    global whiteturn
    global choosingpiece

    piecesquare = getattr(choosingpiece, 'square')
    movesound = pygame.mixer.Sound('move.wav')  # initialize sound
    print(f"the piece is at {piecesquare} and plans to move to {square}")

    # unselects the piece if player clicks the same square twice in a row
    if square == piecesquare[0]:
        square_selected = False
        currentsquare = None
        choosingpiece = None
    # for when a legal move is made
    elif square in legalmoves:
        print(f'{choosingpiece} moved to {square}')

        # troubleshooting solution for whether or not piecesquare was a list, or a list in a list
        proper = isinstance(piecesquare[0], list)
        if proper == True:
            properpiecesquare = piecesquare[0]
        else:
            properpiecesquare = piecesquare

        moveupdate(properpiecesquare, square)   #this function actually updates the grid and peices of the move made

        # updates global variables to reflect a move being made
        whiteturn = not whiteturn
        square_selected = False
        currentsquare = None
        choosingpiece = None
        pygame.mixer.Sound.play(movesound)  #plays soundeffect everytime a piece moves
    else:
        print(f'████ ILLEGAL MOVE ████')    # nothing happens if an illegal move is attempted
    return square

def moveupdate(piecesquare, square):
    '''updates the grid, and objects involved in the actual move'''
    # reference all relevant global variables
    global choosingpiece
    global CURRENT_GRID
    global BLANKGRID

    # print(f'GRID BEFORE UPDATING = {CURRENT_GRID}')
    # print(f'piecesquare is {piecesquare}')

    # gets the indexs of the squares of both the piece being moved, and the spot its moving to, and references a copy of that
    moved_index = copy.deepcopy(BLANKGRID.index(piecesquare))
    cap_index = copy.deepcopy(BLANKGRID.index(square))
    # print(f'moved index = {moved_index}, captured index = {cap_index}')

    # updates the attributes of the choosingpiece to reflect the square it has moved to
    setattr(choosingpiece, 'square', square)
    z = [square]
    pos_x, pos_y = convertcoords(z)
    setattr(choosingpiece, 'x', pos_x)
    setattr(choosingpiece, 'y', pos_y)

    # prevents pawns from moving forward 2 squares after being moved
    if choosingpiece.__class__ == Pawn:
        untouched = getattr(choosingpiece, 'untouched')
        if untouched == True:
            setattr(choosingpiece, 'untouched', False)

    # updates current grid to reflect that there is no piece at the old square
    CURRENT_GRID[moved_index] = copy.deepcopy(BLANKGRID[moved_index])

    # initialize sounds 
    sound1 = pygame.mixer.Sound('captured.mp3')
    sound2 = pygame.mixer.Sound('horse1.mp3')
    sound3 = pygame.mixer.Sound('horse2.mp3')
    sound4 = pygame.mixer.Sound('king.mp3')

    # detects whether there is a piece at the new square
    captured_piece = piece_detect(square)
    if captured_piece != None:
        print(f'{captured_piece} WAS CAPTURED')

        # detects what type of piece was captured, and plays the corect sound
        if captured_piece.__class__ == Knight:
            x = random.choice([sound2, sound3])
            pygame.mixer.Sound.play(x)
        elif captured_piece.__class__ == King:
            pygame.mixer.Sound.play(sound4)
        else:
            pygame.mixer.Sound.play(sound1)
        CURRENT_GRID[cap_index][2] = (choosingpiece)    #changes grid to reflect the new piece
        pygame.sprite.Sprite.kill(captured_piece)   #kills the old piece to prevent lag
    else:
        CURRENT_GRID[cap_index].append(choosingpiece)   #changes grid to reflect the new piece

    #print(f'GRID AFTER UPDATING = {CURRENT_GRID}')

def legal_moves(piece, square):
    '''finds all legal moves for a piece and returns them as a list'''
    # establish relevant variables
    allmoves = []
    global legalmoves
    legalmoves = []
    file, rank = square

    # ███████████████ PAWN MOVEMENT ███████████████
    if piece.__class__ == Pawn:
        print(f'Pawn at {square}')

        # gets attributes specific to pawns
        untouched = getattr(piece, 'untouched')
        direction = getattr(piece, 'direction')
        print(f'unmoved?: {untouched}')

        # ████ FORWARD MOVEMENT ████ 
        # the square directly infront of the pawn
        if (rank + direction) in NUM:
            allmoves.append([file, (rank + direction)])

        # ████ FIRST MOVE MOVEMENT ████ 
        # allows the pawn to move forward 2 squares on its first turn
        if untouched == True:
            allmoves.append([file, (rank + (2*direction))])

        # only adds unoccupied pieces to legal moves
        for move in allmoves:
            captured = piece_detect(move)
            if captured == None:  # for when there's no piece
                legalmoves.append(move)

        # ████ CAPTURE MOVEMENT ████ 
        # detects if there are pieces diagonally infront of it, if so then the pawn can capture them
        pawncapturespots = []
        index = ALPHA.index(file)
        if index != 0:
            pawncapturespots.append([ALPHA[index-1], (rank + direction)])
        if index != 7:
            pawncapturespots.append([ALPHA[index+1], (rank + direction)])
        for move in pawncapturespots:
            captured = piece_detect(move)
            if captured != None:
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)

    # ███████████████ KNIGHT MOVEMENT ███████████████
    elif piece.__class__ == Knight:
        print(f'Knight at {square}')
        existing_ranks = []
        existing_files = []
        index = ALPHA.index(file)
        
        # the knight's movement is split into 2 groups
        # the first group is calculated and added, then the variables are cleared, then the second group is calculated and added
        
        # ████ FIRST GROUP MOVEMENT ████ 
        # rank is +-2 and file is +-1
        # checks to see if ranks and files exist, skips them if they dont
        if rank-2 in NUM:
            existing_ranks.append(rank-2)
        if rank+2 in NUM:
            existing_ranks.append(rank+2)
        if index >= 1:
            existing_files.append(ALPHA[index-1])
        if index <= 6:
            existing_files.append(ALPHA[index+1])
        for ranks in existing_ranks:
            for files in existing_files:
                allmoves.append([files, ranks])

        # clears the ranks and files in order to calculate the second group
        existing_ranks.clear()
        existing_files.clear()

        # ████ SECOND GROUP MOVEMENT ████ 
        # rank is +-1 and file is +-2
        # checks to see if ranks and files exist, skips them if they dont
        if rank-1 in NUM:
            existing_ranks.append(rank-1)
        if rank+1 in NUM:
            existing_ranks.append(rank+1)
        if index > 1:
            existing_files.append(ALPHA[index-2])
        if index < 6:
            existing_files.append(ALPHA[index+2])
        for ranks in existing_ranks:
            for files in existing_files:
                allmoves.append([files, ranks])

        # only adds unoccupied pieces to legal moves
        for move in allmoves:
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                # remove squares occupied by the same color
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)

    # ███████████████ BISHOP & QUEEN MOVEMENT ███████████████
    if piece.__class__ == Bishop or piece.__class__ == Queen:
        print(f'Bishop or Queen at {square}')
        
        # The Bishop/Queen checks each direction individually, going out in each one using a for loop until obstructed
        topleft = True
        topright = True
        bottomleft = True
        bottomright = True
        copysquare = copy.deepcopy(square)  #for resetting reference point after a direction is completed
        index = ALPHA.index(file)

        # ████ TOP LEFT MOVEMENT ████ 
        while topleft == True:
            if rank + 1 not in NUM or (index-1) < 0:
                topleft = False
                break
            # every loop it will search the next square of that direction
            move = [ALPHA[index - 1], (rank + 1)]
            rank += 1
            index = (index - 1)

            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

        # ████ TOP RIGHT MOVEMENT ████ 
        while topright == True:
            if rank + 1 not in NUM or (index+1) > 7:
                topright = False
                break
            # every loop it will search the next square of that direction
            move = [ALPHA[index + 1], (rank + 1)]
            rank += 1
            index = (index + 1)

            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

        # ████ BOTTOM LEFT MOVEMENT ████ 
        while bottomleft == True:
            if rank - 1 not in NUM or (index-1) < 0:
                bottomleft = False
                break
            # every loop it will search the next square of that direction
            move = [ALPHA[index - 1], (rank - 1)]
            rank -= 1
            index = (index - 1)

            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        
        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

        # ████ BOTTOM RIGHT MOVEMENT ████ 
        while bottomright == True:
            if rank - 1 not in NUM or (index+1) > 7:
                bottomright = False
                break
            # every loop it will search the next square of that direction
            move = [ALPHA[index + 1], (rank - 1)]
            rank -= 1
            index = (index + 1)

            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)
    
    # ███████████████ ROOK & QUEEN MOVEMENT ███████████████
    if piece.__class__ == Rook or piece.__class__ == Queen:
        print(f'Rook or Queen at {square}')
        
        # The Rook/Queen checks each direction individually, going out in each one using a for loop until obstructed
        up = True
        down = True
        left = True
        right = True
        copysquare = copy.deepcopy(square)  #for resetting reference point after a direction is completed
        index = ALPHA.index(file)

        # ████ UP MOVEMENT ████ 
        while up == True:
            if rank + 1 not in NUM:
                up = False
                break
            move = [ALPHA[index], (rank + 1)]
            rank += 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

        # ████ DOWN MOVEMENT ████ 
        while down == True:
            if rank - 1 not in NUM:
                down = False
                break
            move = [ALPHA[index], (rank - 1)]
            rank -= 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

        # ████ LEFT MOVEMENT ████ 
        while left == True:
            if index <= 0:
                left = False
                break
            move = [ALPHA[index-1], (rank)]
            index -= 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

        # ████ RIGHT MOVEMENT ████ 
        while right == True:
            if index >= 7:
                right = False
                break
            move = [ALPHA[index+1], (rank)]
            index += 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            # if a piece is detected, it stops continuing in that direction
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break

        # reset variables
        file, rank = copysquare
        index = ALPHA.index(file)

    # ███████████████ KING MOVEMENT ███████████████
    elif piece.__class__ == King:
        print(f'King at {square}')
        
        # checks to see if ranks exist, skips them if they dont
        existing_ranks = [rank]
        if rank-1 in NUM:
            existing_ranks.append(rank-1)
        if rank+1 in NUM:
            existing_ranks.append(rank+1)

        # checks to see if files exist, skips them if they dont
        existing_files = [file]
        index = ALPHA.index(file)
        if index != 0:
            existing_files.append(ALPHA[index-1])
        if index != 7:
            existing_files.append(ALPHA[index+1])

        # loops through to create all squares that exist on the board and adds them to all moves list
        for ranks in existing_ranks:
            for files in existing_files:
                allmoves.append([files, ranks])

        # removes the square the king is currently on
        allmoves.remove([file, rank])
        
        # removes moves from list if there is a piece on the same team
        for move in allmoves:
            captured = piece_detect(move)
            if captured == None: # for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)

    print(f'legalmoves: {legalmoves}')
    return legalmoves

def draw_select_overlay(square):
    '''draws the select overlay image over the selected square'''
    x_og = ALPHA.index(square[0])
    y_og = square[1]
    pos_x = (x_og * 100) + 350
    pos_y = (800 - (y_og * 100))
    raw_image = pygame.image.load(f'select_overlay.png').convert_alpha()
    piece_image = pygame.transform.scale(raw_image, (100, 100))
    WIN.blit(piece_image, (pos_x, pos_y))

def draw_legal_overlay(legalmoves):
    '''draws the legal overlay over squares that are legal moves'''
    for move in legalmoves:
        x_og = ALPHA.index(move[0])
        y_og = move[1]
        pos_x = (x_og * 100) + 350
        pos_y = (800 - (y_og * 100))
        raw_image = pygame.image.load(f'legalmove.png').convert_alpha()
        piece_image = pygame.transform.scale(raw_image, (100, 100))
        WIN.blit(piece_image, (pos_x, pos_y))

def piece_detect(square):
        '''detects if there is a piece on any given square'''
        # Finds index of square in grid, then uses that index to access square in current grid to see if theres a piece
        global CURRENT_GRID
        index = copy.deepcopy(BLANKGRID.index(square))
        if len(CURRENT_GRID[index]) == 3:
            print('piece found')
            return CURRENT_GRID[index][2]
        else:
            print('no piece')
            return None  

# create instances of buttons
restart_button = Button(50, 50, 1.25, 'restart')
instructions_button = Button(50, 250, 1.25, 'instructions')

# the actual main loop
def main():
    pygame.init()   #initializes pygame
    pygame.mixer.init() # initializes pygame music
    pygame.font.init()  # initializes pygame fonts
    run = True
    clock = pygame.time.Clock()
    board = Board() #creates the board

    # initially defines all relevant global variables
    global CURRENT_GRID
    CURRENT_GRID, bm, wm = set_board(1) #sets the board initially
    global square_selected
    global currentsquare
    global legalmoves
    global whiteturn
    global choosingpiece

    square_selected = False
    currentsquare = None
    legalmoves = []
    whiteturn = True
    choosingpiece = None
    winstreak = 0

    # background music
    pygame.mixer.music.load('amaski_war_drums.mp3')
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(FPS) # makes game run at stable FPS
        
        # draws board and all buttons
        board.draw_squares(WIN)
        restart_button.draw()
        instructions_button.draw()

        # detects if game is over then automatically resets board with current winstreak difficulty
        over, winstreak = game_over(winstreak)
        if over == True:
            whiteturn = True
            CURRENT_GRID, bm, wm = set_board(winstreak)

        # event handler
        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('███████████████ MOUSE ███████████████')
                pos_x, pos_y = pygame.mouse.get_pos()
                if pos_x > 350 and pos_x < 1150 and pos_y > 0:
                    # selects given square when its clicked
                    currentsquare = square_select()

                if restart_button.rect.collidepoint((pos_x, pos_y)):
                    
                    # was a little too earpiercing to be used
                    # sound = pygame.mixer.Sound('reset.mp3')
                    # pygame.mixer.Sound.play(sound)

                    # resets variables when reset button is clicked
                    CURRENT_GRID, bm, wm = set_board(1)
                    winstreak = 0
                    whiteturn = True
                    restart_button.clicked = True

            # if event.type == pygame.MOUSEBUTTONUP:
            #     pos_x, pos_y = pygame.mouse.get_pos()
            #     if restart_button.clicked == True and restart_button.rect.collidepoint((pos_x, pos_y)):
            #         pass
            #     restart_button.clicked = False

        # draws all pieces and information
        draw_pieces()
        print_info(winstreak, bm, wm)

        # draws select overlay and legal overlays if applicable
        if square_selected == True and currentsquare != None:
            draw_select_overlay(currentsquare)
        if choosingpiece != None:
            draw_legal_overlay(legalmoves)

        # draws cursor coordinates if applicable
        res = cursor_coordinates()
        if res:
            x, y, z = res
            print_coords(x, y, z)

        # updates the screen every frame
        pygame.display.update()
    
    # quits pygame when quit
    pygame.quit()
    pygame.mixer.quit()







#calling main
main()