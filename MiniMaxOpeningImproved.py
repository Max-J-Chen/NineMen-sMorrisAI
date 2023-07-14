import minimax
import sys
import helper

max_depth = int(sys.argv[1])

minimax.minimax(max_depth=max_depth,
                phase=1,
                static_estimate=helper.static_estimation_opening_improved,
                output_file_name="MiniMaxOpeningOutput.txt",
                player_color="White")
