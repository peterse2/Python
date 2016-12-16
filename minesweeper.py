import random
import enum
from Tools.Scripts.treesync import raw_input
'''
minesweeper.py
Authors: Caitlin Crowe and Emily Peterson
'''

'''
 Status of the game
'''

class Status(enum.Enum):
    WON, LOST, INPROGRESS = range(3)


'''
 Displays list of commands allowed at the prompt
'''


def display_menu():
    print("List of available commands:")
    print("   Show Mines: s/S")
    print("   Hide Mines: h/H")
    print("   Select Cell: c/C")
    print("   Display Board: b/B")
    print("   Display Menu: m/M")
    print("   Quit: q/Q\n")


'''
Initializes the fields of each cell on the board as follows:
    is_mine field to false
    mines field to 0
    visible field to false
'''


def init_board(size: int, board: list):
    for r in range(0, size):
        for c in range(0, size):
            board[r][c] = {'is_mine': False, 'mines': 0, 'visible': False}


'''
Places the specified number of mines randomly on the board
'''


def place_mines_on_board(size: int, board: list, nbr_mines: int):
    i = 0
    while i < nbr_mines:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        if not board[r][c].get("is_mine"):
            board[r][c]['is_mine'] = True
            i += 1


'''
For each non-mine cell on the board, set the "mines" field to the
number of mines in the immediate neighborhood.
'''


def fill_in_mine_count_for_non_mine_cells(size: int, board: list):
    for r in range(0, size):
        for c in range(0, size):
            board[r][c]['mines'] = get_nbr_neighbor_mines(r, c, size, board)


'''
Counts and returns the number of mines on the board
'''


def nbr_of_mines(size: int, board: list) -> int:
    count = 0
    for r in range(0, size):
        for c in range(0, size):
            if board[r][c].get('is_mine'):
                count += 1
    return count


'''
Returns the number of mines in the immediate neighborhood of a cell
at location (row,col) on the board.
'''


