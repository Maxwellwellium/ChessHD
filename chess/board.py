import pygame
from .constants import BLACK, ROWS, WHITE, SQUARE_SIZE, CYAN, WIDTH, HEIGHT, WIN
#from .piece import Pawn, Piece

class Board:
    def __init__(self):
        self.selected_piece = None
#draws the checkerboard pattern onto the screen
    def draw_squares(self, win):
        '''Draws the Checkerboard pattern'''
        win.fill(CYAN)
        pygame.draw.rect(win, BLACK, ((350, 0), (WIDTH, HEIGHT)))
        for row in range(ROWS): #these loops draw the checkerboard pattern
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE + 350, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

class Button:
    def __init__(self, x, y, scale, image):
        raw_image = pygame.image.load(f'{str(image).lower()}_button.png').convert()
        self.x = x
        self.y = y
        self.w = raw_image.get_width()
        self.h = raw_image.get_height()
        self.display_image = pygame.transform.scale(raw_image, (int(self.w * scale), int(self.h * scale)))
        self.rect = self.display_image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):

        WIN.blit(self.display_image, (self.x, self.y))

