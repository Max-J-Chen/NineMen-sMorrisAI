import queue
import alphabeta
import minimax
import helper
import tkinter as tk
from PIL import Image, ImageTk
import os
import threading
import copy


def display_UI():
    root = tk.Tk()
    root.title("Nine Men's Morris Variant")
    root.resizable(False, False)

    # Get the path to the image
    image_path = os.path.join(os.path.dirname(__file__), 'resources', 'MorrisBoardBlank.jpg')

    # Load the image
    image = Image.open(image_path)

    # Create a Tkinter-compatible photo image
    board_image = ImageTk.PhotoImage(image)

    # Create a canvas with the image
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack(side=tk.LEFT)

    # Display the image on the canvas
    clickable_board = canvas.create_image(0, 0, anchor=tk.NW, image=board_image)
    canvas.tag_bind(clickable_board, '<Button-1>', lambda event: on_arb_click(event))

    # Define the circle parameters
    radius = 20
    large_radius = 35
    white_outline_width = 6
    black_outline_width = 2
    large_white_outline_width = 8
    large_black_outline_width = 3
    color_grey = "#808080"  # Hexadecimal color code for grey
    color_light_grey = "#D3D3D3"  # Hexadecimal color code for light grey

    # Array of x-y coordinates corresponding to the ordered array
    coordinates = [(97, 847), (903, 846), (232, 712), (767, 709), (367, 576), (635, 577), (98, 443), (232, 443),
                   (365, 444), (636, 444), (769, 444), (903, 442), (366, 311), (499, 308), (634, 309), (232, 176),
                   (500, 174), (768, 175), (97, 41), (499, 42), (903, 41)]

    # List to store the player pieces
    player_pieces = []

    # List to store the ghost pieces that indicate if a player can place a piece at a position
    hover_boundaries = []

    # Ordered array of size 21 with elements 'x', 'W', or 'B'
    input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
                   'x']

    # Turn count for changing AI modes
    turn_count = 0
    current_turn_player = ''
    piece_selected = None
    remove_mode = False
    is_player_turn = True

    # Create a queue to receive the results of AI
    result_queue = queue.Queue()

    # Create a tree variable to hold previous trees
    tree = None

    # Function to draw a filled circle at the given coordinates
    def draw_white_piece(x, y, index):
        canvas.coords(player_pieces[index], x - radius, y - radius, x + radius, y + radius)
        canvas.itemconfig(player_pieces[index], fill='white', outline='black', width=6)

    def draw_black_piece(x, y, index):
        canvas.coords(player_pieces[index], x - radius, y - radius, x + radius, y + radius)
        canvas.itemconfig(player_pieces[index], fill='black', outline='black', width=2)

    def draw_white_ghost_piece(x, y, index):
        canvas.coords(player_pieces[index], x - radius, y - radius, x + radius, y + radius)
        canvas.itemconfig(player_pieces[index], fill=color_light_grey, outline=color_grey, width=white_outline_width)

    def draw_black_ghost_piece(x, y, index):
        canvas.coords(player_pieces[index], x - radius, y - radius, x + radius, y + radius)
        canvas.itemconfig(player_pieces[index], fill=color_grey, outline=color_grey, width=black_outline_width)

    def draw_white_piece_large(x, y, index):
        canvas.coords(player_pieces[index], x - large_radius, y - large_radius, x + large_radius, y + large_radius)
        canvas.itemconfig(player_pieces[index], fill='white', outline='black', width=large_white_outline_width)

    def draw_black_piece_large(x, y, index):
        canvas.coords(player_pieces[index], x - large_radius, y - large_radius, x + large_radius, y + large_radius)
        canvas.itemconfig(player_pieces[index], fill='black', outline='black', width=large_black_outline_width)

    def hide_piece(x, y, index):
        canvas.coords(player_pieces[index], x - radius, y - radius, x + radius, y + radius)
        canvas.itemconfig(player_pieces[index], fill='', outline='', width=0)

    # Initialize board with player piece objects that are initially invisible
    def initialize_player_pieces():
        for index, player_color in enumerate(input_board):
            x, y = coordinates[index]
            piece = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='', outline='', width=6)
            player_pieces.append(piece)  # Store the circle object

    initialize_player_pieces()

    # Draw the board with circles based on the input_board
    def draw_player_pieces():
        nonlocal input_board
        for index, player_color in enumerate(input_board):
            x, y = coordinates[index]
            if player_color == 'W':
                draw_white_piece(x, y, index)
            elif player_color == 'B':
                draw_black_piece(x, y, index)
            else:
                hide_piece(x, y, index)

    # Create the boxes on each coordinate
    draw_player_pieces()

    def draw_single_piece(x, y, index):
        player_color = input_board[index]
        if player_color == 'W':
            draw_white_piece(x, y, index)
        elif player_color == 'B':
            draw_black_piece(x, y, index)
        else:
            hide_piece(x, y, index)

    # Function to handle mouse hover over a box
    def on_coordinate_hover(event, index):

        player_color = player_color_dropdown.get()
        input_board_piece = input_board[index]
        x, y = coordinates[index]
        nonlocal remove_mode
        # If statement here that prevents hovering at all if it is not the player's turn

        # Highlight potential pieces that can be removed in remove mode
        if remove_mode:
            # Prevent player from removing any pieces in a mill
            if not helper.close_mill(index, input_board):
                if player_color_dropdown.get() == 'White' and input_board[index] == 'B':
                    draw_black_piece_large(x, y, index)
                elif player_color_dropdown.get() == 'Black' and input_board[index] == 'W':
                    draw_white_piece_large(x, y, index)
                return

        ###############################################################################################################
        # PHASE 1 LOGIC
        ###############################################################################################################
        if get_phase() == 1:
            # Draw a ghost piece if the hover box is associated with an empty position
            if input_board_piece == 'x':
                if player_color == "White":
                    draw_white_piece(x, y, index)
                else:
                    draw_black_piece(x, y, index)

        ###############################################################################################################
        # PHASE 2 LOGIC
        ###############################################################################################################
        else:
            # Make player's own piece large if a piece already not selected
            if not is_piece_selected():
                if input_board_piece == 'W' and player_color == "White":
                    draw_white_piece_large(x, y, index)
                elif input_board_piece == 'B' and player_color == "Black":
                    draw_black_piece_large(x, y, index)
            elif helper.is_move_legal(piece_selected, index, input_board):
                if player_color == "White":
                    draw_white_piece(x, y, index)
                else:
                    draw_black_piece(x, y, index)

            # if player has not clicked on their own piece yet, then
            # when hovering over their own pieces only, then make those pieces bigger

            # Hovering over existing pieces that are the same color as the player makes them bigger but the same color
            # Clicking those pieces makes the piece pulse, clicking an invalid coordinate or anywhere else on board will cancel the selection
            # If player clicks a valid opposing piece to take, then remove that piece and place player piece there
            # Else deletes player piece at origin coordinate and place player piece in destination coordinate
            # Need to make a function in helper that determines the valid moves given a specific coordinate, I might have a function like that already

    # Function to handle mouse hover out of a box
    def on_coordinate_hover_out(event, index):
        # draw_player_pieces()
        if is_piece_selected():
            if input_board[index] == 'x':
                x, y = coordinates[index]
                draw_single_piece(x, y, index)
            return
        else:
            x, y = coordinates[index]
            draw_single_piece(x, y, index)

    # Function to handle box click event
    def on_coordinate_click(event, index):
        nonlocal piece_selected
        nonlocal remove_mode
        print("COORD CLICK")
        if remove_mode:
            # Prevent player from removing any pieces in a mill
            if not helper.close_mill(index, input_board):
                if player_color_dropdown.get() == 'White' and input_board[index] == 'B' or player_color_dropdown.get() == 'Black' and input_board[index] == 'W':
                    input_board[index] = 'x'
                    remove_mode = False
                    draw_player_pieces()
                    on_end_turn_button()
                    return

        if get_phase() == 1:
            if player_color_dropdown.get() == 'White':
                input_board[index] = 'W'  # Update the input board with 'W'
            elif player_color_dropdown.get() == 'Black':
                input_board[index] = 'B'  # Update the input board with 'B'
            draw_player_pieces()
            print(''.join(map(str, input_board)))  # Print the updated board
            if check_mill(index):
                return
            on_end_turn_button()
        else:
            # Check if its the players turn
            # If player turn, check if they selected one of their pieces
            x, y = coordinates[index]
            if player_color_dropdown.get() == 'White' and input_board[index] == 'W':
                # Player cannot click on another white piece while in selected mode
                if is_piece_selected():
                    on_arb_click(None)
                else:
                    piece_selected = index
                    draw_white_ghost_piece(x, y, index)
            elif player_color_dropdown.get() == 'Black' and input_board[index] == 'B':
                if is_piece_selected():
                    on_arb_click(None)
                else:
                    piece_selected = index
                    draw_black_ghost_piece(x, y, index)

            # Check if player selected a valid landing position
            elif helper.is_move_legal(piece_selected, index, input_board):
                if player_color_dropdown.get() == 'White':
                    input_board[index] = 'W'
                else:
                    input_board[index] = 'B'

                input_board[piece_selected] = 'x'
                draw_player_pieces()
                on_arb_click(None)
                if check_mill(index):
                    return
                on_end_turn_button()
            else:
                on_arb_click(None)

    def check_mill(index):
        nonlocal remove_mode
        if helper.close_mill(index, input_board):
            remove_mode = True
            return True
        else:
            return False

    def is_piece_selected():
        nonlocal piece_selected
        if piece_selected is None:
            return False
        else:
            return True

    def on_arb_click(event):
        nonlocal piece_selected
        piece_selected = None
        draw_player_pieces()
        print("ARB CLICK")

    # Hover Boundaries will be used to determine on_hover, hover_off, and on_click events.
    def draw_hover_boundaries():
        for index, element in enumerate(input_board):
            x, y = coordinates[index]
            h_bound = canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                         fill='', outline='', width=0, tags=str(index))

            canvas.tag_bind(h_bound, '<Enter>', lambda event, i=index: on_coordinate_hover(event, i))
            canvas.tag_bind(h_bound, '<Leave>', lambda event, i=index: on_coordinate_hover_out(event, i))
            canvas.tag_bind(h_bound, '<Button-1>', lambda event, i=index: on_coordinate_click(event, i))
            hover_boundaries.append(h_bound)  # Store the box object

    draw_hover_boundaries()

    # Function to clear the board and delete the circles
    def clear_board():
        nonlocal tree
        nonlocal input_board
        nonlocal turn_count

        input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
                       'x', 'x']
        tree = None
        turn_count = 0
        update_label_text()
        AI_heuristic.set(options2[0])

        draw_player_pieces()

    # Button click event handler
    def on_load_board_button():
        nonlocal input_board  # Declare input_board as nonlocal

        input_board = helper.read_file_contents()  # Load a new input board using helper.read_file_contents()
        if input_board is None or len(input_board) != len(coordinates):
            return  # Skip if the input board is invalid

        clear_board()
        draw_player_pieces()

    def on_end_turn_button():

        nonlocal input_board
        nonlocal turn_count

        # Don't increment turn count if starting first move as black
        if turn_count != 0 or player_color_dropdown.get() == 'White':
            turn_count += 1

        update_label_text()

        thread = threading.Thread(target=run_AI, args=(result_queue,))
        thread.start()

        check_result()

    def check_result():
        nonlocal input_board
        nonlocal result_queue
        nonlocal turn_count

        try:
            # Attempt to get the result from the queue
            AI_board = result_queue.get(block=False)
            turn_count += 1
            input_board = AI_board

        except queue.Empty:
            # If the queue is empty, re-check after 100 milliseconds
            root.after(100, check_result)
            return

        if turn_count >= 16:
            AI_heuristic.set(options2[1])

        update_label_text()

        # If we got the result, update the GUI
        # clear_board()
        draw_player_pieces()

    def run_AI(return_queue):
        nonlocal input_board
        nonlocal tree

        AI_board = None
        i = int(field_entry.get())

        if AI_heuristic.get() == 'ABGameImproved':
            if player_color_dropdown.get() == 'White':
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=2,
                                                     static_estimate=helper.static_estimation_mid_improved,
                                                     output_file_name="ABGameOutputImproved.txt",
                                                     player_color="Black",
                                                     pos=input_board,
                                                     turn_count=turn_count)
            else:
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=2,
                                                     static_estimate=helper.static_estimation_mid_improved,
                                                     output_file_name="ABGameOutputImproved.txt",
                                                     player_color="White",
                                                     pos=input_board,
                                                     turn_count=turn_count)
        elif AI_heuristic.get() == 'ABOpeningImproved':
            if player_color_dropdown.get() == 'White':
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=1,
                                                     static_estimate=helper.static_estimation_opening_improved,
                                                     output_file_name="ABGameOpeningImproved.txt",
                                                     player_color="Black",
                                                     pos=input_board,
                                                     turn_count=turn_count)
            else:
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=1,
                                                     static_estimate=helper.static_estimation_opening_improved,
                                                     output_file_name="ABGameOpeningImproved.txt",
                                                     player_color="White",
                                                     pos=input_board,
                                                     turn_count=turn_count)
        else:
            if player_color_dropdown.get() == 'White':
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=2,
                                                     static_estimate=helper.static_estimation_mid,
                                                     output_file_name="ABGameOutput.txt",
                                                     player_color="Black",
                                                     pos=input_board)
            else:
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=2,
                                                     static_estimate=helper.static_estimation_mid,
                                                     output_file_name="ABGameOutput.txt",
                                                     player_color="White",
                                                     pos=input_board)

        return_queue.put(AI_board, tree)

    def update_label_text():
        turn_count_label.config(text="Turn Count: " + str(turn_count))
        turns_left_label.config(text="Phase 1 Remaining Turns: " + str(16 - turn_count))

    def get_phase():
        return 1 if AI_heuristic.get() == "ABOpeningImproved" else 2

    # Create a sidebar frame
    sidebar_frame = tk.Frame(root)
    sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)  # Increase the padding

    # Create the button in the sidebar
    load_board_button = tk.Button(sidebar_frame, text="Load Board", command=on_load_board_button, width=20)
    load_board_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    # Create the button in the sidebar
    clear_board_button = tk.Button(sidebar_frame, text="Clear Board", command=clear_board, width=20)
    clear_board_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    # Create the button in the sidebar
    end_turn_button = tk.Button(sidebar_frame, text="End Turn", command=on_end_turn_button, width=20)
    end_turn_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    # Create the label and dropdown menu in the sidebar
    AI_heuristic_label = tk.Label(sidebar_frame, text="AI Type: ")
    AI_heuristic_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    # Create the dropdown menu options
    options2 = ['ABOpeningImproved', 'ABGameImproved']
    AI_heuristic = tk.StringVar()
    AI_heuristic.set(options2[0])  # Set the initial selected option

    dropdown = tk.OptionMenu(sidebar_frame, AI_heuristic, *options2)
    dropdown.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

    # Create the field in the sidebar
    field_label = tk.Label(sidebar_frame, text="Enter a depth value:", width=20)
    field_label.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

    # Create the field in the sidebar
    default_value = 4  # Set the default value

    field_entry = tk.Entry(sidebar_frame, width=20)
    field_entry.insert(tk.END, str(default_value))  # Insert the default value into the entry widget
    field_entry.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

    # Create the label for player color
    turn_count_label = tk.Label(sidebar_frame, text="Play as: ", width=20)
    turn_count_label.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

    # Create the dropdown menu options
    player_color_options = ['White', 'Black']
    player_color_dropdown = tk.StringVar()
    player_color_dropdown.set(player_color_options[0])  # Set the initial selected option

    dropdown = tk.OptionMenu(sidebar_frame, player_color_dropdown, *player_color_options)
    dropdown.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

    # Create the label and dropdown menu in the sidebar
    turn_count_label = tk.Label(sidebar_frame, text="Turn Count: " + str(turn_count), width=20)
    turn_count_label.grid(row=12, column=0, padx=5, pady=5, sticky="ew")

    # Create the label and dropdown menu in the sidebar
    turns_left_label = tk.Label(sidebar_frame, text="Phase 1 Remaining Turns: " + str(16 - turn_count), width=20)
    turns_left_label.grid(row=13, column=0, padx=5, pady=5, sticky="ew")

    # Run the Tkinter event loop
    root.mainloop()


# Call the function to display the image
display_UI()
