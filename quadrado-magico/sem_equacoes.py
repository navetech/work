from utils import build_permutations
from utils import build_def_lines_vals_permuts
from utils import diagonals_sums_are_valid
from utils import check_solution


global lines_len
global lines_sum

global max_value
global num_values

global def_lines
global num_def_lines

global estim_vals


def build_estim_vals_part_lines_permuts(
        estim_vals,
        partial_lines_len,
        lines_sum
        ):
    """
    Build permutations for partial lines of estimated values
    """

    permut_len = partial_lines_len

    permuts = build_permutations(estim_vals, permut_len)

    valid_lines = []

    for permut in permuts:
        valid_line = []

        values_sum = 0
        for value in permut:
            values_sum += value

            if values_sum < lines_sum:
                valid_line.append(value)

        if len(valid_line) > 0:
            valid_lines.append(valid_line)

    permut_len = partial_lines_len

    part_lines_permuts = build_permutations(valid_lines, permut_len)

    return part_lines_permuts


def build_estim_vals_full_lines_permuts(
        estim_vals,
        num_full_lines,
        lines_len, lines_sum
        ):
    """
    Build permutations for full lines of estimated values
    """

    permut_len = lines_len - 1

    permuts = build_permutations(estim_vals, permut_len)

    valid_lines = []

    for permut in permuts:
        valid_line = []

        possible_values = estim_vals.copy()

        values_sum = 0
        for value in permut:
            values_sum += value

            possible_values.discard(value)

        last_value = lines_sum - values_sum

        if last_value in possible_values:
            for value in permut:
                valid_line.append(value)

            valid_line.append(last_value)

        if len(valid_line) > 0:
            valid_lines.append(valid_line)

    permut_len = num_full_lines

    full_lines_permuts = build_permutations(valid_lines, permut_len)

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

    return solutions

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


def get_solution_horiz_estim_vals(
        full_estim_vals_lines_permut,
        horiz_def_lines_permut, def_lines_vals_permut
        ):
    """
    Get a solution for horizontal estimated values
    """

    def put_horiz_def_lines_vals_in_sol(
            horiz_def_lines_permut, def_lines_vals_permut
            ):
        """
        Put horizontal defined lines values in solution
        """

        global ID_ROWS_BASE

        for i_line in range(num_def_lines):
            row = horiz_def_lines_permut[i_line] - ID_ROWS_BASE

            free_rows.remove(row)

            line_values = def_lines_vals_permut[i_line]

            i_value = row * num_columns

            for column in range(num_columns):
                value = line_values[column]

                values[i_value] = value

                columns_sums[column] += value

                i_value += 1

        return

    def put_full_horiz_estim_vals_lines_in_sol(
            full_estim_vals_lines_permut
            ):
        """
        Put horizontal full estimated values lines in solution
        """

        nonlocal values

        for i_line in range(len(full_estim_vals_lines_permut)):
            row = free_rows[i_line]

            line_values = full_estim_vals_lines_permut[i_line]

            i_value = row * num_columns

            for column in range(num_columns):
                value = line_values[column]

                values[i_value] = value

                columns_sums[column] += value

                i_value += 1

        possible_values = estim_vals.difference(set(values))

        # Fill last horizontal line with estimated values
        i_line = len(free_rows) - 1

        row = free_rows[i_line]

        i_value = row * num_columns

        for column in range(num_columns):
            last_value = lines_sum - columns_sums[column]

            if (last_value < 1) or (last_value > max_value):
                values = []

                return

            if last_value not in possible_values:
                values = []

                return

            possible_values.discard(last_value)

            values[i_value] = last_value

            i_value += 1

        return

    num_rows = lines_len
    num_columns = lines_len

    values = num_values * [None]

    free_rows = list(range(num_rows))

    columns_sums = num_columns * [0]

    # Put horizontal defined lines values in solution
    put_horiz_def_lines_vals_in_sol(
        horiz_def_lines_permut, def_lines_vals_permut
        )

    # Put horizontal full estimated values lines in solution
    put_full_horiz_estim_vals_lines_in_sol(
        full_estim_vals_lines_permut
        )

    if len(values) != num_values:
        return []

    if not diagonals_sums_are_valid(values, lines_len, lines_sum):
        return []

    return values


