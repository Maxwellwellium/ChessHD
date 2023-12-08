import pygame
from chess.constants import YELLOW, ALPHA, WIN, FPS
from chess.board import Board, Button
from chess.piece import draw_pieces, set_board
#import sys

pygame.font.init()  #renders the font
pygame.display.set_caption('ChessHD')

def cursor_coordinates():
    '''gets the coordinates of the cursor, converts them to chess notation, then prints it'''
    pos_x, pos_y = pygame.mouse.get_pos()
    if pos_x > 350 and pos_x < 1150 and pos_y > 0:    #when the mouse cursor isn't on the board, it shouldn't have coordinates
        coord_x = int(((pos_x - 350) / 100))    #use 350 to offset x
        coord_y = int(8 - (pos_y / 100))
        z = [ALPHA[coord_x], coord_y + 1]
        #print(z)   #for debugging
    
        font = pygame.font.Font(None, 30)   #default font, to use different ones must make dif variables
        chess_coord = font.render(f'Square: {z[0] + str(z[1])}', True, YELLOW)
        WIN.blit(chess_coord, (1200, 750))  #prints coords in bottom right corner
        WIN.blit(font.render(f'{z[0] + str(z[1])}', True, YELLOW), (coord_x * 100 + 352, 702 - coord_y * 100))  
        #^prints coords on highlighted square, offset slightly
        return z

restart_button = Button(50, 50, 1.25, 'restart')

def main():
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    board = Board()
    #restart_button.draw()

    set_board(1)
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
                #pos_x, pos_y = event.pos

                pos_x, pos_y = pygame.mouse.get_pos()
                if restart_button.rect.collidepoint((pos_x, pos_y)):
                    # if pygame.mouse.get_pressed()[0]:# and restart_button.clicked == False:
                    #     restart_button.clicked = True
                    #     set_board(1)
                    #     print('clicked')
                    set_board(1)
                    restart_button.clicked = True

            if event.type == pygame.MOUSEBUTTONUP: # and restart_button.clicked == True:
                pos_x, pos_y = pygame.mouse.get_pos()
                if restart_button.clicked == True and restart_button.rect.collidepoint((pos_x, pos_y)):
                    print('button clicked')
                restart_button.clicked = False
                print('released')

        #board.draw_squares(WIN)
        draw_pieces()

        cursor_coordinates()
        pygame.display.update()
    
    pygame.quit()

main()