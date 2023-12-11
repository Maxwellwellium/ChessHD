import pygame
from chess.constants import YELLOW, ALPHA, WIN, FPS, BLANKGRID
from chess.board import Board, Button
from chess.piece import draw_pieces, set_board

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
    pos_x, pos_y = pygame.mouse.get_pos()
    if pos_x > 350 and pos_x < 1150 and pos_y > 0:
        square_selected = True
        output = cursor_coordinates()
        square = output[2]
        newsquare = square.copy()
        print(output)
        # print(square)
        piece = piece_detect(square)
        if piece != None:
            legal_moves(piece)
            print(piece)
        if square_selected == True:
            if currentsquare == newsquare and currentsquare != None:
                square_selected == False

        return newsquare


def legal_moves(piece):
    '''finds all legal moves for a piece and returns them as a list'''
    pass

def draw_overlay(square):
    '''draws the overlay image over the selected square'''
    x_og = ALPHA.index(square[0])
    y_og = square[1]
    pos_x = (x_og * 100) + 350
    pos_y = (800 - (y_og * 100))
    raw_image = pygame.image.load(f'select_overlay.png').convert_alpha()
    piece_image = pygame.transform.scale(raw_image, (100, 100))
    WIN.blit(piece_image, (pos_x, pos_y))

def piece_detect(square):
        '''detects if there is a piece on a given square'''
        #Finds index of square in grid, then uses that index to access square in current grid to see if theres a piece
        global CURRENT_GRID
        index = BLANKGRID.index(square)
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
    run = True
    clock = pygame.time.Clock()
    board = Board()

    global CURRENT_GRID
    CURRENT_GRID = set_board(1)
    global square_selected
    global currentsquare
    square_selected = False
    currentsquare = None
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
                print('test')
                # print(cursor_coordinates())
                pos_x, pos_y = pygame.mouse.get_pos()
                if pos_x > 350 and pos_x < 1150 and pos_y > 0:
                    
                    # print(f'clicking grid{CURRENT_GRID}')
                    currentsquare = square_select()

                if restart_button.rect.collidepoint((pos_x, pos_y)):
                    CURRENT_GRID = set_board(1)
                    restart_button.clicked = True
            

            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                if restart_button.clicked == True and restart_button.rect.collidepoint((pos_x, pos_y)):
                    print('button clicked')
                restart_button.clicked = False
                print('released')

        draw_pieces()
        if square_selected == True:
            draw_overlay(currentsquare)
        res = cursor_coordinates()
        if res:
            x, y, z = res
            print_coords(x, y, z)
        pygame.display.update()
    
    pygame.quit()

main()

#compare z0 and z1, then use varibale to reference z3
#then remove it from location and print in another location