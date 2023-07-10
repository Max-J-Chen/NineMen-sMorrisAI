# pos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
#        '20']

#
# print_board(positions2)
import helper

pos = helper.read_file_contents()
helper.print_board(pos)

# new = swap_pieces(pos)
# print_board(new)


possible = helper.generate_moves_mid(pos)
print(possible)
print(len(possible))

for poss in possible:
    helper.print_board(poss)

helper.output_board_to_txt(possible[0], "output.txt")