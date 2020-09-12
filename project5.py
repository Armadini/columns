# ARMAN ROSHANNAI
# 73121312

import pygame
import classes
import math
# from pygame.locals import *

def create_surface():
    """Creates a surface with a default size of 600x600."""
    size = (600,600)
    surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    return surface

def get_color(board, row, col):
    """Checks game board for different jewels and assigns colors accordingly."""
    color_dict = {' ':(255,255,255),'A':(255,0,0) ,'B':(255,255,0),'C':(0,255,0),'D':(0,255,255),'E':(0,0,255),'F':(255,0,255),'G':(127,61,137)}
    symbol = board.board[row][col][0]
    return color_dict[symbol]

def handle_freeze(width, height, surface, board, col, row, x, y):
    """Displays black dod in the center of each frozen jewel."""
    minimum = min(width, height)
    if board.board[row][col][1] == '|':
        pygame.draw.circle(surface, pygame.Color(0,0,0), (math.ceil(x+width/2),math.ceil(y+width/2)), math.ceil(minimum/4))




def generate_surface(board, surface):
    """Generates the surface with a properly sized grid. The grid is filled in according to the jewels on the game board."""
    width = board.width
    height = board.height

    start_coord_x = width/3
    start_coord_y = height/7

    cell_width = start_coord_x/7
    margin_x = cell_width/7

    cell_height = (height - 2*start_coord_y)/14
    margin_y = cell_height/14

    for row in range(board.rows):
        for col in range(board.cols):
            color = get_color(board,row,col)
            my_rect = pygame.Rect(math.ceil(col*(cell_width+margin_x)+start_coord_x), math.ceil(row*(cell_height+margin_y)+start_coord_y), math.ceil(cell_width), math.ceil(cell_height))
            pygame.draw.rect(surface, color, my_rect)
            handle_freeze(cell_width, cell_height, surface, board, col, row, col*(cell_width+margin_x)+start_coord_x, row*(cell_height+margin_y)+start_coord_y)

    
    

def game_loop(board, surface):
    """Runs the game as a loop until the 'x' is clicked in the corner of the window, in which case the loop ends."""
    running = True
    clock = pygame.time.Clock()
    count = 0
    TICK = 60

    while running:
        clock.tick(TICK)
        if count % TICK == 0:
            board.pass_time()
            board.generate_board()
        if board.faller == None:
            board.create_faller()
            board.generate_board()
            generate_surface(board, surface)
        surface.fill(pygame.Color(0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                board.width = event.w
                board.height = event.h
                size = (event.w, event.h)
                surface = pygame.display.set_mode(size, pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.move_left()
                    board.generate_board()
                if event.key == pygame.K_RIGHT:
                    board.move_right()
                    board.generate_board()
                if event.key == pygame.K_SPACE:
                    board.faller.rotate()
                    board.generate_board()

        generate_surface(board,surface)
        pygame.display.flip()
        count += 1


def run():
    """Central logic for the game. Abstracted for ease of understanding."""
    pygame.init()

    surface = create_surface()
    board = classes.board(600, 600)
    pygame.display.set_caption("~~~COLUMNS~~~")
    game_loop(board, surface)

    pygame.quit()


if __name__ == "__main__":
    run()
