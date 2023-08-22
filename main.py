import queue
import alphabeta
import minimax
import helper
import tkinter as tk
from PIL import Image, ImageTk
import os
import threading


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
    canvas.create_image(0, 0, anchor=tk.NW, image=board_image)

    # Define the circle parameters
    radius = 20

    # Array of x-y coordinates corresponding to the ordered array
    coordinates = [(97, 847), (903, 846), (232, 712), (767, 709), (367, 576), (635, 577), (98, 443), (232, 443),
                   (365, 444), (636, 444), (769, 444), (903, 442), (366, 311), (499, 308), (634, 309), (232, 176),
                   (500, 174), (768, 175), (97, 41), (499, 42), (903, 41)]

    # List to store the player pieces
    player_pieces = []

    # List to store the ghost pieces that indicate if a player can place a piece at a position
    ghost_pieces = []

    # Ordered array of size 21 with elements 'x', 'W', or 'B'
    input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
                   'x']

    # Turn count for changing AI modes
    turn_count = 0

    # Create a queue to receive the results of AI
    result_queue = queue.Queue()

    # Create a tree variable to hold previous trees
    tree = None

    # Function to draw a filled circle at the given coordinates
    def draw_filled_circle(x, y, color, index):
        if color == 'W':
            circle_color = 'white'
            outline_color = 'black'
            outline_width = 6  # Three times as thick outline for white circles
        elif color == 'B':
            circle_color = 'black'
            outline_color = 'black'
            outline_width = 2
        else:
            return  # Skip drawing if the color is 'x'

        circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                    fill=circle_color, outline=outline_color, width=outline_width)

        player_pieces.append(circle)  # Store the circle object

        # Bind the click event to the circle
        canvas.tag_bind(circle, '<Button-1>', lambda event, i=index: on_circle_click(event, i))

    # Function to handle circle click event
    def on_circle_click(event, index):
        if input_board[index] != 'x':
            # Replace the element in the input_board array with 'x'
            input_board[index] = 'x'
            clear_board()
            draw_player_pieces()

            print(input_board)

    # Function to handle mouse hover over a box
    def on_box_hover(event, index):
        if input_board[index] == 'x':
            canvas.itemconfig(ghost_pieces[index], fill='red')  # Change the box color on hover
            canvas.tag_raise(ghost_pieces[index])  # Raise the box to be on top

    # Function to handle mouse hover out of a box
    def on_box_hover_out(event, index):
        if input_board[index] == 'x':
            canvas.itemconfig(ghost_pieces[index], fill='', outline='')  # Reset the box color
        else:
            canvas.itemconfig(ghost_pieces[index], fill='',
                              outline='')  # Keep the box color for non-'x' elements

    # Function to handle box click event
    def on_box_click(event, index):
        if input_board[index] != 'x':
            return  # Skip if the element is not 'x'

        if selected_option.get() == 'White':
            input_board[index] = 'W'  # Update the input board with 'W'
        elif selected_option.get() == 'Black':
            input_board[index] = 'B'  # Update the input board with 'B'

        clear_board()
        draw_player_pieces()
        print(''.join(map(str, input_board)))  # Print the updated board

    # Function to clear the board and delete the circles
    def clear_board():
        nonlocal ghost_pieces

        for circle in player_pieces:
            canvas.delete(circle)
        player_pieces.clear()

        # for box in ghost_pieces:
        #     print("Deleted ghost piece")
        #     canvas.delete(box)
        # ghost_pieces = []

    def draw_ghost_pieces():
        for index, element in enumerate(input_board):
            x, y = coordinates[index]

            if element == 'x':
                box = canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius,
                                              fill='', outline='', tags=index)
                canvas.tag_bind(box, '<Enter>', lambda event, i=index: on_box_hover(event, i))
                canvas.tag_bind(box, '<Leave>', lambda event, i=index: on_box_hover_out(event, i))
                canvas.tag_bind(box, '<Button-1>', lambda event, i=index: on_box_click(event, i))
                ghost_pieces.append(box)  # Store the box object

    draw_ghost_pieces()

    # Function to draw the board with circles based on the input_board
    def draw_player_pieces():
        nonlocal input_board
        for index, element in enumerate(input_board):
            x, y = coordinates[index]
            draw_filled_circle(x, y, element, index)

    # Create the boxes on each coordinate
    draw_player_pieces()

    def on_clear_board_button():
        nonlocal tree
        nonlocal input_board
        nonlocal turn_count

        input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
                       'x', 'x']
        tree = None
        turn_count = 0
        clear_board()
        draw_player_pieces()
        update_label_text()
        AI_heuristic.set(options2[0])

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
        if turn_count != 0 or selected_option.get() == 'White':
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

        if turn_count > 16:
            AI_heuristic.set(options2[7])

        update_label_text()

        # If we got the result, update the GUI
        clear_board()
        draw_player_pieces()

    def run_AI(return_queue):
        nonlocal input_board
        nonlocal tree

        AI_board = None
        i = int(field_entry.get())

        if AI_heuristic.get() == 'ABGameImproved':
            if selected_option.get() == 'White':
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
            if selected_option.get() == 'White':
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
            if selected_option.get() == 'White':
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

    # Create a sidebar frame
    sidebar_frame = tk.Frame(root)
    sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)  # Increase the padding

    # Create the button in the sidebar
    load_board_button = tk.Button(sidebar_frame, text="Load Board", command=on_load_board_button, width=20)
    load_board_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    # Create the button in the sidebar
    clear_board_button = tk.Button(sidebar_frame, text="Clear Board", command=on_clear_board_button, width=20)
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
    options = ['White', 'Black']
    selected_option = tk.StringVar()
    selected_option.set(options[0])  # Set the initial selected option

    dropdown = tk.OptionMenu(sidebar_frame, selected_option, *options)
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
