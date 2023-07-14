import tkinter as tk
from tkinter import filedialog
import os
import sys

def read_file_contents():
    # Get the root directory of the executable
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the subdirectory name
    subdirectory = 'input'

    # Create the full path to the subdirectory
    input_dir = os.path.join(root_dir, subdirectory)

    # Open file explorer dialog starting at the input directory
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=input_dir, filetypes=[("Text Files", "*.txt")])

    if not file_path:
        return None

    # Read file contents and split into an array
    with open(file_path, 'r') as file:
        contents = file.read()
        array = list(contents)

    # Verify inputs
    if not verify_input(array):
        print("Invalid Input")
        sys.exit()

    return array

def print_board(p):
    board = [
        [p[18], "-----------", p[19], "-----------", p[20]],
        ["|           |           |"],
        ["|   ", p[15], "-------", p[16], "-------", p[17], "   |"],
        ["|   |       |       |   |"],
        ["|   |   ", p[12], "---", p[13], "---", p[14], "   |   |"],
        ["|   |   |       |   |   |"],
        [p[6], "---", p[7], "---", p[8], "       ", p[9], "---", p[10], "---", p[11]],
        ["|   |   |       |   |   |"],
        ["|   |   ", p[4], "-------", p[5], "   |   |"],
        ["|   |               |   |"],
        ["|   ", p[2], "---------------", p[3], "   |"],
        ["|                       |"],
        [p[0], "-----------------------", p[1]],
    ]

    for row in board:
        print(''.join(row))

def generate_moves_opening(position):
    return generate_add(position)

def generate_moves_mid(board):
    num_white_pieces, num_black_pieces = count_pieces(board)
    if num_white_pieces == 3:
        return generate_hopping(board)
    else:
        return generate_move(board)

def generate_moves_opening_black(position):
    swapped_board = swap_pieces(position)
    possible_positions = generate_moves_opening(swapped_board)
    for board_index in range(0, len(possible_positions)):
        possible_positions[board_index] = swap_pieces(possible_positions[board_index])
    return possible_positions

def generate_moves_mid_black(board):
    swapped_board = swap_pieces(board)
    possible_positions = generate_moves_mid(swapped_board)
    for board_index in range(0, len(possible_positions)):
        possible_positions[board_index] = swap_pieces(possible_positions[board_index])
    return possible_positions

def generate_add(board):
    possible_boards = []

    # Iterate through possible empty locations and replace with W
    for index in range(0, len(board)):

        # Add piece if current index is empty space
        if board[index] == "x":
            board_copy = board.copy()
            board_copy[index] = 'W'

            # If there are 3 in a row, remove possible black pieces and add boards to list
            if close_mill(index, board_copy):
                generate_remove(board_copy, possible_boards)

            # Else, just add board to possible boards list
            else:
                possible_boards.append(board_copy)

    return possible_boards

def generate_hopping(board):
    possible_boards = []

    # Parse for possible starting points
    for start_index in range(0, len(board)):
        if board[start_index] == 'W':

            # Parse for possible landing points
            for landing_index in range(0, len(board)):
                if board[landing_index] == 'x':
                    board_copy = board.copy()
                    board_copy[start_index] = 'x'
                    board_copy[landing_index] = 'W'

                    # If landing point closes a mill, remove opponent piece
                    if close_mill(landing_index, board_copy):
                        generate_remove(board_copy, possible_boards)
                    else:
                        possible_boards.append(board_copy)

    return possible_boards

def generate_remove(board, possible_boards):
    num_positions_added = 0

    # Iterate through possible black locations
    for index in range(0, len(board)):

        # Add piece if current index is black
        if board[index] == "B":

            # Do not remove pieces from existing mills
            if not close_mill(index, board):
                board_copy = board.copy()
                board_copy[index] = 'x'
                possible_boards.append(board_copy)
                num_positions_added += 1

    # No positions were added
    if num_positions_added == 0:
        possible_boards.append(board)

def generate_move(board):
    possible_boards = []

    # Parse through possible starting pieces to move
    for start_index in range(0, len(board)):
        if board[start_index] == 'W':
            neighbor_list = neighbors(start_index)

            # Parse through possible landing positions for a given starting piece
            for landing_index in neighbor_list:

                # If valid spot, make copy of board and move piece to landing index
                if board[landing_index] == 'x':
                    board_copy = board.copy()
                    board_copy[start_index] = 'x'
                    board_copy[landing_index] = 'W'

                    # Check if landing index causes mill
                    if close_mill(landing_index, board_copy):
                        generate_remove(board_copy, possible_boards)
                    else:
                        possible_boards.append(board_copy)

    return possible_boards

