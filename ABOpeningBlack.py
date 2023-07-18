import alphabeta
import sys
import helper

max_depth = int(sys.argv[1])

alphabeta.alphabeta(max_depth=max_depth,
                    phase=1,
                    static_estimate=helper.static_estimation_opening,
                    output_file_name="ABOpeningOutput.txt",
                    player_color="Black")