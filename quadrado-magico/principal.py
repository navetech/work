import sys


from utils import load_lines_len, load_def_lines
from utils import lines_len_is_valid, def_lines_are_valid
from utils import get_def_lines_vals
from utils import build_estim_vals

from sem_equacoes import quadrado_magico_sem_equacoes


def main():

    # Get command line arguments
    if len(sys.argv) > 2:
        sys.exit("Usage: python quadrado-magico.py [directory]")

    directory = sys.argv[1] if len(sys.argv) == 2 else ""

    # Load lines length
    lines_len = load_lines_len(directory)

    # Set number of lines
    num_lines = lines_len

    # Set number of rows and columns
    num_rows = num_lines
    num_columns = num_lines

    # Calculate number of values
    num_values = num_rows * num_columns

    # Calculate max value
    max_value = num_values

    # Calculate total sum of values
    total_sum = ((1 + max_value) * num_values) / 2

    # Calculate sum of values of each line
    lines_sum = int(total_sum / num_lines)

    # Check if line length is valid
    if not lines_len_is_valid(lines_len, lines_sum):
        sys.exit(f"Lines length {lines_len} is invalid")

    # Load defined lines
    def_lines = load_def_lines(directory, num_lines)

    # Check if defined lines are valid
    if not def_lines_are_valid(
            def_lines, lines_len, num_lines, max_value, lines_sum):

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
        lines_len, max_value, num_values, lines_sum,
        def_lines, num_def_lines, num_def_lines_vals,
        num_estim_vals, estim_vals
        )


if __name__ == "__main__":
    main()
