import sys


from utils import load_line_len, load_def_lines
from utils import line_len_is_valid, def_lines_are_valid
from utils import get_def_lines_vals
from utils import build_estim_vals

from sem_equacoes import quadrado_magico_sem_equacoes


def main():

    # Get command line arguments
    if len(sys.argv) > 2:
        sys.exit("Usage: python quadrado-magico.py [directory]")

    directory = sys.argv[1] if len(sys.argv) == 2 else ""

    # Load line length
    line_len = load_line_len(directory)

    # Set number of lines
    num_lines = line_len

    # Calculate max value
    max_value = num_lines * line_len

    # Calculate total number of values
    num_values = max_value

    # Calculate total sum of values
    total_sum = ((1 + max_value) * num_values) / 2

    # Calculate sum of values of each line
    line_sum = int(total_sum / num_lines)

    # Check if line length is valid
    if not line_len_is_valid(line_len, line_sum):
        sys.exit(f"Line length {line_len} is invalid")

    # Load defined lines
    def_lines = load_def_lines(directory, num_lines)

    # Check if defined lines are valid
    if not def_lines_are_valid(
            def_lines, line_len, num_lines, max_value, line_sum):

        sys.exit("Defined lines are invalid")

    # Calculate number of defined lines
    num_def_lines = len(def_lines)

    # Get defined lines values
    def_lines_vals = get_def_lines_vals(def_lines)

    # Calculate number of defined lines values
    num_def_lines_vals = len(def_lines_vals)

    # Build estimated values
    estim_vals = build_estim_vals(max_value, def_lines_vals)

    # Calculate number of estimated alues
    num_estim_vals = len(estim_vals)

    quadrado_magico_sem_equacoes(
        line_len, max_value, num_values, line_sum,
        def_lines, num_def_lines, num_def_lines_vals,
        num_estim_vals, estim_vals
        )


if __name__ == "__main__":
    main()