def get_nbr_neighbor_mines(r: int, c: int, size: int, board: list) -> int:
    count = 0
    if not board[r][c].get('is_mine'):  # if there is no mine in the current cell
        if (r == 0) and (c == 0):  # top left corner
            # check bottom, right, and bottom-right corner cell
            if board[1][0].get('is_mine'):  # bottom
                count += 1
            if board[0][1].get('is_mine'):  # right
                count += 1
            if board[1][1].get('is_mine'):  # bottom-right corner
                count += 1
        elif (r == 0) and (c == (size - 1)):  # top right corner
            # check bottom, left, bottom-left corner cell
            if board[1][(size - 1)].get('is_mine'):  # bottom
                count += 1
            if board[0][(size - 2)].get('is_mine'):  # left
                count += 1
            if board[1][(size - 2)].get('is_mine'):  # bottom-left corner
                count += 1
        elif (r == (size - 1)) and (c == 0):  # bottom left corner
            # check above, right, top-right corner
            if board[(size - 2)][0].get('is_mine'):  # above
                count += 1
            if board[(size - 1)][1].get('is_mine'):  # right
                count += 1
            if board[(size - 2)][1].get('is_mine'):  # above-right corner
                count += 1
        elif (r == (size - 1)) and (c == (size - 1)):  # bottom right corner
            # check above, left, top-left corner
            if board[(size - 2)][(size - 1)].get('is_mine'):  # above
                count += 1
            if board[(size - 1)][(size - 2)].get('is_mine'):  # right
                count += 1
            if board[(size - 2)][(size - 2)].get('is_mine'):  # above-right corner
                count += 1
        elif (r > 0) and (r < (size - 1)) and (c == 0):  # left wall
            # check above, right, below, top-right, bottom-right
            if board[r - 1][0].get('is_mine'):  # above
                count += 1
            if board[r][1].get('is_mine'):  # right
                count += 1
            if board[r + 1][0].get('is_mine'):  # below
                count += 1
            if board[r - 1][1].get('is_mine'):  # top-right
                count += 1
            if board[r + 1][1].get('is_mine'):  # bottom-right
                count += 1
        elif (r > 0) and (r < (size - 1)) and (c == (size - 1)):  # right wall
            # check above, left, below, top-left, bottom-left
            if board[r - 1][(size - 1)].get('is_mine'):  # above
                count += 1
            if board[r][(size - 2)].get('is_mine'):  # left
                count += 1
            if board[r + 1][(size - 1)].get('is_mine'):  # below
                count += 1
            if board[r - 1][(size - 2)].get('is_mine'):  # top-left
                count += 1
            if board[r + 1][(size - 2)].get('is_mine'):  # bottom-left
                count += 1
        elif (r == 0) and (c > 0) and (c < (size - 1)):  # top wall
            # check left, right, below, bottom-left, bottom-right
            if board[0][c - 1].get('is_mine'):  # left
                count += 1
            if board[0][c + 1].get('is_mine'):  # right
                count += 1
            if board[1][c].get('is_mine'):  # below
                count += 1
            if board[1][c - 1].get('is_mine'):  # bottom-left
                count += 1
            if board[1][c + 1].get('is_mine'):  # bottom-right
                count += 1
        elif (r == (size - 1)) and (c > 0) and (c < (size - 1)):  # bottom wall
            # check above, left, right, top-left, top-right
            if board[(size - 2)][c].get('is_mine'):  # above
                count += 1
            if board[(size - 1)][c - 1].get('is_mine'):  # left
                count += 1
            if board[(size - 1)][c + 1].get('is_mine'):  # right
                count += 1
            if board[(size - 2)][c - 1].get('is_mine'):  # top-left
                count += 1
            if board[(size - 2)][c + 1].get('is_mine'):  # top-right
                count += 1
        else:  # in the middle
            # check all around: above, left, right, bottom, top-left, top-right, bottom-left, bottom-right
            if board[r - 1][c].get('is_mine'):  # above
                count += 1
            if board[r][c - 1].get('is_mine'):  # left
                count += 1
            if board[r][c + 1].get('is_mine'):  # right
                count += 1
            if board[r + 1][c].get('is_mine'):  # below
                count += 1
            if board[r - 1][c - 1].get('is_mine'):  # top-left
                count += 1
            if board[r - 1][c + 1].get('is_mine'):  # top-right
                count += 1
            if board[r + 1][c - 1].get('is_mine'):  # bottom-left
                count += 1
            if board[r + 1][c + 1].get('is_mine'):  # bottom-right
                count += 1
    return count


'''
Displays the board. If a cell is not currently visible and has a
mine, show the mine if the displayMines is true. Used for debugging
and testing purposes.
'''


def display_board(size: int, board: list, display_mines: bool):
    print("\n   ")
    print("\t\t", end="")
    for c in range(1, size + 1):
        print(c, "\t", end="")  # print column numbers
    print("")
    for r in range(0, size):
        print("\t", (r + 1), end="")  # print row numbers
        for c in range(0, size):
            if display_mines:
                if board[r][c].get('is_mine'):
                    print("\t*", end="")
                elif board[r][c].get('visible'):
                    print("\t", board[r][c].get('mines'), end="")
                elif not board[r][c].get('visible'):
                    print("\t?", end="")
            elif not display_mines:
                if (board[r][c].get('is_mine')) and (board[r][c].get('mines') != 100):
                    print("\t?", end="")
                elif (board[r][c].get('is_mine')) and (board[r][c].get('mines') == 100):
                    print("\t*", end="")
                elif board[r][c].get('visible'):
                    print("\t", board[r][c].get('mines'), end="")
                elif not board[r][c].get('visible'):
                    print("\t?", end="")
        print("")
    print("")


'''
Prompts the user for board size, reads and validates the input
entered, and returns the integer if it is within valid range.
repeats this in a loop until the user enters a valid value.
'''


def get_board_size() -> int:
    size = 0
    while (size < 5) or (size > 15):
        size = int(input("Enter the board size (5 .. 15): "))
    return size