def get_solution_vert_estim_vals(
        full_estim_vals_lines_permut,
        vert_def_lines_permut, def_lines_vals_permut
        ):
    """
    Get a solution for vertical estimated values
    """

    num_rows = lines_len
    num_columns = lines_len

    values = num_values * [None]

    free_columns = list(range(num_columns))

    rows_sums = num_rows * [0]

    # Put vertical defined lines values in solution
    for i_line in range(num_def_lines):
        column = vert_def_lines_permut[i_line] % lines_len

        free_columns.remove(column)

        line_values = def_lines_vals_permut[i_line]

        i_value = column

        for row in range(num_rows):
            value = line_values[row]

            values[i_value] = value

            rows_sums[row] += value

            i_value += num_columns

    # Put vertical full estimated values lines in solution
    for i_line in range(len(full_estim_vals_lines_permut)):
        column = free_columns[i_line]

        line_values = full_estim_vals_lines_permut[i_line]

        i_value = column

        for row in range(num_rows):
            value = line_values[row]

            values[i_value] = value

            rows_sums[row] += value

            i_value += num_columns

    # Fill last vertical line with estimated values
    possible_values = estim_vals.difference(set(values))

    i_line = len(free_columns) - 1

    column = free_columns[i_line]

    i_value = column

    for row in range(num_rows):
        last_value = lines_sum - rows_sums[row]

        if (last_value < 1) or (last_value > max_value):
            return []

        if last_value not in possible_values:
            return []

        possible_values.discard(last_value)

        values[i_value] = last_value

        i_value += num_columns

    if not diagonals_sums_are_valid(values, lines_len, lines_sum):
        return []

    return values


def get_solution_diag_def_lines_estim_vals(
        part_estim_vals_lines_permut,
        diag_def_lines_permut, def_lines_vals_permut,
        ):
    """
    Get a solution for diagonal defined lines with estimated values
    """

    num_rows = lines_len
    num_columns = lines_len

    values = num_values * [None]

    rows_sums = num_rows * [0]
    columns_sums = num_columns * [0]

    # Put diagonal defined lines values in solution
    for i_line in range(num_def_lines):
        diagonal = diag_def_lines_permut[i_line]

        line_values = def_lines_vals_permut[i_line]

        # Put diagonal 1 defined lines values in solution
        if diagonal == ID_DIAGONAL_1:
            column = 0

            i_value = column

            for row in range(num_rows):
                value = line_values[row]

                values[i_value] = value

                rows_sums[row] += value
                columns_sums[column] += value

                i_value += num_columns + 1

                column += 1

        # Put diagonal 2 defined lines values in solution
        elif diagonal == ID_DIAGONAL_2:
            column = num_columns - 1

            i_value = column

            for row in range(num_rows):
                value = line_values[row]

                values[i_value] = value

                rows_sums[row] += value
                columns_sums[column] += value

                i_value += num_columns - 1

                column -= 1

        else:
            print("diagonal invalid")
            return []

    print (values)

    return []

    # Put partial estimated values lines in solution
    first_col_to_insert = 0
    if values[0] is not None:
        first_col_to_insert += 1

    for row in range(num_rows - 1):
        if row >= len(part_estim_vals_lines_permut):
            break

        vals_to_insert = part_estim_vals_lines_permut[row]

        if (first_col_to_insert + len(vals_to_insert)) > num_columns:
            first_col_to_insert = 0

        i_val_to_insert = 0

        # Put columns values
        for column in range(first_col_to_insert, num_columns):
            if i_val_to_insert >= len(vals_to_insert):
                break

            value = vals_to_insert[i_val_to_insert]

            i_value = (row * num_columns) + column

            if values[i_value] is None:
                i_val_to_insert += 1

                values[i_value] = value

                rows_sums[row] += value
                columns_sums[column] += value

        first_col_to_insert += 1

    # Fill last row with estimated values
    possible_values = estim_vals.difference(set(values))

    row = num_rows - 1

    for column in range(num_columns):
        i_value = (row * num_columns) + column

        if values[i_value] is not None:
            continue

        last_value = lines_sum - columns_sums[column]

        if (last_value < 1) or (last_value > max_value):
            return []

        if last_value not in possible_values:
            return []

        possible_values.discard(last_value)

        values[i_value] = last_value

    # Check rows sums
    for row in range(num_rows):
        if rows_sums[row] != lines_sum:
            return []

    # Check columns sums
    for column in range(num_columns):
        if columns_sums[column] != lines_sum:
            return []

    return values


