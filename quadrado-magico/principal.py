import sys
import argparse


from utils import load_def_lines
from utils import def_lines_are_valid
from utils import get_def_lines_vals
from utils import build_estim_vals
from utils import output_solutions

from sem_equacoes import quadrado_magico_sem_equacoes
from com_equacoes import quadrado_magico_com_equacoes


def main():

    # Get command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", nargs="?", default="")

    parser.add_argument(
        "-l", "--lineslen", type=int, choices=range(1, 5), default=4
        )

    parser.add_argument(
        "-n", "--withouteq", action="store_true"
        )

    parser.add_argument(
        "-e", "--witheq", action="store_true"
        )

    args = parser.parse_args()

    lines_len = args.lineslen

    filename = args.filename

    without_equations = args.withouteq
    with_equations = args.witheq

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

    with_equations_valid = True
    if (lines_len > 4) or ((lines_len == 4) and (num_def_lines < 2)):
        with_equations_valid = False

    if without_equations or (not without_equations and not with_equations):
        print()
        print()

        print()
        print("WITHOUT EQUATIONS")

        result_without_equations = quadrado_magico_sem_equacoes(
            def_lines, num_def_lines,
            def_lines_vals, num_def_lines_vals,
            estim_vals, num_estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        diff_solutions = result_without_equations

        diff_solutions_count = len(diff_solutions)

        solutions_output = False
        if not without_equations:
            print()
            output_solutions(diff_solutions, lines_len, max_value)

            solutions_output = True

        if solutions_output:
            print()
            print()

            print()
            print("WITHOUT EQUATIONS")

        print()
        print(
                (
                    f"{diff_solutions_count} Different Solutions   "
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
                diff_solutions = result_with_equations["diff_solutions"]

                diff_solutions_count = len(diff_solutions)

                solutions_output = False
                if not without_equations:
                    print()
                    output_solutions(diff_solutions, lines_len, max_value)

                    solutions_output = True

                solutions_count = result_with_equations["solutions_count"]

                valid_solutions_count = (
                    result_with_equations["valid_solutions_count"]
                )

                exceptions_count = result_with_equations["exceptions_count"]

                if solutions_output:
                    print()
                    print()

                    print()
                    print("WITH EQUATIONS")

                print()
                print(
                        (
                            f"{diff_solutions_count} Different Solutions   "
                            f"{valid_solutions_count} Valid Solutions   "
                            f"{solutions_count} Solutions   "
                            f"{exceptions_count} Exceptiions"
                        )
                    )

        print()
        print()


if __name__ == "__main__":
    main()
