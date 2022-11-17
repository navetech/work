from utils import build_permutations
from utils import check_solution


def build_estim_vals_full_lines_permuts(
        estim_vals,
        num_full_lines,
        lines_len, lines_sum, max_value
        ):
    """
    Build permutations for full lines of estimated values
    """

    permut_len = lines_len - 1

    permuts = build_permutations(estim_vals, permut_len)

    valid_permuts = []

    for permut in permuts:
        invalid_permut = False
        values_sum = 0

        for value in permut:
            values_sum += value

            if values_sum >= lines_sum:
                invalid_permut = True
                break

        if (not invalid_permut):
            last_value = lines_sum - values_sum

            if (last_value >= 1) and (last_value <= max_value):
                for value in permut:
                    valid_permuts.append(value)

                valid_permuts.append(last_value)

    permut_len = num_full_lines

    full_lines_permuts = build_permutations(valid_permuts, permut_len)

    return full_lines_permuts


def build_remain_estim_vals_permuts(
        estim_vals, estim_vals_lines_permut
        ):
    """
    Build permutations for the remaining estimated values
    """

    lines_vals = set()

    for line_values in estim_vals_lines_permut:
        values = set(line_values)

        lines_vals = lines_vals.union(values)

    remain_estim_vals = estim_vals.difference(lines_vals)
    permut_len = len(remain_estim_vals)

    remain_estim_vals_permuts = build_permutations(
        remain_estim_vals, permut_len
        )

    return remain_estim_vals_permuts