def get_solution_horizontal_estim_vals(
        full_estim_vals_lines_permut, estim_vals,
        lines_len, lines_sum
        ):
    """
    Get a solution for horizontal estimated values
    """

    values = []

    for lines_values in full_estim_vals_lines_permut:
        values.extend(lines_values)

    possible_values = estim_vals.difference(set(values))

    num_columns = lines_len

    last_line_values = []

    for column in range(num_columns):
        column_sum = 0

        i_value = column

        for row in range(len(full_estim_vals_lines_permut)):
            column_sum += values[i_value]

            i_value += num_columns

        last_value = lines_sum - column_sum

        if last_value not in possible_values:
            return []

        possible_values.discard(last_value)

        last_line_values.append(last_value)

    values.extend(last_line_values)

    if not diagonals_sums_are_valid(values, lines_len, lines_sum):
        return []

    return values


def get_sols_horiz_estim_vals(
        full_estim_vals_lines_permuts,
        horiz_def_lines_permut, def_lines_vals_permut
        ):
    """
    Get solutions for horizontal estimated values
    """

    global result

    # For each permutation of full lines of estimated values
    full_estim_vals_lines_permuts_count = 0
    for full_estim_vals_lines_permut in full_estim_vals_lines_permuts:
        full_estim_vals_lines_permuts_count += 1

        # Get solution for horizontal estimated values
        solution = get_solution_horiz_estim_vals(
            full_estim_vals_lines_permut,
            horiz_def_lines_permut, def_lines_vals_permut
            )

        result["sols_count"] += 1

        if len(solution) > 0:
            result["valid_sols"].append(solution)

            result["valid_sols_count"] += 1

        print(
            full_estim_vals_lines_permuts_count,
            result["sols_count"], result["valid_sols_count"],
            solution, end="\r"
            )

    # This check is necessry because full_estim_vals_lines_permuts
    # does not have len() method
    if full_estim_vals_lines_permuts_count < 1:
        full_estim_vals_lines_permut = []

        # Get solution for horizontal estimated values
        solution = get_solution_horiz_estim_vals(
            full_estim_vals_lines_permut,
            horiz_def_lines_permut, def_lines_vals_permut,
            )

        result["sols_count"] += 1

        if len(solution) > 0:
            result["valid_sols"].append(solution)

            result["valid_sols_count"] += 1

        print(
            full_estim_vals_lines_permuts_count,
            result["sols_count"], result["valid_sols_count"],
            solution, end="\r"
            )

    return


def get_sols_vert_estim_vals(
        full_estim_vals_lines_permuts,
        vert_def_lines_permut, def_lines_vals_permut
        ):
    """
    Get solutions for vertical estimated values
    """

    # For each permutation of full lines of estimated values
    full_estim_vals_lines_permuts_count = 0
    for full_estim_vals_lines_permut in full_estim_vals_lines_permuts:
        full_estim_vals_lines_permuts_count += 1

        # Get solution for vertical estimated values
        solution = get_solution_vert_estim_vals(
            full_estim_vals_lines_permut,
            vert_def_lines_permut, def_lines_vals_permut
            )

        result["sols_count"] += 1

        if len(solution) > 0:
            result["valid_sols"].append(solution)

            result["valid_sols_count"] += 1

        print(
            full_estim_vals_lines_permuts_count,
            result["sols_count"], result["valid_sols_count"],
            solution, end="\r"
            )

    # This check is necessry because full_estim_vals_lines_permuts
    # does not have len() method
    if full_estim_vals_lines_permuts_count < 1:
        full_estim_vals_lines_permut = []

        # Get solution for vertical estimated values
        solution = get_solution_vert_estim_vals(
            full_estim_vals_lines_permut,
            vert_def_lines_permut, def_lines_vals_permut
            )

        result["sols_count"] += 1

        if len(solution) > 0:
            result["valid_sols"].append(solution)

            result["valid_sols_count"] += 1

        print(
            full_estim_vals_lines_permuts_count,
            result["sols_count"], result["valid_sols_count"],
            solution, end="\r"
            )

    return