'''
Prompts the user for percentage of mines to place on the board,
reads and validates the input entered, and returns the integer if it
is thin valid range. repeats this in a loop until the user enters
a valid value for board size.
'''


def get_percent_mines() -> int:
    percent = int(input("Enter the percentage of mines on the board (10 .. 70): "))
    return percent


'''
Process cell selection by user during the game
'''


def select_cell(row: int, col: int, size: int, board: list) -> Status:
    i = size * size - nbr_of_mines(size, board)
    if board[row][col].get('is_mine'):
        board[row][col]['mines'] = 100
        return Status.LOST
    elif not board[row][col].get('is_mine'):
        if nbr_visible_cells(size, board) == i:
            return Status.WON
        else:
            set_all_neighbor_cells_visible(row, col, size, board)
            return Status.INPROGRESS


'''
Returns the number of cells that are currently visible.
'''


def nbr_visible_cells(size: int, board: list) ->int:
    count = 1
    for r in range(0, size):
        for c in range(0, size):
            if board[r][c].get('visible'):
                count += 1
    return count


'''
If the mine count of a cell at location (row,col) is zero, then make
the cells in the immediate neighborhood visible and repeat this
process for each of the cells in this set of cells that have a mine
count of zero, and so on.
'''


def set_all_neighbor_cells_visible(row: int, col: int, size: int, board: list):
    # dont want to check cells that don't exist
    if row < 0 or row >= size:
        return
    if col < 0 or col >= size:
        return
    # if the cell is already visible, don't do anything to it
    if board[row][col].get('visible'):
        return
    board[row][col]['visible'] = True
    if board[row][col].get('mines') == 0:
        set_all_neighbor_cells_visible(row - 1, col, size, board)  # check above
        set_all_neighbor_cells_visible(row, col + 1, size, board)  # check right
        set_all_neighbor_cells_visible(row, col - 1, size, board)  # check left
        set_all_neighbor_cells_visible(row + 1, col, size, board)  # check below

'''
Main driver of the program. Uses the functions defined above.
'''


def main():
    row = 0
    col = 0

    display_mines = False
    game_state = Status.INPROGRESS

    print("!!!!!WELCOME TO THE MINESWEEPER GAME!!!!!\n")
    size = get_board_size()

    # declare 2D array of cells
    board = [[' ' for i in range(size)] for i in range(size)]

    init_board(size, board)

    # determine number of mine to place on the board
    nbr_mines = int((size * size * (get_percent_mines() / 100.0)))

    # place mines randomly on the board
    place_mines_on_board(size, board, nbr_mines)

    # For each non-mine cell, sets the neighboring mine count
    fill_in_mine_count_for_non_mine_cells(size, board)

    display_board(size, board, display_mines)

    while True:
        command = input("Enter command (m/M for command menu): ")
        if (command == "m") or (command == "M"):
            display_menu()
        elif (command == "c") or (command == "C"):
            while (row < 1) or (row > size) or (col < 1) or (col > size):
                row, col = raw_input("Enter row and col of cell: ").split()
                row, col = [int(row), int(col)]
                if (row < 1) or (row > size) or (col < 1) or (col > size):
                    print("Invalid row or column values. Try again.")
            row -= 1
            col -= 1
            game_state = select_cell(row, col, size, board)
            display_board(size, board, display_mines)
        elif (command == "s") or (command == "S"):
            display_mines = True
            display_board(size, board, display_mines)
        elif (command == "h") or (command == "H"):
            display_mines = False
            display_board(size, board, display_mines)
        elif (command == "b") or (command == "B"):
            display_board(size, board, display_mines)
        elif (command == "q") or (command == "Q"):
            print("Bye.")
            return 0
        else:
            print("Invalid command. Try again.")

        if game_state == Status.WON:
            print("You found all the mines. Congratulations. Bye.")
            return 0
        elif game_state == Status.LOST:
            print("Oops. Sorry, you landed on a mine. Bye")
            return 0
    return 0

main()