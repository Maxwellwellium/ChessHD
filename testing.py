# import pygame
# from chess.constants import ALPHA, BLACK, GB, GW
# from chess.piece import King, game_over
# import random


# ██ This file was for testing things before implementing them into the main script ██


# l = [0, 1]

# # x = l[0]
# # y = 5
# # x.append(y)

# a = isinstance(l[0], list)
# if a == True:
#     print('test1')
# else:
#     print('test2')
# # x = True
# # print(x)
# # x = not x
# # print(x)




# z = []
# x = 5
# y = -1
# z.append(x + y)
# print(z)

# allmoves = []
# square = ['a', 8]
# file, rank = square

# existing_ranks = [rank]
# if rank-1 in NUM:
#     existing_ranks.append(rank-1)
# if rank+1 in NUM:
#     existing_ranks.append(rank+1)

# existing_files = [file]
# index = ALPHA.index(file)
# if index != 0:
#     existing_files.append(ALPHA[index-1])
# if index != 7:
#     existing_files.append(ALPHA[index+1])
# for ranks in existing_ranks:
#     for files in existing_files:
#         allmoves.append([files, ranks])
# allmoves.remove([file, rank])

# print(allmoves)

# def picksquare(color):
#     '''picks an available square'''
#     if color == 'white':
#         rows = GW
#     else:
#         rows = GB
    
#     current_row = rows[0]
#     x = 0
#     if len(current_row) != 0:
#         choice = random.choices(current_row)
#     else:
#         x += 1
#         current_row = rows[x]
#         choice = random.choices(current_row)
#     print(choice)
#     if choice[0] in GRID:
#         spawn = choice[0]
#         print(spawn)
#     else:
#         current_row = current_row.remove(choice[0])
#         print(current_row)
#     return spawn

# picksquare('black')
# picksquare('white')
# picksquare('black')
# picksquare('black')
# picksquare('black')
# picksquare('black')
# print(GRID)


# GW = [[], [], [], []]
# GB = [[], [], [], []]

# for i in range(len(GRID)):
#     if GRID[i][1] == 1:
#         GW[0].append(GRID[i])
#     elif GRID[i][1] == 2:
#         GW[1].append(GRID[i])
#     elif GRID[i][1] == 3:
#         GW[2].append(GRID[i])
#     elif GRID[i][1] == 4:
#         GW[3].append(GRID[i])
#     elif GRID[i][1] == 5:
#         GB[3].append(GRID[i])
#     elif GRID[i][1] == 6:
#         GB[2].append(GRID[i])
#     elif GRID[i][1] == 7:
#         GB[1].append(GRID[i])
#     elif GRID[i][1] == 8:
#         GB[0].append(GRID[i])
# print(GW)
# print(GB)



# worth = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9}
# z = random.choices(list(worth.items()), weights = [50, 15, 15, 12, 8])

# print(z)


# x = 10

# def mult(x):
#     z = x * 10
#     return z

# mult(x)
# print(x + 2)



# l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# y = random.choice(l)

# if y in l:
#     l.remove(y)
# print(y)
# print(l)
#print(GB)
# def convertcoords(piece_square):
#     '''takes the chess square the piece is on and converts it into xy coordinates'''
#     x_og = ALPHA.index(piece_square[0][0])
#     y_og = piece_square[0][1]

#     pos_x = (x_og * 100) + 350 + 10
#     pos_y = ((y_og - 1) * 100) + 10
#     return pos_x, pos_y

# def create_p():
#     pawns = pygame.sprite.Group() 
#     piece_square = random.choices(GB)
#     pos_x, pos_y = convertcoords(piece_square)
#     piece = Pawn(pos_x, pos_y, BLACK)
#     pawns.add(piece)

#     return pawns.sprites

# print(create_p())

#piece_square = random.choices(GB)

# def convertcoords(piece_square):
#     '''takes the chess square the piece is on and converts it into xy coordinates'''
#     x_og = ALPHA.index(piece_square[0][0]) + 1
#     y_og = piece_square[0][1]

#     pos_x = (x_og * 100) + 350
#     pos_y = (y_og * 100)
#     return pos_x, pos_y


# convertcoords(piece_square)

#print(piece_square[0][0])
#print(ALPHA[5])

#piece_square = random.choices(GB)
#print(piece_square)

#gen_white = []
#gen_black = []
#gen_extra = []
#
#for i in range(len(GRID)):
#    if GRID[i][1] == 1 or GRID[i][1] == 2:
#        gen_white.append(GRID[i])
#    elif GRID[i][1] == 7 or GRID[i][1] == 8:
#        gen_black.append(GRID[i])
#    else:#if GRID[i][1] == 3 or GRID[i][1] == 4 or GRID[i][1] == 5 or GRID[i][1] == 6:
#        gen_extra.append(GRID[i])

#print(gen_white)   
#print(gen_black)
#print(gen_extra)
#print(GRID)

#total = 0
#amount = 39
#while total < amount:
#    worth = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9}
#    z = random.choices(list(worth.items()), weights = [50, 15, 15, 12, 8])
#    print(z)
#    total += z[0][1]
    #print(total)
    #total += 
    #create('pawn')

#GRID = []
#for col in ALPHA:
#    for row in range(1, 9):
#        GRID.append([col, row])
#print(GRID)

#grid = {}
#for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
#    grid[col] = list(range(1,9))
#        
#print(grid)

#def assign_squares(self, win):
    #    '''assigns all coordinates on the board with a chess coordinate'''
    #    grid = {}
    #    for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    #       grid[col] = list(range(0,9))

#self.board = {'a' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'b' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'c' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'd' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'e' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'f' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'g' : [1, 2, 3, 4, 5, 6, 7, 8],
        #              'h' : [1, 2, 3, 4, 5, 6, 7, 8]}

