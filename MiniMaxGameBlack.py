import minimax
import sys
import helper

max_depth = int(sys.argv[1])

minimax.minimax(max_depth=max_depth,
                phase=2,
                static_estimate=helper.static_estimation_mid,
                output_file_name="MiniMaxGameOutput.txt",
                player_color="Black")
