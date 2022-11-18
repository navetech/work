import numpy as np


from utils import build_permutations
from utils import check_solution


def build_fixed_equations_coeffs(
        num_fixed_equations,
        lines_len, num_values
        ):
    """
    Build coefficients for fixed equations
    """

    equations_coeffs = []

    num_columns = lines_len

    for equation in range(num_fixed_equations):
        coeffs = num_values * [0]

        row = equation
        for column in range(num_columns):
            i_x = (row * num_fixed_equations) + column

            coeffs[i_x] = 1

        equations_coeffs.append(coeffs)

    return equations_coeffs


def build_estim_vals_permuts(
        estim_vals, num_estim_vals_to_permut
        ):
    """
    Build estimated values permutations
    """

    permut_length = num_estim_vals_to_permut

    permuts = build_permutations(estim_vals, permut_length)

    return permuts


def build_def_lines_vals_permuts(
        def_lines, num_def_lines
        ):
    """
    Build defined lines values permutations
    """

    vals_permuts = {}

    direct_permuts = []
    for line in def_lines:
        permut_length = len(line)

        line_permuts = list(build_permutations(line, permut_length))

        direct_permuts.append(line_permuts)

    vals_permuts["direct"] = direct_permuts

    inverted_permuts = []
    i_permut = 0

    while True:
        end = True
        permuts = []

        for i_line in range(num_def_lines):
            line_permuts = direct_permuts[i_line]

            if i_permut < len(line_permuts):
                end = False

                permut = line_permuts[i_permut]
                permuts.append(permut)
            else:
                permuts.append([])

        if end:
            break

        inverted_permuts.append(permuts)

        i_permut += 1

    vals_permuts["inverted"] = inverted_permuts

    return vals_permuts


def build_def_lines_pos_permuts(
        num_def_lines, lines_len
        ):
    """
    Build defined lines positions permutations
    """

    if num_def_lines < 1:
        return []

    permuts = []

    id_rows = list(range(lines_len))
    id_columns = list(range(lines_len, 2 * lines_len))
    id_diagonals = [2 * lines_len, 2 * lines_len + 1]

    rows_permuts = list(build_permutations(id_rows, num_def_lines))
    columns_permuts = list(build_permutations(id_columns, num_def_lines))

    permuts.extend(rows_permuts)
    permuts.extend(columns_permuts)

    if num_def_lines < 3:
        diagonals_permuts = list(
            build_permutations(id_diagonals, num_def_lines)
            )
        permuts.extend(diagonals_permuts)

    return permuts


def build_def_lines_equations_coeffs(
        def_lines_pos_permut,
        lines_len, num_values
        ):
    """
    Build coefficients for defined lines equations
    """

    equations_coeffs = []

    num_colums = lines_len

    for position in def_lines_pos_permut:

        if position < lines_len:
            row = position

            for i in range(lines_len):
                column = i

                i_x = (row * num_colums) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

        elif position < 2 * lines_len:
            column = position % lines_len

            for i in range(lines_len):
                row = i

                i_x = (row * num_colums) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

        elif position == 2 * lines_len:
            for i in range(lines_len):
                row = i
                column = i

                i_x = (row * num_colums) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

        elif position == (2 * lines_len) + 1:
            for i in range(lines_len):
                row = i
                column = (num_colums - 1) - i

                i_x = (row * num_colums) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

    return equations_coeffs


def build_def_lines_equations_consts(def_lines_vals_permut):
    """
    Build constants for defined lines equations
    """

    equations_consts = []

    for values in def_lines_vals_permut:

        for value in values:
            equations_consts.append(value)

    return equations_consts


