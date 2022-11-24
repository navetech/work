import sys
import argparse


from utils import remove_duplicates_list

from utils import load_def_lines
from utils import def_lines_are_valid
from utils import def_lines_are_full_lines
from utils import get_def_lines_vals
from utils import build_estim_vals
from utils import print_solutions

from sem_equacoes import quadrado_magico_sem_equacoes
from com_equacoes import quadrado_magico_com_equacoes


def main():

    # Get command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l", "--lineslen", type=int, choices=range(1, 5), default=4
        )

    parser.add_argument("filename", nargs="?", default="")

    parser.add_argument(
        "-n", "--withoutequations", action="store_true"
        )

    parser.add_argument(
        "-e", "--withequations", action="store_true"
        )

    parser.add_argument(
        "-o", "--outputsolutions", action="store_true"
        )

    parser.add_argument(
        "-h", "--horizontal", action="store_true"
        )

    parser.add_argument(
        "v", "--vertical", action="store_true"
        )

    parser.add_argument(
        "d", "--diagonal", action="store_true"
        )

    args = parser.parse_args()

    lines_len = args.lineslen

    filename = args.filename

    without_equations = args.withoutequations
    with_equations = args.withequations

    output_solutions = args.outputsolutions

    horizontal = args.horizontal
    vertical = args.vertical
    diagonal = args.diagonal

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

    # Load defined lines
    # def_lines = load_def_lines(directory, num_lines, lines_len)
    def_lines = load_def_lines(filename, lines_len)

    # Check if defined lines are valid
    if not def_lines_are_valid(
            def_lines,
            lines_len, lines_sum, max_value
            ):

        sys.exit("Defined lines are invalid")

    # Check if defined lines are full lines
    if not def_lines_are_full_lines(def_lines, lines_len):
        sys.exit("Defined lines are not full lines")

    # Calculate number of defined lines
    num_def_lines = len(def_lines)

    # Get defined lines values
    def_lines_vals = get_def_lines_vals(def_lines)

    # Build estimated values
    estim_vals = build_estim_vals(max_value, def_lines_vals)

    with_equations_valid = True
    if (lines_len > 4) or ((lines_len == 4) and (num_def_lines < 2)):
        with_equations_valid = False

    if without_equations or (not without_equations and not with_equations):
        print()
        print()

        print()
        print("WITHOUT EQUATIONS")

        result_without_equations = quadrado_magico_sem_equacoes(
            horizontal, vertical, diagonal,
            def_lines, num_def_lines,
            estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        sols_count = result_without_equations["sols_count"]
        valid_sols_count = result_without_equations["valid_sols_count"]

        valid_sols_len = len(result_without_equations["valid_sols"])

        diff_sols = remove_duplicates_list(
            result_without_equations["valid_sols"]
            )

        diff_sols_count = len(diff_sols)

        solutions_output = False
        if output_solutions and not with_equations:
            print()
            print_solutions(diff_sols, lines_len, max_value)

            solutions_output = True

        if solutions_output:
            print()
            print()

            print()
            print("WITHOUT EQUATIONS")

        print()
        print(
                (
                    f"{diff_sols_count} Different Solutions   "
                    f"{valid_sols_count} Valid Solutions   "
                    f"{valid_sols_len} Valid Solutions Length   "
                    f"{sols_count} Solutions   "
                )
            )

        print()
        print()

    if with_equations:
        print()
        print()

        print()
        print("WITH EQUATIONS")

        if not with_equations_valid:
            print()
            print("With Equations is not Valid")

        else:
            result_with_equations = quadrado_magico_com_equacoes(
                def_lines, num_def_lines,
                def_lines_vals, estim_vals,
                lines_len, lines_sum, max_value, num_values
                )

            error = result_with_equations["error"]
            if error:
                print()
                print(error)

            else:
                sols_count = result_with_equations["sols_count"]
                valid_sols_count = result_with_equations["valid_sols_count"]

                valid_sols_len = len(result_with_equations["valid_sols"])

                excepts_count = result_with_equations["excepts_count"]

                diff_sols = remove_duplicates_list(
                    result_with_equations["valid_sols"]
                    )

                diff_sols_count = len(diff_sols)

                solutions_output = False
                if output_solutions and not without_equations:
                    print()
                    print_solutions(diff_sols, lines_len, max_value)

                    solutions_output = True

                if solutions_output:
                    print()
                    print()

                    print()
                    print("WITH EQUATIONS")

                print()
                print(
                        (
                            f"{diff_sols_count} Different Solutions   "
                            f"{valid_sols_count} Valid Solutions   "
                            f"{valid_sols_len} Valid Solutions Length   "
                            f"{sols_count} Solutions   "
                            f"{excepts_count} Exceptiions"
                        )
                    )

        print()
        print()


if __name__ == "__main__":
    main()
