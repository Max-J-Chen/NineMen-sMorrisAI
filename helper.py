import tkinter as tk
from tkinter import filedialog
import os

def read_file_contents():
    # Get the root directory of the executable
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Open file explorer dialog starting at the root directory
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=root_dir, filetypes=[("Text Files", "*.txt")])

    if not file_path:
        return None

    # Read file contents and split into an array
    with open(file_path, 'r') as file:
        contents = file.read()
        array = list(contents)

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

def generate_add(position):
    possible_boards = []

    # Iterate through possible empty locations and replace with W
    for loc in range(0, len(position)):
        if loc == "x":
            position_copy = position
            position_copy[loc] = 'W'

            # If there are 3 in a row, remove a black piece



    return possible_boards

def close_mill(location_ind, position):



    return None

def generate_remove(b, possible_boards):


    return None









pos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

#
# print_board(positions2)

# position = read_file_contents()
print_board(pos)
#generate_add(pos)