def get_def_lines_cells_occupation(
        def_lines_pos_permut, lines_len
        ):
    """
    Get cells occupation for defined lines
    """

    cells_occupation = {}

    num_rows = lines_len
    num_columns = lines_len

    rows_with_free_cells = set(list(range(num_rows)))
    columns_with_free_cells = set(list(range(num_columns)))

    rows_num_free_cells = num_rows * [num_columns]
    columns_num_free_cells = num_columns * [num_rows]

    occupied_cells = set()

    for position in def_lines_pos_permut:
        if position < lines_len:
            row = position

            rows_with_free_cells.discard(row)
            rows_num_free_cells[row] = 0

            for column in range(num_columns):
                occupied_cells.add((row, column))

                columns_num_free_cells[column] -= 1

        elif position < 2 * lines_len:
            column = position % lines_len

            columns_with_free_cells.discard(column)
            columns_num_free_cells[column] = 0

            for row in range(num_rows):
                occupied_cells.add((row, column))

                rows_num_free_cells[row] -= 1

        elif position == 2 * lines_len:
            for i in range(lines_len):
                row = i
                column = i

                occupied_cells.add((row, column))

                rows_num_free_cells[row] -= 1
                columns_num_free_cells[column] -= 1

        elif position == (2 * lines_len) + 1:
            for i in range(lines_len):
                row = i
                column = (lines_len - 1) - i

                occupied_cells.add((row, column))

                rows_num_free_cells[row] -= 1
                columns_num_free_cells[column] -= 1

        else:
            return {}

    cells_occupation["rows_with_free_cells"] = rows_with_free_cells
    cells_occupation["columns_with_free_cells"] = columns_with_free_cells

    cells_occupation["rows_num_free_cells"] = rows_num_free_cells
    cells_occupation["columns_num_free_cells"] = columns_num_free_cells

    cells_occupation["occupied_cells"] = occupied_cells

    return cells_occupation