def get_sols_diag_def_lines_estim_vals(
        part_estim_vals_lines_permuts,
        diag_def_lines_permut, def_lines_vals_permut
        ):
    """
    Get solutions for diagonal defined lines with estimated values
    """

    # For each permutation of partial lines of estimated values
    part_estim_vals_lines_permuts_count = 0
    for part_estim_vals_lines_permut in part_estim_vals_lines_permuts:
        part_estim_vals_lines_permuts_count += 1

        # Get solution for diagonal defined lines with estimated values
        solution = get_solution_diag_def_lines_estim_vals(
            part_estim_vals_lines_permut,
            diag_def_lines_permut, def_lines_vals_permut,
            )

        result["sols_count"] += 1

        if len(solution) > 0:
            result["valid_sols"].append(solution)

            result["valid_sols_count"] += 1

        print(
            part_estim_vals_lines_permuts_count,
            result["sols_count"], result["valid_sols_count"],
            solution, end="\r"
            )

    # This check is necessry because full_estim_vals_lines_permuts
    # does not have len() method
    if part_estim_vals_lines_permuts_count < 1:
        part_estim_vals_lines_permut = []

        # Get solution for diagonal defined lines with estimated values
        solution = get_solution_diag_def_lines_estim_vals(
            part_estim_vals_lines_permut,
            diag_def_lines_permut, def_lines_vals_permut,
            )

        result["sols_count"] += 1

        if len(solution) > 0:
            result["valid_sols"].append(solution)

            result["valid_sols_count"] += 1

        print(
            part_estim_vals_lines_permuts_count,
            result["sols_count"], result["valid_sols_count"],
            solution, end="\r"
            )

    return


def get_solutions_horizontal_estim_vals(
        full_estim_vals_lines_permuts, estim_vals,
        lines_len, lines_sum
        ):
    """
    Get solutions for horizontal estimated values
    """

    solutions = []

    # For each permutation of full lines of estimated values
    i = 0
    valid_count = 0
    diff_count = 0

    for full_estim_vals_lines_permut in full_estim_vals_lines_permuts:
        i += 1

        # Get solution for horizontal estimated values
        solution = get_solution_horizontal_estim_vals(
            full_estim_vals_lines_permut, estim_vals,
            lines_len, lines_sum
            )

        if len(solution) > 0:
            valid_count += 1

            if solution not in solutions:
                diff_count += 1

                solutions.append(solution)

        print(i, valid_count, diff_count, solution, end="\r")

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
        lines_len, lines_sum
        )

    # Get solutions for horizontal estimated values
    sols = get_solutions_horizontal_estim_vals(
        full_estim_vals_lines_permuts, estim_vals,
        lines_len, lines_sum
        )

    solutions.extend(sols)

    # Get solutions for vertical estimated values
    sols = get_solutions_vertical_estim_vals(
        full_estim_vals_lines_permuts,
        lines_len, lines_sum, max_value, num_values
        )

    solutions.extend(sols)

    return solutions


def build_horiz_def_lines_permuts(
        num_def_lines, lines_len
        ):
    """
    Build permutations for horizontal defined lines
    """

    global ID_ROWS_BASE

    if num_def_lines < 1:
        return []

    id_rows = list(range(ID_ROWS_BASE, ID_ROWS_BASE + lines_len))

    permuts = list(build_permutations(id_rows, num_def_lines))

    return permuts


def build_vert_def_lines_permuts(
        num_def_lines, lines_len
        ):
    """
    Build permutations for vertical defined lines
    """

    if num_def_lines < 1:
        return []

    id_columns = list(range(ID_COLUMNS_BASE, ID_COLUMNS_BASE + lines_len))

    permuts = list(build_permutations(id_columns, num_def_lines))

    return permuts


def build_diag_def_lines_permuts(
        num_def_lines, lines_len
        ):
    """
    Build permutations for diagonal defined lines
    """

    if (
        (num_def_lines < 1)
        or (num_def_lines > 2)
        or ((num_def_lines == 2) and (lines_len % 2) != 0)
    ):
        return []

    id_diagonals = [ID_DIAGONAL_1, ID_DIAGONAL_2]

    permuts = list(build_permutations(id_diagonals, num_def_lines))

    return permuts


def get_sols_horiz_def_lines(
        def_lines_vals_permuts, num_def_lines,
        full_estim_vals_lines_permuts
        ):
    """
    Get solutions for horizontal defined lines
    """

    # Build permutations for horizontal defined lines
    horiz_def_lines_permuts = build_horiz_def_lines_permuts(
        num_def_lines, lines_len
        )

    # For each permutation of horizontal defined lines
    for horiz_def_lines_permut in horiz_def_lines_permuts:

        # For each permutation of defined lines values
        for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

            # Get solutions for horizontal estimated values
            get_sols_horiz_estim_vals(
                full_estim_vals_lines_permuts,
                horiz_def_lines_permut, def_lines_vals_permut
                )

    return


