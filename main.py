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
    root.title("Image Display")

    # Get the path to the image
    image_path = os.path.join(os.path.dirname(__file__), 'resources', 'MorrisBoardBlank.jpg')

    # Load the image
    image = Image.open(image_path)

    # Create a Tkinter-compatible photo image
    photo = ImageTk.PhotoImage(image)

    # Create a canvas with the image
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack(side=tk.LEFT)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Define the circle parameters
    radius = 20

    # Array of x-y coordinates corresponding to the ordered array
    coordinates = [(97, 847), (903, 846), (232, 712), (767, 709), (367, 576), (635, 577), (98, 443), (232, 443),
                   (365, 444), (636, 444), (769, 444), (903, 442), (366, 311), (499, 308), (634, 309), (232, 176),
                   (500, 174), (768, 175), (97, 41), (499, 42), (903, 41)]

    # List to store the circle objects
    circle_objects = []

    # List to store the box objects
    box_objects = []

    # Ordered array of size 21 with elements 'x', 'W', or 'B'
    input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
                   'x']

    # Piece counts for changing AI modes
    white_piece_count = 0
    black_piece_count = 0

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

        circle_objects.append(circle)  # Store the circle object

        # Bind the click event to the circle
        canvas.tag_bind(circle, '<Button-1>', lambda event, i=index: on_circle_click(event, i))

    # Function to handle circle click event
    def on_circle_click(event, index):
        if input_board[index] != 'x':
            # Replace the element in the input_board array with 'x'
            input_board[index] = 'x'
            clear_board()
            draw_board()

            print(input_board)

    # Function to handle mouse hover over a box
    def on_box_hover(event, index):
        if input_board[index] == 'x':
            canvas.itemconfig(box_objects[index], fill='')  # Change the box color on hover
            canvas.tag_raise(box_objects[index])  # Raise the box to be on top

    # Function to handle mouse hover out of a box
    def on_box_hover_out(event, index):
        if input_board[index] == 'x':
            canvas.itemconfig(box_objects[index], fill='', outline='')  # Reset the box color
        else:
            canvas.itemconfig(box_objects[index], fill='',
                              outline='')  # Keep the box color for non-'x' elements

    # Function to handle box click event
    def on_box_click(event, index):
        if input_board[index] != 'x':
            return  # Skip if the element is not 'x'

        if selected_option.get() == 'White':
            input_board[index] = 'W'  # Update the input board with 'W'
        elif selected_option.get() == 'Black':
            input_board[index] = 'B'  # Update the input board with 'B'

        # Delete the box object from the canvas
        canvas.delete(box_objects[index])

        clear_board()
        draw_board()
        print(input_board)  # Print the updated board

    # Function to clear the board and delete the circles
    def clear_board():
        for circle in circle_objects:
            canvas.delete(circle)
        circle_objects.clear()

        for box in box_objects:
            canvas.delete(box)

    # Function to draw the board with circles based on the input_board
    def draw_board():

        nonlocal input_board

        for index, element in enumerate(input_board):
            x, y = coordinates[index]
            draw_filled_circle(x, y, element, index)

            if element == 'x':
                box = canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius,
                                              fill='', outline='', tags=index)

                canvas.tag_bind(box, '<Enter>', lambda event, i=index: on_box_hover(event, i))
                canvas.tag_bind(box, '<Leave>', lambda event, i=index: on_box_hover_out(event, i))
                canvas.tag_bind(box, '<Button-1>', lambda event, i=index: on_box_click(event, i))

                box_objects.append(box)  # Store the box object

    # Create the boxes on each coordinate
    draw_board()

    def on_clear_board_button():
        nonlocal tree
        nonlocal input_board
        nonlocal white_piece_count
        nonlocal black_piece_count

        input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x','x','x']
        tree = None

        white_piece_count = 0
        black_piece_count = 0

        clear_board()
        draw_board()

        update_label_text()

        AI_heuristic.set(options2[6])

    # Button click event handler
    def on_load_board_button():
        nonlocal input_board  # Declare input_board as nonlocal

        input_board = helper.read_file_contents()  # Load a new input board using helper.read_file_contents()
        if input_board is None or len(input_board) != len(coordinates):
            return  # Skip if the input board is invalid

        clear_board()
        draw_board()

    def on_end_turn_button():

        nonlocal input_board

        thread = threading.Thread(target=run_AI, args=(result_queue,))
        thread.start()

        check_result()

    def check_result():
        nonlocal input_board
        nonlocal result_queue
        nonlocal white_piece_count
        nonlocal black_piece_count

        try:
            white_old_count = input_board.count('W')
            black_old_count = input_board.count('B')

            # Attempt to get the result from the queue
            AI_board = result_queue.get(block=False)

            white_new_count = AI_board.count('W')
            black_new_count = AI_board.count('B')

            if white_new_count > white_old_count:
                white_piece_count += 1

            if black_new_count > black_old_count:
                black_piece_count += 1

            input_board = AI_board

        except queue.Empty:
            # If the queue is empty, re-check after 100 milliseconds
            root.after(100, check_result)
            return

        if black_piece_count > 7 or white_piece_count > 7:
            AI_heuristic.set(options2[7])

        update_label_text()

        # If we got the result, update the GUI
        clear_board()
        draw_board()

    def set_manual_entry():
        nonlocal input_board
        array = list(manual_entry.get())
        if helper.verify_input(array):
            input_board = array

        clear_board()
        draw_board()

    def run_AI(return_queue):

        nonlocal input_board
        nonlocal tree
        nonlocal white_piece_count
        nonlocal black_piece_count

        AI_board = None
        i = int(field_entry.get())

        if AI_heuristic.get() == 'MiniMaxOpening':
            if selected_option.get() == 'White':
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=1,
                                                 static_estimate=helper.static_estimation_opening,
                                                 output_file_name="MiniMaxOpeningOutput.txt",
                                                 player_color="Black",
                                                 pos=input_board)
            else:
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=1,
                                                 static_estimate=helper.static_estimation_opening,
                                                 output_file_name="MiniMaxOpeningOutput.txt",
                                                 player_color="White",
                                                 pos=input_board)

        elif AI_heuristic.get() == 'MiniMaxGame':
            if selected_option.get() == 'White':
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=2,
                                                 static_estimate=helper.static_estimation_mid,
                                                 output_file_name="MiniMaxGameOutput.txt",
                                                 player_color="Black",
                                                 pos=input_board)
            else:
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=2,
                                                 static_estimate=helper.static_estimation_mid,
                                                 output_file_name="MiniMaxGameOutput.txt",
                                                 player_color="White",
                                                 pos=input_board)
        elif AI_heuristic.get() == 'ABOpening':
            if selected_option.get() == 'White':
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=1,
                                                     static_estimate=helper.static_estimation_opening,
                                                     output_file_name="ABOpeningOutput.txt",
                                                     player_color="Black",
                                                     pos=input_board)
            else:
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=1,
                                                     static_estimate=helper.static_estimation_opening,
                                                     output_file_name="ABOpeningOutput.txt",
                                                     player_color="White",
                                                     pos=input_board)
        elif AI_heuristic.get() == 'MiniMaxOpeningImproved':
            if selected_option.get() == 'White':
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=1,
                                                 static_estimate=helper.static_estimation_opening_improved,
                                                 output_file_name="MiniMaxOpeningOutputImproved.txt",
                                                 player_color="Black",
                                                 pos=input_board)
            else:
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=1,
                                                 static_estimate=helper.static_estimation_opening_improved,
                                                 output_file_name="MiniMaxOpeningOutputImproved.txt",
                                                 player_color="White",
                                                 pos=input_board)
        elif AI_heuristic.get() == 'MiniMaxGameImproved':
            if selected_option.get() == 'White':
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=2,
                                                 static_estimate=helper.static_estimation_mid_improved,
                                                 output_file_name="MiniMaxGameOutputImproved.txt",
                                                 player_color="Black",
                                                 pos=input_board)
            else:
                AI_board, tree = minimax.minimax(max_depth=i,
                                                 phase=2,
                                                 static_estimate=helper.static_estimation_mid_improved,
                                                 output_file_name="MiniMaxGameOutputImproved.txt",
                                                 player_color="White",
                                                 pos=input_board)
        elif AI_heuristic.get() == 'ABGameImproved':
            if selected_option.get() == 'White':
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=2,
                                                     static_estimate=helper.static_estimation_mid_improved,
                                                     output_file_name="ABGameOutputImproved.txt",
                                                     player_color="Black",
                                                     pos=input_board,
                                                     black_turn_number=black_piece_count)
            else:
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=2,
                                                     static_estimate=helper.static_estimation_mid_improved,
                                                     output_file_name="ABGameOutputImproved.txt",
                                                     player_color="White",
                                                     pos=input_board,
                                                     black_turn_number=black_piece_count)
        elif AI_heuristic.get() == 'ABOpeningImproved':
            if selected_option.get() == 'White':
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=1,
                                                     static_estimate=helper.static_estimation_opening_improved,
                                                     output_file_name="ABGameOpeningImproved.txt",
                                                     player_color="Black",
                                                     pos=input_board,
                                                     black_turn_number=black_piece_count)
            else:
                AI_board, tree = alphabeta.alphabeta(max_depth=i,
                                                     phase=1,
                                                     static_estimate=helper.static_estimation_opening_improved,
                                                     output_file_name="ABGameOpeningImproved.txt",
                                                     player_color="White",
                                                     pos=input_board,
                                                     black_turn_number=black_piece_count)
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
        white_piece_count_label.config(text="White Pieces Placed: " + str(white_piece_count))
        black_piece_count_label.config(text="Black Pieces Placed: " + str(black_piece_count))

    # Create a sidebar frame
    sidebar_frame = tk.Frame(root)
    sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)  # Increase the padding

    # Create the button in the sidebar
    load_board_button = tk.Button(sidebar_frame, text="Load Board", command=on_load_board_button)
    load_board_button.pack(pady=10)

    # Create the button in the sidebar
    end_turn_button = tk.Button(sidebar_frame, text="End Turn", command=on_end_turn_button)
    end_turn_button.pack(pady=10)

    # Create the button in the sidebar
    clear_board_button = tk.Button(sidebar_frame, text="Clear Board", command=on_clear_board_button)
    clear_board_button.pack(pady=10)

    # Create the label and dropdown menu in the sidebar
    AI_heuristic_label = tk.Label(sidebar_frame, text="AI Type: ")
    AI_heuristic_label.pack(pady=10)

    # Create the dropdown menu options
    options2 = ['MiniMaxOpening', 'MiniMaxGame', 'ABOpening', 'ABGame', 'MiniMaxOpeningImproved', 'MiniMaxGameImproved',
                'ABOpeningImproved', 'ABGameImproved']
    AI_heuristic = tk.StringVar()
    AI_heuristic.set(options2[6])  # Set the initial selected option

    dropdown = tk.OptionMenu(sidebar_frame, AI_heuristic, *options2)
    dropdown.pack(pady=10)

    # Create the label and dropdown menu in the sidebar
    AI_heuristic_label = tk.Label(sidebar_frame, text="Playing as: ")
    AI_heuristic_label.pack(pady=10)

    # Create the dropdown menu options
    options = ['White', 'Black']
    selected_option = tk.StringVar()
    selected_option.set(options[0])  # Set the initial selected option

    dropdown = tk.OptionMenu(sidebar_frame, selected_option, *options)
    dropdown.pack(pady=10)

    # Create the field in the sidebar
    field_label = tk.Label(sidebar_frame, text="Enter a value:")
    field_label.pack(pady=10)

    # Create the field in the sidebar
    default_value = 4  # Set the default value

    field_entry = tk.Entry(sidebar_frame)
    field_entry.insert(tk.END, default_value)  # Insert the default value into the entry widget
    field_entry.pack(pady=10)

    manual_input_field = tk.Label(sidebar_frame, text="Manual Input:")
    manual_input_field.pack(pady=10)

    manual_entry = tk.Entry(sidebar_frame)
    manual_entry.insert(tk.END, "")  # Insert the default value into the entry widget
    manual_entry.pack(pady=10)

    # Create the button in the sidebar
    manual_entry_button = tk.Button(sidebar_frame, text="Confirm Board", command=set_manual_entry)
    manual_entry_button.pack(pady=10)

    # Create the label and dropdown menu in the sidebar
    white_piece_count_label = tk.Label(sidebar_frame, text="White Pieces Placed: " + str(white_piece_count))
    white_piece_count_label.pack(pady=10)

    # Create the label and dropdown menu in the sidebar
    black_piece_count_label = tk.Label(sidebar_frame, text="Black Pieces Placed: " + str(black_piece_count))
    black_piece_count_label.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()


# Call the function to display the image
display_UI()