def close_mill(location_index, board):
    player_color = board[location_index]

    if player_color == 'x':
        return False

    elif location_index == 0:
        if board[6] == player_color and board[18] == player_color:
            return True

    elif location_index == 1:
        if board[11] == player_color and board[20] == player_color:
            return True

    elif location_index == 2:
        if board[7] == player_color and board[15] == player_color:
            return True

    elif location_index == 3:
        if board[10] == player_color and board[17] == player_color:
            return True

    elif location_index == 4:
        if board[8] == player_color and board[12] == player_color:
            return True

    elif location_index == 5:
        if board[9] == player_color and board[14] == player_color:
            return True

    elif location_index == 6:
        if board[0] == player_color and board[18] == player_color:
            return True

        elif board[7] == player_color and board[8] == player_color:
            return True

        else:
            return False

    elif location_index == 7:
        if board[2] == player_color and board[15] == player_color:
            return True

        elif board[6] == player_color and board[8] == player_color:
            return True

        else:
            return False

    elif location_index == 8:
        if board[12] == player_color and board[4] == player_color:
            return True

        elif board[6] == player_color and board[7] == player_color:
            return True

        else:
            return False

    elif location_index == 9:
        if board[14] == player_color and board[5] == player_color:
            return True

        elif board[10] == player_color and board[11] == player_color:
            return True

        else:
            return False

    elif location_index == 10:
        if board[17] == player_color and board[3] == player_color:
            return True

        elif board[9] == player_color and board[11] == player_color:
            return True

        else:
            return False

    elif location_index == 11:
        if board[9] == player_color and board[10] == player_color:
            return True

        elif board[20] == player_color and board[1] == player_color:
            return True

        else:
            return False

    elif location_index == 12:
        if board[8] == player_color and board[4] == player_color:
            return True

        elif board[13] == player_color and board[14] == player_color:
            return True

        else:
            return False

    elif location_index == 13:
        if board[12] == player_color and board[14] == player_color:
            return True

        elif board[16] == player_color and board[19] == player_color:
            return True

        else:
            return False

    elif location_index == 14:
        if board[12] == player_color and board[13] == player_color:
            return True

        elif board[9] == player_color and board[5] == player_color:
            return True

        else:
            return False

    elif location_index == 15:
        if board[7] == player_color and board[2] == player_color:
            return True

        elif board[16] == player_color and board[17] == player_color:
            return True

        else:
            return False

    elif location_index == 16:
        if board[15] == player_color and board[17] == player_color:
            return True

        elif board[19] == player_color and board[13] == player_color:
            return True

        else:
            return False

    elif location_index == 17:
        if board[16] == player_color and board[15] == player_color:
            return True

        elif board[10] == player_color and board[3] == player_color:
            return True

        else:
            return False

    elif location_index == 18:
        if board[6] == player_color and board[0] == player_color:
            return True

        elif board[19] == player_color and board[20] == player_color:
            return True

        else:
            return False

    elif location_index == 19:
        if board[18] == player_color and board[20] == player_color:
            return True

        elif board[16] == player_color and board[13] == player_color:
            return True

        else:
            return False

    else:
        if board[19] == player_color and board[18] == player_color:
            return True

        elif board[11] == player_color and board[1] == player_color:
            return True

        else:
            return False

    return False

def neighbors(location_index):
    if location_index == 0:
        return [1, 6]
    elif location_index == 1:
        return [0, 11]
    elif location_index == 2:
        return [3, 7]
    elif location_index == 3:
        return [2, 10]
    elif location_index == 4:
        return [5, 8]
    elif location_index == 5:
        return [4, 9]
    elif location_index == 6:
        return [0, 7, 18]
    elif location_index == 7:
        return [2, 6, 8, 15]
    elif location_index == 8:
        return [4, 7, 12]
    elif location_index == 9:
        return [5, 10, 14]
    elif location_index == 10:
        return [3, 9, 11, 17]
    elif location_index == 11:
        return [1, 10, 20]
    elif location_index == 12:
        return [8, 13]
    elif location_index == 13:
        return [12, 14, 16]
    elif location_index == 14:
        return [9, 13]
    elif location_index == 15:
        return [7, 16]
    elif location_index == 16:
        return [13, 15, 17, 19]
    elif location_index == 17:
        return [10, 16]
    elif location_index == 18:
        return [6, 19]
    elif location_index == 19:
        return [16, 18, 20]
    else:
        return [11, 19]

