# pos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
#        '20']

#
# print_board(positions2)
import MiniMaxOpening
import helper
import tkinter as tk
from PIL import ImageTk, Image
import os


def display_image():
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
    input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']

    # Function to draw a filled circle at the given coordinates
    def draw_filled_circle(x, y, color):
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

    # Function to handle mouse hover over a box
    def on_box_hover(event, index):
        canvas.itemconfig(box_objects[index], fill='blue')  # Change the box color on hover

    # Function to handle mouse hover out of a box
    def on_box_hover_out(event, index):
        canvas.itemconfig(box_objects[index], fill='')  # Reset the box color on hover out

    # Function to handle box click event
    def on_box_click(event, index):
        nonlocal input_board  # Declare input_board as nonlocal

        if input_board[index] != 'x':
            return  # Skip if the element is not 'x'

        if selected_option.get() == 'White':
            input_board[index] = 'W'  # Update the input board with 'W'
        elif selected_option.get() == 'Black':
            input_board[index] = 'B'  # Update the input board with 'B'

        clear_board()
        draw_board()
        print(input_board)  # Print the updated board

        AI_turn()

    def AI_turn():
        nonlocal input_board  # Declare input_board as nonlocal

        if selected_option.get() == 'White':
            AI_color = "Black"
        elif selected_option.get() == 'Black':
            AI_color = "White"

        input_board = MiniMaxOpening.MiniMaxOpening(input_board, AI_color)
        clear_board()
        draw_board()


    # Function to clear the board and delete the circles
    def clear_board():
        for circle in circle_objects:
            canvas.delete(circle)
        circle_objects.clear()

    # Function to draw the board with circles based on the input_board
    def draw_board():
        for index, element in enumerate(input_board):
            x, y = coordinates[index]
            draw_filled_circle(x, y, element)

    # Create the boxes on each coordinate
    for index, (x, y) in enumerate(coordinates):
        box = canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius,
                                      fill='', outline='', tags=index)

        canvas.tag_bind(box, '<Enter>', lambda event, i=index: on_box_hover(event, i))
        canvas.tag_bind(box, '<Leave>', lambda event, i=index: on_box_hover_out(event, i))
        canvas.tag_bind(box, '<Button-1>', lambda event, i=index: on_box_click(event, i))

        box_objects.append(box)  # Store the box object

    # Button click event handler
    def on_button_click():
        nonlocal input_board  # Declare input_board as nonlocal

        input_board = helper.read_file_contents()  # Load a new input board using helper.read_file_contents()
        if input_board is None or len(input_board) != len(coordinates):
            return  # Skip if the input board is invalid

        clear_board()
        draw_board()

    # Button click event handler
    def on_reset_click():
        nonlocal input_board  # Declare input_board as nonlocal

        input_board = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']

        clear_board()
        draw_board()

    # Create a sidebar frame
    sidebar_frame = tk.Frame(root)
    sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)  # Increase the padding

    # Create the load_board in the sidebar
    button = tk.Button(sidebar_frame, text="Load Board", command=on_button_click)
    button.pack(pady=10)

    # Create the label and dropdown menu in the sidebar
    label = tk.Label(sidebar_frame, text="Playing as: ")
    label.pack(pady=10)

    # Create the dropdown menu options
    options = ['White', 'Black']
    selected_option = tk.StringVar()
    selected_option.set(options[0])  # Set the initial selected option

    dropdown = tk.OptionMenu(sidebar_frame, selected_option, *options)
    dropdown.pack(pady=10)

    # Create the reset button in the sidebar
    button = tk.Button(sidebar_frame, text="Reset", command=on_reset_click)
    button.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()


# Call the function to display the image
display_image()

# coordinates = [(97, 847), (903, 846), (232, 712), (767, 709), (367, 576), (635, 577), (98, 443), (232, 443), (365, 444), (636, 444), (769, 444), (903, 442), (366, 311), (499, 308), (634, 309), (232, 176), (500, 174), (768, 175), (97, 41), (499, 42), (903, 41)]




# p = helper.read_file_contents()
#
# root = tk.Tk()
#
# button = tk.Button(root, text="Print Board", command=on_button_click)
# button.pack()
#
# root.mainloop()



#
# pos = helper.read_file_contents()
# helper.print_board(pos)
#
# # new = swap_pieces(pos)
# # print_board(new)
#
#
# possible = helper.generate_moves_mid(pos)
# print(possible)
# print(len(possible))
#
# for poss in possible:
#     helper.print_board(poss)
#
# helper.output_board_to_txt(possible[0], "output.txt")