def build_estim_vals_equations_coeffs(
        num_estim_vals_equations, def_lines_pos_permut,
        lines_len, num_values
        ):
    """
    Build coefficients for estimated values equations
    """

    equations_coeffs = []

    num_rows = lines_len
    num_columns = lines_len

    def_lines_cells_occupation = get_def_lines_cells_occupation(
        def_lines_pos_permut, lines_len
        )

    rows_with_free_cells = def_lines_cells_occupation["rows_with_free_cells"]
    columns_with_free_cells = (
        def_lines_cells_occupation["columns_with_free_cells"]
    )

    rows_num_free_cells = def_lines_cells_occupation["rows_num_free_cells"]

    columns_num_free_cells = (
        def_lines_cells_occupation["columns_num_free_cells"]
    )

    occupied_cells = def_lines_cells_occupation["occupied_cells"]

    if len(rows_with_free_cells) > 0:
        rows_with_free_cells = list(rows_with_free_cells)

        rows_with_free_cells.sort()

        vals_count = 0
        i_free_cells_row = 0
        column = 0
        i_equation = 0

        row = rows_with_free_cells[i_free_cells_row]

        if (rows_num_free_cells[row]) == num_rows:
            num_vals_per_line = lines_len

        else:
            num_vals_per_line = min(
                rows_num_free_cells[row],
                num_estim_vals_equations // lines_len
                )

        one_equation_coeffs = num_values * [0]

        while i_equation < num_estim_vals_equations:

            if (vals_count >= num_vals_per_line) or (column >= num_columns):
                vals_count = 0
                column = 0
                i_free_cells_row += 1
                if i_free_cells_row >= len(rows_with_free_cells):
                    break

                row = rows_with_free_cells[i_free_cells_row]

                if (rows_num_free_cells[row]) == num_rows:
                    num_vals_per_line = lines_len

                else:
                    num_vals_per_line = min(
                        rows_num_free_cells[row],
                        num_estim_vals_equations // lines_len
                        )

            if (row, column) in occupied_cells:
                column += 1
                continue

            if column < num_columns:
                i_x = (row * num_columns) + column

                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

                vals_count += 1
                column += 1

                i_equation += 1
                one_equation_coeffs = num_values * [0]

    elif len(columns_with_free_cells) > 0:
        columns_with_free_cells = list(columns_with_free_cells)

        columns_with_free_cells.sort()

        vals_count = 0
        i_free_cells_column = 0
        row = 0
        i_equation = 0

        column = columns_with_free_cells[i_free_cells_column]

        if (columns_num_free_cells[column]) == num_columns:
            num_vals_per_line = lines_len

        else:
            num_vals_per_line = min(
                columns_num_free_cells[column],
                num_estim_vals_equations // lines_len)

        one_equation_coeffs = num_values * [0]

        while i_equation < num_estim_vals_equations:

            if (vals_count >= num_vals_per_line) or (row >= num_rows):
                vals_count = 0
                row = 0

                i_free_cells_column += 1
                if i_free_cells_column >= len(columns_with_free_cells):
                    break

                column = columns_with_free_cells[i_free_cells_column]

                if (columns_num_free_cells[column]) == num_columns:
                    num_vals_per_line = lines_len

                else:
                    num_vals_per_line = min(
                        columns_num_free_cells[column],
                        num_estim_vals_equations // lines_len
                        )

            if (row, column) in occupied_cells:
                row += 1
                continue

            if row < num_rows:
                i_x = (row * num_columns) + column

                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

                vals_count += 1
                row += 1

                i_equation += 1
                one_equation_coeffs = num_values * [0]

    return equations_coeffs


def build_estim_vals_equations_consts(
        estim_vals_permut
        ):
    """
    Build constants for estimated values equations
    """

    equations_consts = []

    for value in estim_vals_permut:
        equations_consts.append(value)

    return equations_consts


def build_equations_coeffs(
        fixed_equations_coeffs,
        def_lines_equations_coeffs,
        estim_vals_equations_coeffs
        ):
    """
    Build coefficients for all equations
    """

    coeffs_matrix = []

    for coeffs in fixed_equations_coeffs:
        coeffs_matrix.append(coeffs)

    for coeffs in def_lines_equations_coeffs:
        coeffs_matrix.append(coeffs)

    for coeffs in estim_vals_equations_coeffs:
        coeffs_matrix.append(coeffs)

    return coeffs_matrix


def build_equations_consts(
        fixed_equations_consts,
        def_lines_equations_consts,
        estim_vals_equations_consts
        ):
    """
    Build constants for all equations
    """
    consts_matrix = []

    consts_matrix.extend(fixed_equations_consts)
    consts_matrix.extend(def_lines_equations_consts)
    consts_matrix.extend(estim_vals_equations_consts)

    return consts_matrix


def handle_exception(
        e, result,
        coeffs_matrix, consts_matrix,

        fixed_equations_coeffs,
        def_lines_equations_coeffs,
        estim_vals_equations_coeffs,

        fixed_equations_consts,
        def_lines_equations_consts,
        estim_vals_equations_consts
        ):

    """
    Handle exception
    """

    if str(e) in result["exceptions"]:
        return False

    else:
        print()
        print()

        print(e)

        print()
        print()

        """
        print()
        print("consts matrix")
        print(consts_matrix)

        print()
        print("coeffs matrix")
        for coeffs in coeffs_matrix:
            print(coeffs)

        print()
        print("consts fixed matrix")
        print(fixed_equations_consts)

        print()
        print("coeffs fixed matrix")
        for coeffs in fixed_equations_coeffs:
            print(coeffs)

        print()
        print("consts def lines matrix")
        print(def_lines_equations_consts)

        print()
        print("coeffs def lines matrix")
        for coeffs in def_lines_equations_coeffs:
            print(coeffs)

        print()
        print("consts estim vals matrix")
        print(estim_vals_equations_consts)

        print()
        print("coeffs estim vals matrix")
        for coeffs in estim_vals_equations_coeffs:
            print(coeffs)

        print()
        """

        return True


def solve_equations(
        coeffs_array, consts_array,
        result,

        coeffs_matrix, consts_matrix,

        fixed_equations_coeffs,
        def_lines_equations_coeffs,
        estim_vals_equations_coeffs,

        fixed_equations_consts,
        def_lines_equations_consts,
        estim_vals_equations_consts
        ):
    """
    Solve equations
    """

    solution = {}

    x = []
    solutions_count = result["solutions_count"]

    exception = None
    exceptions_count = result["exceptions_count"]

    try:
        x = np.linalg.solve(coeffs_array, consts_array)

    except Exception as e:
        exception = e
        exceptions_count += 1

        handle_exception(
            e, result,
            coeffs_matrix, consts_matrix,

            fixed_equations_coeffs,
            def_lines_equations_coeffs,
            estim_vals_equations_coeffs,

            fixed_equations_consts,
            def_lines_equations_consts,
            estim_vals_equations_consts
            )

    else:
        solutions_count += 1

    finally:
        print(
            (
                f"{solutions_count} Solut   "
                f"{exceptions_count} Except   "
                f"{exception}   Solution: {x}"
            ),
            end="\r"
            )

    solution["x"] = x
    solution["solutions_count"] = solutions_count

    solution["exception"] = exception
    solution["exceptions_count"] = exceptions_count

    return solution


def quadrado_magico_com_equacoes(
        def_lines, num_def_lines,
        def_lines_vals, estim_vals,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Quadrado magico sem equacoes
    """

    # Initialize result
    result = {}

    result["solutions"] = []
    result["solutions_count"] = 0

    result["valid_solutions"] = []
    result["valid_solutions_count"] = 0

    result["exceptions"] = set()
    result["exceptions_count"] = 0

    result["erro"] = ""

    # Calculate number of lines
    num_lines = lines_len

    # Calculate number of equations
    num_equations = num_values

    # Calculate number of defined lines equations
    num_def_lines_equations = def_lines_vals

    # Calculate number of fixed equations
    num_fixed_equations = num_equations - num_def_lines_equations
    if num_fixed_equations > num_lines:
        num_fixed_equations = num_lines

    # Check number of fixed equations
    if num_fixed_equations < num_lines:
        error = (
            f"Number of fixed equations {num_fixed_equations} <"
            f"number of lines {num_lines}"
            )

        result["error"] = error

        return result

    # Calculate number of estimated values equations
    num_estim_vals_equations = (
        num_equations - num_def_lines_equations - num_fixed_equations
    )

    # Build coefficients for fixed equations
    fixed_equations_coeffs = build_fixed_equations_coeffs(
        num_fixed_equations,
        lines_len, num_values
        )

    # Build constants for fixed equations
    fixed_equations_consts = num_fixed_equations * [lines_sum]

    # Build estimated values permutations
    num_estim_vals_to_permut = num_estim_vals_equations

    estim_vals_permuts = build_estim_vals_permuts(
        estim_vals, num_estim_vals_to_permut
        )

    # If there are not any defined lines
    if num_def_lines < 1:

        # Build coefficients for estimated values equations
        def_lines_pos_permut = []

        estim_vals_equations_coeffs = build_estim_vals_equations_coeffs(
            num_estim_vals_equations, def_lines_pos_permut,
            lines_len, num_values
            )

        # For each estimated values permutation
        for estim_vals_permut in estim_vals_permuts:

            # Build constants for estimated values equations
            estim_vals_equations_consts = build_estim_vals_equations_consts(
                estim_vals_permut
                )

            # Build coefficients for all equations
            def_lines_equations_coeffs = []

            coeffs_matrix = build_equations_coeffs(
                fixed_equations_coeffs,
                def_lines_equations_coeffs,
                estim_vals_equations_coeffs
                )

            coeffs_array = np.array(coeffs_matrix)

            # Build constants for all equations
            def_lines_equations_consts = []

            consts_matrix = build_equations_consts(
                fixed_equations_consts,
                def_lines_equations_consts,
                estim_vals_equations_consts
                )

            consts_array = np.array(consts_matrix)

            # Solve equations
            solution = solve_equations(
                coeffs_array, consts_array,
                result,

                coeffs_matrix, consts_matrix,

                fixed_equations_coeffs,
                def_lines_equations_coeffs,
                estim_vals_equations_coeffs,

                fixed_equations_consts,
                def_lines_equations_consts,
                estim_vals_equations_consts
                )

            result["solutions"].append(solution["x"])
            result["solutions_count"] = solution["solutions_count"]

            result["exceptions"].add(solution["exception"])
            result["exceptions_count"] = solution["exceptions_count"]

            solution_check = check_solution(
                solution["x"],
                lines_len, lines_sum, max_value, num_values
                )

            if len(solution_check) > 0:
                result["valid_solution_count"] += 1

                result["valid_solutions"].append(solution_check)

    # Else there are defined lines
    else:

        # Convert estimated values permutations to list because if not
        # it cause failures on iterating this sequence,
        # and if the conversion is made at the sequence generation
        # it cause memory error when the sequence is too big
        estim_vals_permuts_list = list(estim_vals_permuts)

        # Build defined lines values permutations
        def_lines_vals_permuts = build_def_lines_vals_permuts(
            def_lines, num_def_lines
            )

        # Build defined lines positions permutations
        def_lines_pos_permuts = build_def_lines_pos_permuts(
            num_def_lines, lines_len
            )

        # For each defined lines positions permutation
        for def_lines_pos_permut in def_lines_pos_permuts:

            # Build coefficients for defined line equations
            def_lines_equations_coeffs = build_def_lines_equations_coeffs(
                def_lines_pos_permut,
                lines_len, num_values
                )

            # Build coefficients for estimated values equations
            estim_vals_equations_coeffs = build_estim_vals_equations_coeffs(
                num_estim_vals_equations, def_lines_pos_permut,
                lines_len, num_values
                )

            # For each defined lines values permutations
            for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

                # Build constants for defined line equations
                def_lines_equations_consts = build_def_lines_equations_consts(
                    def_lines_vals_permut
                    )

                # For each estimated values permutation
                estim_vals_permut_counts = 0

                for estim_vals_permut in estim_vals_permuts_list:
                    estim_vals_permut_counts += 1

                    # Build constants for estimated values equations
                    estim_vals_equations_consts = (
                        build_estim_vals_equations_consts(
                            estim_vals_permut
                        )
                    )

                    # Build coefficients for all equations
                    coeffs_matrix = build_equations_coeffs(
                        fixed_equations_coeffs,
                        def_lines_equations_coeffs,
                        estim_vals_equations_coeffs
                        )

                    coeffs_array = np.array(coeffs_matrix)

                    # Build constants for all equations
                    consts_matrix = build_equations_consts(
                        fixed_equations_consts,
                        def_lines_equations_consts,
                        estim_vals_equations_consts
                        )

                    consts_array = np.array(consts_matrix)

                    # Solve equations
                    solution = solve_equations(
                        coeffs_array, consts_array,
                        result,

                        coeffs_matrix, consts_matrix,

                        fixed_equations_coeffs,
                        def_lines_equations_coeffs,
                        estim_vals_equations_coeffs,

                        fixed_equations_consts,
                        def_lines_equations_consts,
                        estim_vals_equations_consts
                        )

                    result["solutions"].append(solution["x"])
                    result["solutions_count"] = solution["solutions_count"]

                    result["exceptions"].add(solution["exception"])
                    result["exceptions_count"] = solution["exceptions_count"]

                    solution_check = check_solution(
                        solution["x"],
                        lines_len, lines_sum, max_value, num_values
                        )

                    if len(solution_check) > 0:
                        result["valid_solution_count"] += 1

                        result["valid_solutions"].append(solution_check)

                # if there are not any estimated values permutations
                if estim_vals_permut_counts < 1:

                    # Build coefficients for all equations
                    estim_vals_equations_coeffs = []

                    coeffs_matrix = build_equations_coeffs(
                        fixed_equations_coeffs,
                        def_lines_equations_coeffs,
                        estim_vals_equations_coeffs
                        )

                    coeffs_array = np.array(coeffs_matrix)

                    # Build constants for all equations
                    estim_vals_equations_consts = []

                    consts_matrix = build_equations_consts(
                        fixed_equations_consts,
                        def_lines_equations_consts,
                        estim_vals_equations_consts
                        )

                    consts_array = np.array(consts_matrix)

                    # Solve equations
                    solution = solve_equations(
                        coeffs_array, consts_array,
                        result,

                        coeffs_matrix, consts_matrix,

                        fixed_equations_coeffs,
                        def_lines_equations_coeffs,
                        estim_vals_equations_coeffs,

                        fixed_equations_consts,
                        def_lines_equations_consts,
                        estim_vals_equations_consts
                        )

                    result["solutions"].append(solution["x"])
                    result["solutions_count"] = solution["solutions_count"]

                    result["exceptions"].add(solution["exception"])
                    result["exceptions_count"] = solution["exceptions_count"]

                    solution_check = check_solution(
                        solution["x"],
                        lines_len, lines_sum, max_value, num_values
                        )

                    if len(solution_check) > 0:
                        result["valid_solution_count"] += 1

                        result["valid_solutions"].append(solution_check)

    return result