def count_pieces(board):
    num_white_pieces = 0
    num_black_pieces = 0

    for piece in board:
        if piece == 'W':
            num_white_pieces += 1
        if piece == 'B':
            num_black_pieces += 1

    return num_white_pieces, num_black_pieces

def swap_pieces(board):
    board_copy = board.copy()

    for index in range(0, len(board_copy)):
        if board_copy[index] == 'W':
            board_copy[index] = 'B'
        elif board_copy[index] == 'B':
            board_copy[index] = 'W'

    return board_copy

def static_estimation_opening(board):
    num_white_pieces, num_black_pieces = count_pieces(board)
    return num_white_pieces - num_black_pieces

def static_estimation_mid(board):
    num_white_pieces, num_black_pieces = count_pieces(board)

    if num_black_pieces <= 2:
        return 10000
    if num_white_pieces <= 2:
        return -10000

    # Get possible list of positions generated by black move
    swapped_board = swap_pieces(board)
    black_positions = generate_moves_mid(swapped_board)
    for board_index in range(0, len(black_positions)):
        black_positions[board_index] = swap_pieces(black_positions[board_index])

    num_black_moves = len(black_positions)

    if num_black_moves == 0:
        return 10000
    else:
        return 1000 * (num_white_pieces - num_black_pieces) - num_black_moves

def static_estimation_mid_improved(board):
    #
    # Win conditions
    #

    num_white_pieces, num_black_pieces = count_pieces(board)
    if num_black_pieces <= 2:
        return 10000
    if num_white_pieces <= 2:
        return -10000

    # Get possible list of positions generated by black move
    swapped_board = swap_pieces(board)
    black_positions = generate_moves_mid(swapped_board)
    for board_index in range(0, len(black_positions)):
        black_positions[board_index] = swap_pieces(black_positions[board_index])

    num_black_moves = len(black_positions)

    if num_black_moves == 0:
        return 10000

    # Amended advantageous board valuations
    else:
        static_estimate = 0

        three_way_white_over_black, four_way_white_over_black, upper_half_white_over_black = intersection_difference(
            board)

        # Value from having more valuable nodes than your opponent
        static_estimate += 60 * three_way_white_over_black
        static_estimate += 100 * four_way_white_over_black
        static_estimate += 50 * upper_half_white_over_black

        return 1000 * (num_white_pieces - num_black_pieces) - num_black_moves


def static_estimation_opening_improved(board):

    static_estimate = 0
    num_white_pieces, num_black_pieces = count_pieces(board)
    three_way_white_over_black, four_way_white_over_black, upper_half_white_over_black = intersection_difference(board)

    # Value from having more pieces than your opponent
    static_estimate += 20 * (num_white_pieces - num_black_pieces)

    # Value from having more valuable nodes than your opponent
    static_estimate += 2 * three_way_white_over_black
    static_estimate += 3 * four_way_white_over_black
    static_estimate += 1 * upper_half_white_over_black

    return static_estimate

def intersection_difference(board):

    three_way_white_over_black = 0
    four_way_white_over_black = 0
    upper_half_white_over_black = 0

    three_way_intersection = [6, 8, 9, 11, 13, 19]
    four_way_intersection = [7, 10, 16]
    upper_half = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    for index in three_way_intersection:
        if board[index] == 'W':
            three_way_white_over_black += 1
        elif board[index] == 'B':
            three_way_white_over_black -= 1

    for index in four_way_intersection:
        if board[index] == 'W':
            four_way_white_over_black += 1
        elif board[index] == 'B':
            four_way_white_over_black -= 1

    for index in upper_half:
        if board[index] == 'W':
            upper_half_white_over_black += 1
        elif board[index] == 'B':
            upper_half_white_over_black -= 1

    return three_way_white_over_black, four_way_white_over_black, upper_half_white_over_black

def output_board_to_txt(array, filename):
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Create a string by joining all elements of the array
    array_string = ''.join(map(str, array))

    # Write the string to a text file in the output directory
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as file:
        file.write(array_string)

def verify_input(array):
    if len(array) != 21:
        return False
    for element in array:
        if element != 'W' and element != 'B' and element != 'x':
            return False

    return True