def get_solution_vertical_estim_vals(
        full_estim_vals_lines_permut,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get a solution for vertical estimated values
    """

    values = []

    solution = check_solution(
        values,
        lines_len, lines_sum, max_value, num_values
        )

    return solution


def get_solutions_vertical_estim_vals(
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for vertical estimated values
    """

    solutions = []

    # For each permutation of full lines of estimated values
    for full_estim_vals_lines_permut in full_estim_vals_lines_permuts:

        # Get solution for vertical estimated values
        solution = get_solution_vertical_estim_vals(
            full_estim_vals_lines_permut,
            lines_len, lines_sum, max_value, num_values
            )

        if len(solution) > 0:
            solutions.append(solution)

    return solutions


def get_solution_horizontal_estim_vals(
        full_estim_vals_lines_permut,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get a solution for horizontal estimated values
    """

    values = []

    for lines_values in full_estim_vals_lines_permut:
        values.extend(lines_values)

    num_rows = lines_len
    num_columns = lines_len

    for column in range(num_columns):
        values_sum = 0

        for row in range(len(full_estim_vals_lines_permut)):
            i_value = (row * num_columns) + column

            values_sum += values[i_value]
            if values_sum > lines_sum:
                return []

        last_value = lines_sum - values_sum

        if (last_value < 1) or (last_value > max_value):
            return []

        else:
            row = num_rows - 1

            i_value = (row * num_columns) + column
            values[i_value] = last_value

    solution = check_solution(
        values,
        lines_len, lines_sum, max_value, num_values
        )

    return solution


def get_solutions_horizontal_estim_vals(
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for horizontal estimated values
    """

    solutions = []

    # For each permutation of full lines of estimated values
    for full_estim_vals_lines_permut in full_estim_vals_lines_permuts:

        # Get solution for horizontal estimated values
        solution = get_solution_horizontal_estim_vals(
            full_estim_vals_lines_permut,
            lines_len, lines_sum, max_value, num_values
            )

        if len(solution) > 0:
            solutions.append(solution)

    return solutions


def get_solutions_parallel_estim_vals_only(
        estim_vals,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for parallel estimated values only
    """

    solutions = []

    # Build permutations for full lines of estimated values only
    num_lines = lines_len
    num_full_lines = num_lines - 1

    full_estim_vals_lines_permuts = build_estim_vals_full_lines_permuts(
        estim_vals,
        num_full_lines,
        lines_len, lines_sum, max_value
        )

    # Get solutions for horizontal estimated values
    sols = get_solutions_horizontal_estim_vals(
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        )

    solutions.extend(sols)

    # Get solutions for vertical estimated values
    sols = get_solutions_vertical_estim_vals(
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        )

    solutions.extend(sols)

    return solutions


def get_solutions_horizontal_def_lines(
        def_lines, num_def_lines,
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for horizontal defined lines
    """

    solutions = []

    return solutions


def get_solutions_vertical_def_lines(
        def_lines, num_def_lines,
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for vertical defined lines
    """

    solutions = []

    return solutions


def get_solutions_parallel_def_lines(
        def_lines, num_def_lines,
        estim_vals,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for parallel defined lines
    """

    solutions = []

    # If there are defined lines
    if num_def_lines > 1:

        # Build permutations for full lines of estimated values
        num_lines = lines_len
        num_full_lines = num_lines - num_def_lines - 1

        full_estim_vals_lines_permuts = build_estim_vals_full_lines_permuts(
            estim_vals,
            num_full_lines,
            lines_len, lines_sum, max_value
            )

        # Get solutions for horizontal defined lines
        sols = get_solutions_horizontal_def_lines(
            def_lines, num_def_lines,
            full_estim_vals_lines_permuts,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

        # Get solutions for vertical defined lines
        sols = get_solutions_vertical_def_lines(
            def_lines, num_def_lines,
            full_estim_vals_lines_permuts,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

    # Else there are not any defined lines
    else:

        # Get solutions for parallel estimated values only
        sols = get_solutions_parallel_estim_vals_only(
            estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

    return solutions


def get_solutions_non_parallel_def_lines(
        def_lines, num_def_lines,
        estim_vals,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for non parallel defined lines
    """

    solutions = []

    return solutions


def get_solution_diagonal_estim_vals(
        full_estim_vals_lines_permut,
        remain_estim_vals_permut,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get a solution for diagonal estimated values
    """

    values = []

    for lines_values in full_estim_vals_lines_permut:
        values.extend(lines_values)

    values.extend(remain_estim_vals_permut)

    solution = check_solution(
        values,
        lines_len, lines_sum, max_value, num_values
        )

    return solution


def get_solutions_diagonal_estim_vals_only(
        estim_vals,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Get solutions for diagonal estimated values only
    """

    solutions = []

    # Build permutations for full lines of estimated values
    num_full_lines = 2

    full_estim_vals_lines_permuts = build_estim_vals_full_lines_permuts(
        estim_vals,
        num_full_lines,
        lines_len, lines_sum, max_value
        )

    # For each permutation of full lines of estimated values
    for full_estim_vals_lines_permut in full_estim_vals_lines_permuts:

        # Build permutations for the remaining estimated values
        remain_estim_vals_permuts = build_remain_estim_vals_permuts(
            estim_vals, full_estim_vals_lines_permut
            )

        # For each permutation of the remaining estimated values
        for remain_estim_vals_permut in remain_estim_vals_permuts:

            # Get solution for diagonal estimated values
            solution = get_solution_diagonal_estim_vals(
                full_estim_vals_lines_permut,
                remain_estim_vals_permut,
                lines_len, lines_sum, max_value, num_values
                )

            if len(solution) > 0:
                solutions.append(solution)

    return solutions


def quadrado_magico_sem_equacoes(
        def_lines, num_def_lines,
        def_lines_vals, num_def_lines_vals,
        estim_vals, num_estim_vals,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Quadrado magico sem equacoes
    """

    solutions = []

    # If there are defined lines
    if num_def_lines > 1:

        # Get solutions for parallel defined lines
        sols = get_solutions_parallel_def_lines(
            def_lines, num_def_lines,
            estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

        # Get solutions for non parallel defined lines
        sols = get_solutions_non_parallel_def_lines(
            def_lines, num_def_lines,
            estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

    # Else there are not any defined lines
    else:

        # Get solutions for parallel estimated values only
        sols = get_solutions_parallel_estim_vals_only(
            estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

        # Get solutions for diagonal estimated values only
        sols = get_solutions_diagonal_estim_vals_only(
            estim_vals,
            lines_len, lines_sum, max_value, num_values
            )

        solutions.extend(sols)

    return solutions
