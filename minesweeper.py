# -*- coding: utf-8 -*-
"""
Student: Gil Shechter
ID: 207226317
Assignment no. 6
Program: minesweeper.py
"""

class MSSquare:
    ''' This class represents a square in the minesweeper game. 
        Attributes: 
            has_mine - bool - True if the square has mine
            hidden - bool - True if the square is hidden
            neighbor_mines - int - num of mines around the square '''
            
    def __init__(self, has_mine, hidden, neighbor_mines):
        ''' Constructs all the necessary attributes for the MSSquare object. '''
        if not isinstance(neighbor_mines, int) or neighbor_mines < 0:
            raise Exception('wrong neighbor mines value')
        if not isinstance(has_mine, bool):
            raise Exception('wrong has_mine value')
        if not isinstance(hidden, bool):
            raise Exception('wrong hidden value')
        self.__has_mine = has_mine
        self.__hidden = hidden
        self.__neighbor_mines = neighbor_mines
        
    def __str__(self):
        ''' If not hidden, prints the content of the square - If has mine prints 'x', if not prints neighbor_mines '''
        if self.__hidden == False:
            if self.has_mine == True:
                return "\033[1;31mx\033[00m"
            return str(self.__neighbor_mines)
        return ' '   
    
    def setMine(self, has_mine):
        ''' Set value to has_mine '''
        if not isinstance(has_mine, bool):
            raise Exception('wrong has_mine value')
        self.__has_mine = has_mine
        
    def setHidden(self, hidden):
        ''' Set value to hidden '''
        if not isinstance(hidden, bool):
            raise Exception('wrong hidden value')
        self.__hidden = hidden
        
    def setNeighbor(self, neighbor_mines):
        ''' Set value to neighbor_mines '''
        if not isinstance(neighbor_mines, int) or neighbor_mines < 0:
            raise Exception('wrong neighbor mines value')
        self.__neighbor_mines = neighbor_mines
        
    @property
    def has_mine(self):
        return self.__has_mine
    @has_mine.setter
    def has_mine(self, value):
        self.setMine(value)
    @property
    def hidden(self):
        return self.__hidden
    @hidden.setter
    def hidden(self, value):
        self.setHidden(value)
    @property
    def neighbor_mines(self):
        return self.__neighbor_mines
    @neighbor_mines.setter
    def neighbor_mines(self, value):
        self.setNeighbor(value)

def game_board(size, ms_list):
    ''' This function prints the game board '''
    for i in range(1, size+1):
        # Prints the game board with the given size and list of MSSquares
        print(' ' + '+---' * size + '+')
        print(i, end='')
        for j in range(1, size+1):
            # Prints the content of each square in the line
            print('|', ms_list[i][j], end=' ')
        print('|')
    print(' ' + '+---' * size + '+')
    for i in range(1, size+1):
        print('  ', i, end='')

def MS_list(size, mines_num):
    ''' This function creates the initial list of MSSquares and places the mines '''
    import random
    lst = [[MSSquare(False, True, 0) for i in range(size+2)] for j in range(size+2)]
    for i in range(mines_num):
        # Places mines in random places on the board
        x = random.randint(1, size-1)
        y = random.randint(1, size-1)
        while lst[x][y].has_mine == True:
            x = random.randint(1, size-1)
            y = random.randint(1, size-1)
        lst[x][y].has_mine = True
    return lst

def numOfMines(ms_list):
    ''' This function calculates neighbor mines for each MSSquare in the board '''
    for x in range(1, len(ms_list)-1):
        for y in range(1, len(ms_list)-1):
            if not ms_list[x][y].has_mine:
                count = 0
                if ms_list[x-1][y-1].has_mine:
                    count += 1
                if ms_list[x][y-1].has_mine:
                    count += 1
                if ms_list[x+1][y-1].has_mine:
                    count += 1
                if ms_list[x-1][y].has_mine:
                    count += 1
                if ms_list[x+1][y].has_mine:
                    count += 1
                if ms_list[x-1][y+1].has_mine:
                    count += 1
                if ms_list[x][y+1].has_mine:
                    count += 1
                if ms_list[x+1][y+1].has_mine:
                    count += 1
                ms_list[x][y].neighbor_mines = count

