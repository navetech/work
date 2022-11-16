from utils import build_permutations
from utils import build_estim_vals_permuts
from utils import build_def_lines_vals_permuts
from utils import check_solution, output_solutions


def build_estim_vals_2_lines_permuts(
        all_estim_vals, line_length, line_sum, max_value
        ):
    """
    Build 2 lines estimated values permutations
    """

    permut_length = line_length - 1

    permuts = build_permutations(all_estim_vals, permut_length)

    valid_permuts = []

    for permut in permuts:
        invalid_permut = False
        permut_sum = 0

        for value in permut:
            permut_sum += value

            if permut_sum >= line_sum:
                invalid_permut = True
                break

        if (not invalid_permut):
            last_value = line_sum - permut_sum

            if (last_value >= 1) and (last_value <= max_value):

                for value in permut:
                    valid_permuts.append(value)
                    valid_permuts.append(last_value)

    permut_length = 2

    two_lines_permuts = build_permutations(valid_permuts, permut_length)

    return two_lines_permuts


def build_remain_estim_vals_permuts(
        all_estim_vals, estim_vals_2_lines_permut
        ):
    """
    Build remaining estimated values permutations
    """

    two_lines_vals = set()
    for line_values in estim_vals_2_lines_permut:
        values = set(line_values)

        two_lines_vals = two_lines_vals.union(values)

    remain_estim_vals = all_estim_vals.difference(two_lines_vals)

    remain_estim_vals = list(remain_estim_vals)

    remain_estim_vals.sort()

    return remain_estim_vals


def get_solution_estim_vals(
        estim_vals_2_lines_permut, remain_estim_vals_permut,
        line_length, num_values, max_value, line_sum
        ):
    """
    Get solution
    """

    values = []

    for lines_values in estim_vals_2_lines_permut:
        values.extend(lines_values)

    values.extend(remain_estim_vals_permut)

    solution = check_solution(
        values, line_length, num_values, max_value, line_sum
        )

    return solution


def get_solution_def_lines_estim_vals(
        def_lines_vals_permut, estim_vals_permut,
        line_length, num_values, max_value, line_sum
        ):
    """
    Get solution
    """

    values = []

    for lines_values in def_lines_vals_permut:
        values.extend(lines_values)

    values.extend(estim_vals_permut)

    solution = check_solution(
        values, line_length, num_values, max_value, line_sum
        )

    return solution


def get_solution_def_lines(
        def_lines_vals_permut,
        line_length, num_values, max_value, line_sum
        ):
    """
    Get solution
    """

    values = []

    for lines_values in def_lines_vals_permut:
        values.extend(lines_values)

    last_values = []

    columns_sum = line_length * [0]
    for column in range(line_length):

        for lines_values in def_lines_vals_permut:
            value = lines_values[column]

            columns_sum[column] += value

        value = line_sum - columns_sum[column]
        last_values.append(value)

    values.extend(last_values)

    solution = check_solution(
        values, line_length, num_values, max_value, line_sum
        )

    return solution


def quadrado_magico_sem_equacoes(
        line_length, max_value, num_values, line_sum,
        def_lines, num_def_lines, all_estim_vals
        ):
    """
    Quadrado magico sem equacoes
    """

    solutions_count = 0
    solutions = []

    # If there are not any defined lines
    if num_def_lines < 1:

        # Build 2 lines estimated values permutations
        estim_vals_2_lines_permuts = build_estim_vals_2_lines_permuts(
            all_estim_vals, line_length, line_sum, max_value
            )

        """
        count = 0
        for permut in estim_vals_2_lines_permuts:
            count += 1
            # print(permut)

        print((len(all_estim_vals))
        print(count)
        """

        # For each estimated values 2 lines permutation
        for estim_vals_2_lines_permut in estim_vals_2_lines_permuts:

            # Build remaining estimated values permutations
            remain_estim_vals_permuts = build_remain_estim_vals_permuts(
                all_estim_vals, estim_vals_2_lines_permut,
                line_length, line_sum
                )

            # For each remaining estimated values permutation
            for remain_estim_vals_permut in remain_estim_vals_permuts:

                # Get solution
                solution = get_solution_estim_vals(
                    estim_vals_2_lines_permut, remain_estim_vals_permut
                    )

                if len(solution) > 1:
                    solutions_count += 1
                    solutions.append(solution)

    # Else there are defined lines
    else:

        # Build defined lines values permutations
        def_lines_vals_permuts = build_def_lines_vals_permuts(
            def_lines, num_def_lines
            )

        """
        print()
        print("inverted")
        for permuts in def_lines_vals_permuts["inverted"]:
            print(permuts)

        print(len(def_lines_vals_permuts["inverted"]))

        print()
        print("direct")
        for i in range(num_def_lines):
            print()
            for permut in def_lines_vals_permuts["direct"][i]:
                print(permut)
            count = len(def_lines_vals_permuts["direct"][i])
            print(f"{count} permuts of line {i}")
        """

        # Build estimated values permutations
        num_estim_vals_equations = num_values - (num_def_lines * line_length)

        estim_vals_permuts = build_estim_vals_permuts(
            all_estim_vals, num_estim_vals_equations
            )

        # Convert estimated values permutations to list because if not
        # it cause failures on iterating this sequence,
        # and if the conversion is made at the sequence generation
        # it cause memory error when the sequence is too big
        estim_vals_permuts_list = list(estim_vals_permuts)

        # For each defined lines values permutations
        for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

            # For each estimated values permutation
            estim_vals_permut_counts = 0
            for estim_vals_permut in estim_vals_permuts_list:
                estim_vals_permut_counts += 1

                # Get solution
                solution = get_solution_def_lines_estim_vals(
                    def_lines_vals_permut, estim_vals_permut
                    )

                if len(solution) > 1:
                    solutions_count += 1
                    solutions.append(solution)

                # if there are not any estimated values permutations
                if estim_vals_permut_counts < 1:

                    # Get solution
                    solution = get_solution_def_lines(def_lines_vals_permut)

                    if len(solution) > 1:
                        solutions_count += 1
                        solutions.append(solution)

    print()
    print()

    output_solutions(solutions, line_length, max_value)

    print()
    print()

    print()
    print('Number of Solutions')
    print(solutions_count)

    return solutions