def get_sols_vert_def_lines(
        def_lines_vals_permuts, num_def_lines,
        full_estim_vals_lines_permuts
        ):
    """
    Get solutions for vertical defined lines
    """

    # Build permutations for vertical defined lines
    vert_def_lines_permuts = build_vert_def_lines_permuts(
        num_def_lines, lines_len
        )

    # For each permutation of vertical defined lines
    for vert_def_lines_permut in vert_def_lines_permuts:

        # For each permutation of defined lines values
        for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

            # Get solutions for vertical estimated values
            get_sols_vert_estim_vals(
                full_estim_vals_lines_permuts,
                vert_def_lines_permut, def_lines_vals_permut
                )

    return


def get_sols_parallel_def_lines(
        def_lines_vals_permuts
        ):
    """
    Get solutions for parallel defined lines
    """

    # Build permutations for full lines of estimated values
    num_lines = lines_len
    num_full_lines = num_lines - num_def_lines - 1

    full_estim_vals_lines_permuts = build_estim_vals_full_lines_permuts(
        estim_vals,
        num_full_lines,
        lines_len, lines_sum
        )

    # Get solutions for horizontal defined lines
    get_sols_horiz_def_lines(
        def_lines_vals_permuts, num_def_lines,
        full_estim_vals_lines_permuts
        )

    # Get solutions for vertical defined lines
    get_sols_vert_def_lines(
        def_lines_vals_permuts, num_def_lines,
        full_estim_vals_lines_permuts
        )

    return result


def get_sols_diag_def_lines(
        def_lines_vals_permuts
        ):
    """
    Get solutions for diagonal defined lines
    """

    # Build permutations for partial lines of estimated values
    partial_lines_len = lines_len - num_def_lines - 1

    part_estim_vals_lines_permuts = build_estim_vals_part_lines_permuts(
        estim_vals,
        partial_lines_len,
        lines_sum
        )

    # Build permutations for diagonal defined lines
    diag_def_lines_permuts = build_diag_def_lines_permuts(
        num_def_lines, lines_len
        )

    # For each permutation of diagonal defined lines
    for diag_def_lines_permut in diag_def_lines_permuts:

        # For each permutation of defined lines values
        for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

            # Get solutions for diagonal defined lines with estimated values
            get_sols_diag_def_lines_estim_vals(
                part_estim_vals_lines_permuts,
                diag_def_lines_permut, def_lines_vals_permut
                )

    return


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

    return solutions

    # Build permutations for full lines of estimated values
    num_full_lines = 2

    full_estim_vals_lines_permuts = build_estim_vals_full_lines_permuts(
        estim_vals,
        num_full_lines,
        lines_len, lines_sum
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
        def_lines_, num_def_lines_,
        estim_vals_,
        lines_len_, lines_sum_, max_value_, num_values_
        ):
    """
    Quadrado magico sem equacoes
    """

    global lines_len
    global lines_sum

    global max_value
    global num_values

    global def_lines
    global num_def_lines

    global estim_vals

    lines_len = lines_len_
    lines_sum = lines_sum_

    max_value = max_value_
    num_values = num_values_

    def_lines = def_lines_
    num_def_lines = num_def_lines_

    estim_vals = estim_vals_

    # Initialize lines ids
    global ID_ROWS_BASE
    ID_ROWS_BASE = 0

    global ID_COLUMNS_BASE
    ID_COLUMNS_BASE = ID_ROWS_BASE + lines_len

    global ID_DIAGONALS_BASE
    ID_DIAGONALS_BASE = ID_COLUMNS_BASE + lines_len

    global ID_DIAGONAL_1
    ID_DIAGONAL_1 = ID_DIAGONALS_BASE

    global ID_DIAGONAL_2
    ID_DIAGONAL_2 = ID_DIAGONALS_BASE + 1

    # Initialize result
    global result
    result = {}

    result["sols_count"] = 0

    result["valid_sols_count"] = 0
    result["valid_sols"] = []

    solutions = []

    # If there are defined lines
    if num_def_lines > 0:

        # Build defined lines values permutations
        def_lines_vals_permuts = build_def_lines_vals_permuts(
            def_lines, num_def_lines
            )

        count = 0
        for permut in def_lines_vals_permuts:
            print(permut)
            count += 1

        print(count)

        return result
        
        # Get solutions for parallel defined lines
        """
        get_sols_parallel_def_lines(
            def_lines_vals_permuts
            )
        """

        # Get solutions for diagonal defined lines
        if (
            (num_def_lines == 1)
            or ((num_def_lines == 2) and ((lines_len % 2) == 0))
        ):

            get_sols_diag_def_lines(
                def_lines_vals_permuts
                )

    # Else there are not any defined lines
    else:

        return result

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

    return result
