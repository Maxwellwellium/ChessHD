import pygame
import copy
import random
from chess.constants import YELLOW, ALPHA, NUM, WIN, FPS, BLANKGRID
from chess.board import Board, Button
from chess.piece import King, Pawn, Bishop, Knight, Rook, Queen, draw_pieces, set_board, convertcoords

pygame.font.init()  #renders the font
pygame.display.set_caption('ChessHD')

def cursor_coordinates():
    '''gets the coordinates of the cursor, converts them to chess notation'''
    pos_x, pos_y = pygame.mouse.get_pos()
    if pos_x > 350 and pos_x < 1150 and pos_y > 0:    #when the mouse cursor isn't on the board, it shouldn't have coordinates
        coord_x = int(((pos_x - 350) / 100))    #use 350 to offset x
        coord_y = int(8 - (pos_y / 100))
        z = [ALPHA[coord_x], coord_y + 1]
        return coord_x, coord_y, z
    
def print_coords(x, y, z):
        '''prints the chess notation coordinates'''
        pos_x, pos_y = pygame.mouse.get_pos()
        if pos_x > 350 and pos_x < 1150 and pos_y > 0:
            font = pygame.font.Font(None, 30)   #default font, to use different ones must make dif variables
            chess_coord = font.render(f'Square: {z[0] + str(z[1])}', True, YELLOW)
            WIN.blit(chess_coord, (1200, 750))  #prints coords in bottom right corner
            WIN.blit(font.render(f'{z[0] + str(z[1])}', True, YELLOW), (x * 100 + 352, 702 - y * 100))  
            return z
        
def square_select():
    '''detects which square the player has clicked and selects the piece on it if there is one'''
    global square_selected
    global currentsquare
    global legalmoves
    global whiteturn
    global choosingpiece
    pos_x, pos_y = pygame.mouse.get_pos()

    #only executes when player clicks on grid
    if pos_x > 350 and pos_x < 1150 and pos_y > 0:
        square_selected = True
        output = cursor_coordinates()
        square = output[2]
        newsquare = square.copy()

        #For deselecting a square
        if square_selected == True and currentsquare != None:
            print(f'current square: {currentsquare}████ new square: {newsquare}')
            if currentsquare == newsquare:
                square_selected == False
                choosingpiece = None
                legalmoves = []
                return None

        #determines if a piece has been chosen to move, if not it does so
        if choosingpiece == None:
            return pick_piece(square)
        else:
            return move_piece(square)

def pick_piece(square):
    '''picks a piece intended to move'''
    global choosingpiece
    newsquare = square.copy()
    piece = piece_detect(square)
    if piece != None:
        piece_color = getattr(piece, 'color')
        if (piece_color == 'white' and whiteturn == True) or (piece_color == 'black' and whiteturn == False):
            legal_moves(piece, square)
            choosingpiece = piece
            return newsquare
        
def move_piece(square):
    '''will move the selected piece to that spot'''
    global square_selected
    global currentsquare
    global legalmoves
    global whiteturn
    global choosingpiece
    piecesquare = getattr(choosingpiece, 'square')
    movesound = pygame.mixer.Sound('move.wav')
    print(f"piece's square = {piecesquare}████ clicked square = {square}")
    if square == piecesquare[0]:
        square_selected = False
        currentsquare = None
        choosingpiece = None
    elif square in legalmoves:
        print(f'{choosingpiece} moved to {square}')

        proper = isinstance(piecesquare[0], list)
        if proper == True:
            properpiecesquare = piecesquare[0]
        else:
            properpiecesquare = piecesquare

        moveupdate(properpiecesquare, square)

        whiteturn = not whiteturn
        square_selected = False
        currentsquare = None
        choosingpiece = None
        pygame.mixer.Sound.play(movesound)
    else:
        print(f'████ ILLEGAL MOVE ████')

    return square

