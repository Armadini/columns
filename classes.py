# ARMAN ROSHANNAI
# 73121312

import random

"""IMPORTANT NOTE PLEASE READ:

I left in some functions that are unused becasue I want to continue working on this game and implement
the breaking functionality. Please don't mark off points for the extra functions. Thank you :)

"""


class board:
    def __init__(self, width, height):
        self.board = []
        self.rows = 13
        self.cols = 6
        self.width = width
        self.height = height
        self.faller = None
            
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                self.board[row].append([' ', ' '])
        
    # def print_board(self):
    #     for row in range(self.rows):
    #         print('|', end='')
    #         for col in range(self.cols):
    #             if self.board[row][col][1] == '[':
    #                 fall_type = '[]'
    #             else:
    #                 fall_type = self.board[row][col][1] + self.board[row][col][1]
    #             print(fall_type[0] + self.board[row][col][0] + fall_type[1], end='')
    #         print('|')
    #     print(' ' + ('-' * self.cols * 3) + ' ')

    def handle_fall(self):
        for col in range(self.cols):
            elements = []
            for row in range(self.rows):
                if self.board[row][col][0] !=  ' ':
                    elements.append(self.board[row][col][0])
                self.board[row][col][0] = ' '
            while len(elements) != self.rows:
                elements = [' '] + elements
            for row in range(self.rows):
                self.board[row][col][0] = elements[row]

    def assign_break(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col][0] != ' ':
                    self._check_horizontal(row, col)
                    self._check_vertical(row, col)
                    self._check_diagonal_plus(row, col)
                    self._check_diagonal_minus(row, col)

    def handle_break(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col][1] == '*':
                    self.board[row][col][0] = ' '
                    self.board[row][col][1] = ' '
        
    def check_break(self):
        self.assign_break()
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col][1] == '*':
                    return True

    def get_command(self):
        self.command = input()

    def handle_command(self):
        command = self.command
        if command =='':
            self.pass_time()
        elif command[0] == 'F':
            self.create_faller()
        elif command[0] == 'R':
            self.faller.rotate()
        elif command[0] == '<':
            self.move_left()
            self._check_below()
        elif command[0] == '>':
            self.move_right()
            self._check_below()
        elif command[0] == 'Q':
            self.end_sequence()

    def create_faller(self):
        self.faller = faller()
        eligibles = []
        for col in range(self.cols):
            if self.board[0][col][0] == ' ':
                eligibles.append(col)
        
        if len(eligibles) == 0:
            self.end_sequence()

        self.faller.faller[3] = random.choice(eligibles)
        # FALLER STRUCTURE: if command == S V T,  faller = [[S, row],[V, row],[T, row], column, fall_type] with S on top
        if self.board[0][self.faller.faller[3]][0] == ' ':
            self.faller.faller[2][1] = 0
            self.faller.faller[1][1] = -1
            self.faller.faller[0][1] = -2
            self.faller.faller[4] = '['
        else:
            self.end_sequence()

    
    def generate_board(self):
        if self.faller != None:
            for i in range(3):
                letter = self.faller.faller[i][0]
                fall_type = self.faller.faller[4]
                row = self.faller.faller[i][1]
                col = self.faller.faller[3]
                if row >= 0:
                    self.board[row][col][0] = letter
                    self.board[row][col][1] = fall_type
            if self.faller.faller[0][1] > 0:
                row = self.faller.faller[0][1]
                col = self.faller.faller[3]
                for i in range(0, row):
                    self.board[i][col][0] = ' '
                    self.board[i][col][1] = ' '


    def pass_time(self):
        # try:
        if self.faller != None:
            self._move_down()
        elif self.check_break():
            self.handle_break()
            self.handle_fall()
            self.assign_break()
        # except as e:
        #     print(e)


    def end_sequence(self):
        exit()

    def game_status(self):
        for row in range(self.rows):
            for col in range(self.cols):
                state = False
                if self.board[row][col][0] == ' ' or self.board[row][col][1] != ' ':
                    return True
            return state

    def _faller_status(self):
        state = True
        for i in range(3):
            if self.faller.faller[i][1] < 0:
                state = False
        if not(state):
            # self.print_board()
            self.end_sequence()

    def _check_below(self):
        try:
            state = self.board[self.faller.faller[2][1]+1][self.faller.faller[3]][0] != ' '
        except:
            state = False
        if state or self.faller.faller[2][1] >= self.rows-1:
            if self.faller.faller[4] == '|':
                self.faller.faller[4] = ' '
                self.generate_board()
                self._faller_status()
                self.faller = None
                self.assign_break()
            else:
                self.faller.faller[4] = '|'
        else:
            self.faller.faller[4] = '['

    def _move_down(self):
        try:
            if (self.faller.faller[2][1] < self.rows-1) and (self.board[self.faller.faller[2][1]+1][self.faller.faller[3]][0] == ' '):
                for i in range(3):
                    self.faller.faller[i][1] += 1
                
        except IndexError:
            pass
        self._check_below()
        
    def move_right(self):
        try:
            state = True
            for i in range(3):
                if self.board[self.faller.faller[i][1]][self.faller.faller[3]+1][0] != ' ':
                    state = False
            if state:
                for i in range(3):
                    self.board[self.faller.faller[i][1]][self.faller.faller[3]][0] = ' '
                    self.board[self.faller.faller[i][1]][self.faller.faller[3]][1] = ' '
                self.faller.faller[3] += 1
        except IndexError:
            pass
            
    def move_left(self):
        state = True
        for i in range(3):
            if self.board[self.faller.faller[i][1]][self.faller.faller[3]-1][0] != ' ' or self.faller.faller[3]-1 < 0:
                state = False
        if state:
            for i in range(3):
                self.board[self.faller.faller[i][1]][self.faller.faller[3]][0] = ' '
                self.board[self.faller.faller[i][1]][self.faller.faller[3]][1] = ' '
            self.faller.faller[3] -= 1
        

    def _check_horizontal(self, row, col):
        try:
            if self.board[row][col][0] == self.board[row][col+1][0] and self.board[row][col][0] == self.board[row][col+2][0]:
                self.board[row][col][1] = '*'
                self.board[row][col+1][1] = '*'
                self.board[row][col+2][1] = '*'
                try:
                    c = 3
                    while self.board[row][col][0] == self.board[row][col+c][0]:
                        self.board[row][col+c][1] = '*'
                        c += 1
                except IndexError:
                    pass
        except IndexError:
            pass

    def _check_vertical(self, row, col):
        try:
            if (row-2) >= 0:
                if self.board[row][col][0] == self.board[row-1][col][0] and self.board[row][col][0] == self.board[row-2][col][0]:
                    self.board[row][col][1] = '*'
                    self.board[row-1][col][1] = '*'
                    self.board[row-2][col][1] = '*'
                    try:
                        c = 3
                        while self.board[row][col][0] == self.board[row-c][col][0] and row-c >= 0:
                            self.board[row-c][col][1] = '*'
                            c += 1
                    except IndexError:
                        pass
        except IndexError:
            pass

    def _check_diagonal_plus(self, row, col):
        try:
            if row-2 >= 0:
                if self.board[row][col][0] == self.board[row-1][col+1][0] and self.board[row][col][0] == self.board[row-2][col+2][0]:
                    self.board[row][col][1] = '*'
                    self.board[row-1][col+1][1] = '*'
                    self.board[row-2][col+2][1] = '*'
                    try:
                        c = 3
                        while self.board[row][col][0] == self.board[row-c][col+c][0] and row-c >= 0:
                            self.board[row-c][col+c][1] = '*'
                            c += 1
                    except IndexError:
                        pass
        except IndexError:
            pass

    def _check_diagonal_minus(self, row, col):
        try:
            if self.board[row][col][0] == self.board[row+1][col+1][0] and self.board[row][col][0] == self.board[row+2][col+2][0]:
                self.board[row][col][1] = '*'
                self.board[row+1][col+1][1] = '*'
                self.board[row+2][col+2][1] = '*'
                try:
                    c = 3
                    while self.board[row][col][0] == self.board[row+c][col+c][0]:
                        self.board[row+c][col+c][1] = '*'
                        c += 1
                except IndexError:
                    pass
        except IndexError:
            pass



class faller:
    def __init__(self):
        letters = ['A','B','C','D','E','F','G']
        self.faller = [[random.choice(letters), None], [random.choice(letters), None], [random.choice(letters), None], None, None]


    def rotate(self):
        zero = self.faller[0][0]
        one = self.faller[1][0]
        two = self.faller[2][0]

        self.faller[0][0] = two
        self.faller[1][0] = zero
        self.faller[2][0] = one