def free_spaces(ms_list, x, y):
    ''' This function exposes squares with no neighbor mines, until running into a square with neighbor mines '''
    if x < 1 or x >= (len(ms_list)-1):
        return
    elif y < 1 or y >= (len(ms_list)-1):
        return
    elif ms_list[x][y].neighbor_mines != 0:
        ms_list[x][y].hidden = False
        return
    elif ms_list[x][y].hidden == False:
        return
    else:
        ms_list[x][y].hidden = False
        free_spaces(ms_list, x+1, y)
        free_spaces(ms_list, x, y-1)
        free_spaces(ms_list, x, y+1)
        free_spaces(ms_list, x-1, y)
        free_spaces(ms_list, x+1, y+1)
        free_spaces(ms_list, x-1, y-1)
        free_spaces(ms_list, x-1, y+1)
        free_spaces(ms_list, x+1, y-1)
 
def check_win(ms_list, mines_num):
    ''' This function check if the user already won the game '''
    count = 0
    for ls in ms_list[1:-1]:
        for obj in ls[1:-1]:
            # Check if the number of mines equals the number of hidden MSSquares
            if obj.hidden == True:
                count += 1
    return count == mines_num

def game_over(ms_list):
    ''' This function exposes all the mines on the board '''
    for lst in ms_list:
        for obj in lst:
            if obj.has_mine:
                obj.hidden = False
    return ms_list

def guess_validity_check(ms_list):
    ''' This function checks validity of the input guess '''
    while True:
        # Try until valid input
        guess = input("Your guess(enter coordinates XY): ")
        if len(guess) != 2 or not guess.isnumeric():
            print('wrong input')
            continue
        x, y = int(guess[0]), int(guess[1])
        if x not in range(1, len(ms_list)-1) or y not in range(1, len(ms_list)-1):
            print('coordinate out of range')
            continue
        if not ms_list[x][y].hidden:
            print('This square is already chosen')
            continue
        break
    return x, y
    
def game_play(board_size, ms_list, mines_num):
    ''' This function runs the game. On each step it gets new coordinates as an guess input from the user,
        until winning or losing the game. '''
    print('\n* * * LETS PLAY! * * *\n')
    lose = False
    win = False
    while not win and not lose:
        # Keeps playing until win or lose
        game_board(board_size, ms_list)
        x, y = guess_validity_check(ms_list)
        if ms_list[x][y].has_mine:
            lose = True
        elif ms_list[x][y].neighbor_mines == 0:
            free_spaces(ms_list, x, y)
        else:
            ms_list[x][y].hidden = False
        if check_win(ms_list, mines_num):
            win = True
    game_board(board_size, game_over(ms_list))
    print("\n* * * YOU WIN! * * *") if win else print("\n * * * YOU LOSE! * * *")      
    
def main():
    ''' This program simulates the game Minesweeper.
        The program prints a board game at each level of the game.
        Each square of the board represents MSSquare object.
        The game ends when the user exposes a mine (lose), or when exposes all other squares (win) '''
    
    # Input check for board size
    while True:
        try:
            board_size = int(input("Enter board size(min 4,  max 9): "))
            if board_size not in range(4, 10):
                print('Board size not in range 4-9. Try again')
                continue
        except ValueError as error:
            print('wrong value entered: ', error)
            continue
        break
    
    # Input check for mines num
    while True:
        try:
            mines_num = int(input(f'Enter number of mines(max {board_size * 2}): '))
            if mines_num not in range(2 * board_size):
                print('Mines number not in range. Try again: ')
                continue
        except ValueError as error:
            print('wrong value error: ', error)
            continue
        break
    
    ms_list = MS_list(board_size, mines_num)
    numOfMines(ms_list)
    game_play(board_size, ms_list, mines_num)
main()