def moveupdate(piecesquare, square):
    '''updates the grid, and objects involved in the actual move'''
    global choosingpiece
    global CURRENT_GRID
    global BLANKGRID
    print(f'GRID BEFORE UPDATING = {CURRENT_GRID}')
    print(f'████piecesquare is {piecesquare}████')
    moved_index = copy.deepcopy(BLANKGRID.index(piecesquare))
    cap_index = copy.deepcopy(BLANKGRID.index(square))
    print(f'moved index = {moved_index}, captured index = {cap_index}')

    #updates the attributes of the piece moving
    setattr(choosingpiece, 'square', square)
    z = [square]
    pos_x, pos_y = convertcoords(z)
    setattr(choosingpiece, 'x', pos_x)
    setattr(choosingpiece, 'y', pos_y)
    if choosingpiece.__class__ == Pawn:
        untouched = getattr(choosingpiece, 'untouched')
        if untouched == True:
            setattr(choosingpiece, 'untouched', False)

    #updates current grid to show there is no piece at old spot
    CURRENT_GRID[moved_index] = copy.deepcopy(BLANKGRID[moved_index])

    #in the case that the new spot has a piece already there
    captured_piece = piece_detect(square)
    sound1 = pygame.mixer.Sound('captured.mp3')
    sound2 = pygame.mixer.Sound('horse1.mp3')
    sound3 = pygame.mixer.Sound('horse2.mp3')
    sound4 = pygame.mixer.Sound('king.mp3')

    if captured_piece != None:
        print(f'{captured_piece} WAS CAPTURED')
        if captured_piece.__class__ == Knight:
            x = random.choice([sound2, sound3])
            pygame.mixer.Sound.play(x)
        elif captured_piece.__class__ == King:
            pygame.mixer.Sound.play(sound4)
        else:
            pygame.mixer.Sound.play(sound1)
        CURRENT_GRID[cap_index][2] = (choosingpiece)
        pygame.sprite.Sprite.kill(captured_piece)
    else:
        #updates new spot to reference the new piece
        CURRENT_GRID[cap_index].append(choosingpiece)

    print(f'GRID AFTER UPDATING = {CURRENT_GRID}')

def legal_moves(piece, square):
    '''finds all legal moves for a piece and returns them as a list'''
    allmoves = []
    global legalmoves
    legalmoves = []
    file, rank = square

    if piece.__class__ == Pawn:
        print(f'Pawn at {square}')
        untouched = getattr(piece, 'untouched')
        direction = getattr(piece, 'direction')
        print(f'unmoved?: {untouched}')

        if (rank + direction) in NUM:
            allmoves.append([file, (rank + direction)])

        #for pawns moving forward 2 squares on the first turn
        if untouched == True:
            allmoves.append([file, (rank + (2*direction))])

        for move in allmoves:
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)

        #for the squares the pawn can move to when capturing
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


    elif piece.__class__ == Knight:
        print(f'Knight at {square}')
        #checks to see if ranks exist, skips them if they dont
        existing_ranks = []
        existing_files = []
        index = ALPHA.index(file)
        
        #splits horse's movement into 2 squares, with each legal move being a corner (or intersection between a file and rank)
        #this is the first square where rank is +-2 and file is +-1
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
        # print(f'knight moves 1:{allmoves}')

        #clear ranks and files to avoid messing up the next for loops
        existing_ranks.clear()
        existing_files.clear()

        #this is the second square where rank is +-1 and file is +-2
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
        # print(f'knight moves 2:{allmoves}')

        #removes already occupied pieces
        for move in allmoves:
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)

    if piece.__class__ == Bishop or piece.__class__ == Queen:
        print(f'Bishop or Queen at {square}')
        topleft = True
        topright = True
        bottomleft = True
        bottomright = True
        copysquare = copy.deepcopy(square)
        index = ALPHA.index(file)

        #currently one of these for every directions, probably could make it a for loop but idk
        while topleft == True:
            #index = ALPHA.index(file)
            if rank + 1 not in NUM or (index-1) < 0:
                topleft = False
                break

            move = [ALPHA[index - 1], (rank + 1)]
            rank += 1
            index = (index - 1)
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

        while topright == True:
            #index = ALPHA.index(file)
            if rank + 1 not in NUM or (index+1) > 7:
                topright = False
                break

            move = [ALPHA[index + 1], (rank + 1)]
            rank += 1
            index = (index + 1)
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

        while bottomleft == True:
            #index = ALPHA.index(file)
            if rank - 1 not in NUM or (index-1) < 0:
                bottomleft = False
                break

            move = [ALPHA[index - 1], (rank - 1)]
            rank -= 1
            index = (index - 1)
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

        while bottomright == True:
            #index = ALPHA.index(file)
            if rank - 1 not in NUM or (index+1) > 7:
                bottomright = False
                break

            move = [ALPHA[index + 1], (rank - 1)]
            rank -= 1
            index = (index + 1)
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

    if piece.__class__ == Rook or piece.__class__ == Queen:
        print(f'Rook or Queen at {square}')
        up = True
        down = True
        left = True
        right = True
        copysquare = copy.deepcopy(square)
        index = ALPHA.index(file)

        while up == True:
            if rank + 1 not in NUM:
                up = False
                break
            move = [ALPHA[index], (rank + 1)]
            rank += 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

        while down == True:
            if rank - 1 not in NUM:
                down = False
                break
            move = [ALPHA[index], (rank - 1)]
            rank -= 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

        while left == True:
            if index <= 0:
                left = False
                break
            move = [ALPHA[index-1], (rank)]
            index -= 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

        while right == True:
            if index >= 7:
                right = False
                break
            move = [ALPHA[index+1], (rank)]
            index += 1
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
                    break
                else: break
        file, rank = copysquare
        index = ALPHA.index(file)

    elif piece.__class__ == King:
        print(f'King at {square}')
        
        #checks to see if ranks exist, skips them if they dont
        existing_ranks = [rank]
        if rank-1 in NUM:
            existing_ranks.append(rank-1)
        if rank+1 in NUM:
            existing_ranks.append(rank+1)

        #checks to see if files exist, skips them if they dont
        existing_files = [file]
        index = ALPHA.index(file)
        if index != 0:
            existing_files.append(ALPHA[index-1])
        if index != 7:
            existing_files.append(ALPHA[index+1])

        #loops through to create all squares that exist on the board and adds them to all moves list
        for ranks in existing_ranks:
            for files in existing_files:
                allmoves.append([files, ranks])
        #removes the square the king is currently on
        allmoves.remove([file, rank])
        # print(f'all available moves: {allmoves}')
        #this should be enough for the king, since game ends on capture

        #removes moves from list if there is a piece there of the same color
        for move in allmoves:
            captured = piece_detect(move)
            if captured == None: #for when there's no piece
                legalmoves.append(move)
            else: 
                piececolor = getattr(piece, 'color')
                capturedcolor = getattr(captured, 'color')
                if piececolor != capturedcolor:
                    legalmoves.append(move)
    print(f'legalmoves: {legalmoves}')
    return legalmoves

def draw_select_overlay(square):
    '''draws the overlay image over the selected square'''
    x_og = ALPHA.index(square[0])
    y_og = square[1]
    pos_x = (x_og * 100) + 350
    pos_y = (800 - (y_og * 100))
    raw_image = pygame.image.load(f'select_overlay.png').convert_alpha()
    piece_image = pygame.transform.scale(raw_image, (100, 100))
    WIN.blit(piece_image, (pos_x, pos_y))

def draw_legal_overlay(legalmoves):
    for move in legalmoves:
        x_og = ALPHA.index(move[0])
        y_og = move[1]
        pos_x = (x_og * 100) + 350
        pos_y = (800 - (y_og * 100))
        raw_image = pygame.image.load(f'legalmove.png').convert_alpha()
        piece_image = pygame.transform.scale(raw_image, (100, 100))
        WIN.blit(piece_image, (pos_x, pos_y))

def piece_detect(square):
        '''detects if there is a piece on a given square'''
        #Finds index of square in grid, then uses that index to access square in current grid to see if theres a piece
        global CURRENT_GRID
        index = copy.deepcopy(BLANKGRID.index(square))
        # print(index)
        # print(CURRENT_GRID[index])
        if len(CURRENT_GRID[index]) == 3:
            print('piece found')
            return CURRENT_GRID[index][2]
        else:
            print('no piece')
            return None  

restart_button = Button(50, 50, 1.25, 'restart')

def main():
    pygame.init()
    pygame.mixer.init()
    run = True
    clock = pygame.time.Clock()
    board = Board()
    global CURRENT_GRID
    CURRENT_GRID = set_board(1)
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
    pygame.mixer.music.load('amaski_war_drums.mp3')
    pygame.mixer.music.play(-1)
    while run:
        clock.tick(FPS) #makes game run at stable FPS
        board.draw_squares(WIN)
        restart_button.draw()
        
        #event handler
        for event in pygame.event.get():
            #quit program
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('███████████████ MOUSE ███████████████')
                # print(cursor_coordinates())
                pos_x, pos_y = pygame.mouse.get_pos()
                if pos_x > 350 and pos_x < 1150 and pos_y > 0:
                    
                    # print(f'clicking grid{CURRENT_GRID}')
                    print(f'clicking grid{BLANKGRID}')
                    currentsquare = square_select()

                if restart_button.rect.collidepoint((pos_x, pos_y)):
                    sound = pygame.mixer.Sound('reset.mp3')
                    pygame.mixer.Sound.play(sound)
                    CURRENT_GRID = set_board(1)
                    whiteturn = True
                    restart_button.clicked = True
            

            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                if restart_button.clicked == True and restart_button.rect.collidepoint((pos_x, pos_y)):
                    pass
                restart_button.clicked = False
                # print('released')

        draw_pieces()
        if square_selected == True and currentsquare != None:
            draw_select_overlay(currentsquare)
        if choosingpiece != None:
            draw_legal_overlay(legalmoves)

        res = cursor_coordinates()
        if res:
            x, y, z = res
            print_coords(x, y, z)
        pygame.display.update()
    
    pygame.quit()
    pygame.mixer.quit()

main()