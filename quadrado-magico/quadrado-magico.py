import csv
import sys

# from numpy import det
import itertools
import numpy as np


def load_line_length(directory):
    """
    Load line length from CSV file into memory.
    """

    # Line length default
    line_length = 4

    try:
        with open(f"{directory}/line-length.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                line_length = int(row["length"])
    except:
        pass

    return line_length


def load_def_lines(directory, num_lines):
    """
    Load defined lines from CSV files into memory.
    """

    # Defined lines default (none)
    def_lines = []

    for i in range(num_lines):
        line_values = []

        try:
            with open(f"{directory}/defined-line-{i}.csv", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    line_values.append(int(row["value"]))
        except:
            pass

        if len(line_values) > 0 :
            def_lines.append(line_values)

    return def_lines


def line_length_is_valid(line_length, line_sum):
    """
    Check if line legth is valid
    """

    return (line_length % 2) == (line_sum) % 2


def def_lines_are_valid(def_lines, line_length, num_lines, max_value, line_sum):
    """
    Check if defined lines are valid
    """

    num_def_lines = len(def_lines)
    if num_def_lines == 0:
        return True
    elif num_def_lines > num_lines:
        return False
    else:
        lines_set = set()

        for line in def_lines:
            line_set = set(line)

            num_line_values = len(line_set)
            if num_line_values != line_length:
                return False

            elif len(lines_set.intersection(line_set)) > 0:
                return False

            else:
                values_sum = 0
                for value in line:
                    if value < 1 or value > max_value:
                        return False
                    
                    else:
                        values_sum += value

                if values_sum != line_sum:
                    return False

                else:
                    lines_set = lines_set.union(line_set)

        return True


def build_fixed_equations_coeffs(num_fixed_equations, num_values, line_length):
    """
    Build coefficients for fixed equations
    """

    equations_coeffs = []

    for equation in range(num_fixed_equations):
        coeffs = num_values * [0]
        row = equation
        for column in range(line_length):
            cell = (row * num_fixed_equations) + column
            coeffs[cell] = 1

        equations_coeffs.append(coeffs)

    return equations_coeffs


def build_estim_vals(max_value, def_lines):
    """
    Build sorted estimated values
    """

    estim_vals = set(range(1, max_value + 1))

    def_vals = set()
    for line in def_lines:
        values = set(line)
        def_vals = def_vals.union(values)

    estim_vals = estim_vals.difference(def_vals)

    estim_vals = list(estim_vals)

    estim_vals.sort()

    return estim_vals


def build_valid_estim_vals_combs(estim_vals, combs_length, line_sum):
    """
    Build valid estimated values combinations
    """

    valid_combs = []

    combs = itertools.combinations(estim_vals, combs_length)

    for comb in combs:
        comb_sum = 0
        for value in comb:
            comb_sum += value

        if comb_sum <= line_sum:
            valid_combs.append(comb)

    return valid_combs


def build_valid_estim_vals_permuts(
    estim_vals, num_estim_vals_equations, line_length, line_sum, max_value
    ):
    """
    Build valid estimated values permutations
    """

    permuts_length = num_estim_vals_equations // line_length

    max_permuts_sum = 0
    for i in range(permuts_length):
        max_permuts_sum += max_value - i

    if max_permuts_sum <= line_sum:
        valid_permutations = list(itertools.permutations(estim_vals, permuts_length))
    
    else:
        valid_combs = build_valid_estim_vals_combs(estim_vals, permuts_length, line_sum)

        valid_permutations = []

        for comb in valid_combs:
            comb_permuts = itertools.permutations(comb)

            valid_permutations.extend(comb_permuts)

    return valid_permutations


def build_permutations(iterable, permut_length):
    """
    Build permutations
    """

    permuts = []

    if permut_length > 1:
        # permuts = list(itertools.permutations(iterable, permut_length))
        permuts = itertools.permutations(iterable, permut_length)

    elif permut_length == 1:
        for elem in iterable:
            permuts.append([elem])

    return permuts


def build_estim_vals_permuts2(estim_vals, num_estim_vals_equations, line_length, line_sum, num_def_lines):
    """
    Build estimated values permutations
    """

    permuts = []

    if num_def_lines < 1:
        permut_length = line_length

        permuts = build_permutations(estim_vals, permut_length)

        valid_permuts = []

        for permut in permuts:
            invalid_permut = False
            permut_sum = 0

            for value in permut:
                permut_sum += value

                if permut_sum > line_sum:
                    invalid_permut = True
                    break

            if (not invalid_permut) and (permut_sum == line_sum):
                valid_permuts.append(permut)

        permut_length = num_estim_vals_equations // line_length

        permuts = build_permutations(valid_permuts, permut_length)

    else:
        permut_length = num_estim_vals_equations // line_length

        permuts = build_permutations(estim_vals, permut_length)

        valid_permuts = []

        for permut in permuts:
            invalid_permut = False
            permut_sum = 0

            for value in permut:
                permut_sum += value

                if permut_sum > line_sum:
                    invalid_permut = True
                    break

            if (not invalid_permut):
                valid_permuts.append(permut)

        permut_length = line_length

        permuts = build_permutations(valid_permuts, permut_length)


    return permuts


def build_estim_vals_permuts(all_estim_vals, num_estim_vals_to_permut):
    """
    Build estimated values permutations
    """

    permut_length = num_estim_vals_to_permut

    permuts = build_permutations(all_estim_vals, permut_length)

    return permuts


def build_def_lines_vals_permuts(def_lines, num_def_lines):
    """
    Build defined lines values permutations
    """

    val_permuts = {}

    direct_permuts = []
    for line in def_lines:
        line_permuts = list(itertools.permutations(line))

        direct_permuts.append(line_permuts)

    val_permuts["direct"] = direct_permuts


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

    val_permuts["inverted"] = inverted_permuts


    return val_permuts


def build_def_lines_pos_permuts(num_def_lines, line_length):
    """
    Build defined lines positions permutations
    """

    if num_def_lines < 1:
        return []

    permuts = []

    id_rows = list(range(line_length))
    id_columns = list(range(line_length, 2 * line_length))
    id_diagonals = [2 * line_length, 2 * line_length + 1]

    """
    if num_def_lines == 1:
        for id in id_rows:
            id_list = [id]
            permuts.append(id_list)

        for id in id_columns:
            id_list = [id]
            permuts.append(id_list)

        for id in id_diagonals:
            id_list = [id]
            permuts.append(id_list)

    else:
        rows_permuts = list(itertools.permutations(id_rows, num_def_lines))
        columns_permuts = list(itertools.permutations(id_columns, num_def_lines))

        permuts.extend(rows_permuts)
        permuts.extend(columns_permuts)

        if num_def_lines < 3:
            diagonals_permuts = list(itertools.permutations(id_diagonals, num_def_lines))
            permuts.extend(diagonals_permuts)
    """

    rows_permuts = list(build_permutations(id_rows, num_def_lines))
    columns_permuts = list(build_permutations(id_columns, num_def_lines))

    permuts.extend(rows_permuts)
    permuts.extend(columns_permuts)

    if num_def_lines < 3:
        diagonals_permuts = list(build_permutations(id_diagonals, num_def_lines))
        permuts.extend(diagonals_permuts)

    return permuts


def build_def_lines_equations_coeffs(def_lines_pos_permut, line_length, num_values):
    """ 
    Build coefficients for defined lines equations
    """

    equations_coeffs = []

    for position in def_lines_pos_permut:

        if position < line_length:
            row = position
            for i_value in range(line_length):
                column = i_value
                i_x = (row * line_length) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

        elif position < 2 * line_length:
            column = position % line_length
            for i_value in range(line_length):
                row = i_value
                i_x = (row * line_length) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

        elif position == 2 * line_length:
            for i_value in range(line_length):
                row = i_value
                column = i_value
                i_x = (row * line_length) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

        elif position == (2 * line_length) + 1:
            for i_value in range(line_length):
                row = i_value
                column = (line_length - 1) - i_value
                i_x = (row * line_length) + column

                one_equation_coeffs = num_values * [0]
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

    return equations_coeffs


def build_def_lines_equations_consts(def_lines_vals_permut):
    """ 
    Build constants for defined lines equations
    """

    equations_consts = []

    for def_line_values in def_lines_vals_permut:

        for value in def_line_values:
            equations_consts.append(value)

    return equations_consts


def get_def_lines_cells_occupation(def_lines_pos_permut, line_length) :
    """ 
    Get cells occupation for defined lines
    """

    cells_occupation = {}

    rows_with_free_cells = set(list(range(line_length)))
    columns_with_free_cells = set(list(range(line_length)))

    rows_num_free_cells = line_length * [line_length]
    columns_num_free_cells = line_length * [line_length]

    occupied_cells = set()

    for position in def_lines_pos_permut:
        if position < line_length:
            row = position
            rows_with_free_cells.discard(row)
            rows_num_free_cells[row] = 0

            for column in range(line_length):
                occupied_cells.add((row, column))
                columns_num_free_cells[column] -= 1

        elif position < 2 * line_length:
            column = position % line_length
            columns_with_free_cells.discard(column)
            columns_num_free_cells[column] = 0

            for row in range(line_length):
                occupied_cells.add((row, column))
                rows_num_free_cells[row] -= 1

        elif position == 2 * line_length:
            for i_value in range(line_length):
                row = i_value
                column = i_value

                occupied_cells.add((row, column))
                rows_num_free_cells[row] -= 1
                columns_num_free_cells[column] -= 1

        elif position == (2 * line_length) + 1:
            for i_value in range(line_length):
                row = i_value
                column = (line_length - 1) - i_value

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


def build_estim_vals_equations_coeffs(num_estim_vals_equations, def_lines_pos_permut, line_length, num_values):
    """ 
    Build coefficients for estimated values equations
    """

    equations_coeffs = []

    def_lines_cells_occupation = get_def_lines_cells_occupation(def_lines_pos_permut, line_length) 

    rows_with_free_cells = def_lines_cells_occupation["rows_with_free_cells"]
    columns_with_free_cells = def_lines_cells_occupation["columns_with_free_cells"]

    rows_num_free_cells = def_lines_cells_occupation["rows_num_free_cells"]
    columns_num_free_cells = def_lines_cells_occupation["columns_num_free_cells"]

    occupied_cells = def_lines_cells_occupation["occupied_cells"]

    if len(rows_with_free_cells) > 0:
        rows_with_free_cells = list(rows_with_free_cells)
        rows_with_free_cells.sort()

        vals_count = 0
        i_free_cells_row = 0
        column = 0
        i_equation = 0

        row = rows_with_free_cells[i_free_cells_row]

        if (rows_num_free_cells[row]) == line_length:
            num_vals_per_line = line_length
        else:
            num_vals_per_line = min(rows_num_free_cells[row], num_estim_vals_equations // line_length)

        one_equation_coeffs = num_values * [0]

        while i_equation < num_estim_vals_equations:

            if (vals_count >= num_vals_per_line) or (column >= line_length):
                vals_count = 0
                column = 0
                
                i_free_cells_row += 1

                if i_free_cells_row >= len(rows_with_free_cells):
                    break

                row = rows_with_free_cells[i_free_cells_row]

                if (rows_num_free_cells[row]) == line_length:
                    num_vals_per_line = line_length
                else:
                    num_vals_per_line = min(rows_num_free_cells[row], num_estim_vals_equations // line_length)

            if (row, column) in occupied_cells:
                column += 1
                continue

            if column < line_length:
                i_x = (row * line_length) + column
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

        if (columns_num_free_cells[column]) == line_length:
            num_vals_per_line = line_length
        else:
            num_vals_per_line = min(columns_num_free_cells[column], num_estim_vals_equations // line_length)

        one_equation_coeffs = num_values * [0]

        while i_equation < num_estim_vals_equations:

            if (vals_count >= num_vals_per_line) or (row >= line_length):
                vals_count = 0
                row = 0
                
                i_free_cells_column += 1

                if i_free_cells_column >= len(columns_with_free_cells):
                    break

                column = columns_with_free_cells[i_free_cells_column]

                if (columns_num_free_cells[column]) == line_length:
                    num_vals_per_line = line_length
                else:
                    num_vals_per_line = min(columns_num_free_cells[column], num_estim_vals_equations // line_length)

            if (row, column) in occupied_cells:
                row += 1
                continue

            if row < line_length:
                i_x = (row * line_length) + column
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

                vals_count += 1
                row += 1
                
                i_equation += 1
                one_equation_coeffs = num_values * [0]


    return equations_coeffs    


def build_estim_vals_equations_consts(estim_vals_permut):
    """ 
    Build constants for estimated values equations
    """

    equations_consts = []

    for value in estim_vals_permut:
        equations_consts.append(value)

    return equations_consts


def estim_vals_cross_def_lines_are_valid(
    estim_vals_permut, num_def_lines, def_lines_vals_permut, def_lines_pos_permut,
    line_length, line_sum):

    """ 
    Check if estimamated values crossed with defined lines are valid
    """

    rows_sum = line_length * [0]
    columns_sum = line_length * [0]

    occupied_cells = set()

    non_full_def_line_exist = False

    for i_def_line in range(num_def_lines):

        position = def_lines_pos_permut[i_def_line]

        if position >= 2 * line_length:
            non_full_def_line_exist = True

            def_line_values = def_lines_vals_permut[i_def_line]

            if position == 2 * line_length:
                for i_value in range(line_length):
                    row = i_value
                    column = i_value

                    occupied_cells.add((row, column))

                    rows_sum[row] += def_line_values[row]
                    columns_sum[column] += def_line_values[column]

            elif position == (2 * line_length) + 1:
                for i_value in range(line_length):
                    row = i_value
                    column = (line_length - 1) - i_value

                    occupied_cells.add((row, column))

                    rows_sum[row] += def_line_values[row]
                    columns_sum[column] += def_line_values[column]

    if not non_full_def_line_exist:
        return True

    num_estim_vals_lines = len(estim_vals_permut)

    row = 0
    column = 0
    row_estim_val = 0
    column_estim_val = 0

    estim_values = estim_vals_permut[row_estim_val]
    while True:

        if column_estim_val >= len(estim_values):
            column_estim_val = 0

            row_estim_val += 1
            if row_estim_val >= num_estim_vals_lines:
                break

            estim_values = estim_vals_permut[row_estim_val]
            continue

        if column >= line_length:
            column = 0

            row += 1
            if row >= line_length:
                break

            continue

        if (row, column) in occupied_cells:
            column += 1
            continue

        rows_sum[row] += estim_values[column_estim_val]
        if rows_sum[row] > line_sum:
            return False

        columns_sum[column] += estim_values[column_estim_val]
        if columns_sum[column] > line_sum:
            return False

        column += 1


    return True


def build_equations_coeffs(fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs):
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


def build_equations_consts(fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts):
    """ 
    Build constants for all equations
    """
    consts_matrix = []

    consts_matrix.extend(fixed_equations_consts)
    consts_matrix.extend(def_lines_equations_consts)
    consts_matrix.extend(estim_vals_equations_consts)

    return consts_matrix


def handle_exception(e, exceptions,
    coeffs_matrix, fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs,
    consts_matrix, fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts
    ):

    """ 
    Handle exception
    """

    if (str(e) in exceptions):
        return False
    else:
        exceptions.add(str(e))

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


def solve_equations(coeffs_array, consts_array,
    coeffs_matrix, fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs,
    consts_matrix, fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts,
    solution_stats, exceptions_stats
    ):

    """ 
    Solve equations
    """

    solution = {}

    solutions_count = solution_stats["solutions_count"]

    exception = exceptions_stats["exception"]
    exceptions = exceptions_stats["exceptions"]
    exceptions_count = exceptions_stats["exceptions_count"]

    x = []

    try:
        x = np.linalg.solve(coeffs_array, consts_array)

    except Exception as e:
        exception = e
        exceptions_count += 1

        handle_exception(e, exceptions,
            coeffs_matrix, fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs,
            consts_matrix, fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts,
            )

    else:
        solutions_count += 1

    finally:
        print(f"{solutions_count} Solut   {exceptions_count} Except   {exception}   Solution: {x}", end="\r")


    solution_stats["solutions_count"] = solutions_count

    exceptions_stats["exception"] = exception
    exceptions_stats["exceptions"] = exceptions
    exceptions_stats["exceptions_count"] = exceptions_count

    solution["solution_stats"] = solution_stats
    solution["exceptions_stats"] = exceptions_stats
    solution["x"] = x

    return solution


def check_solution(x, line_length, num_values, max_value, line_sum):
    """ 
    Check solution
    """

    if len(x) != num_values:
        return []

    x_int = []
    for value in x:
        value_int = int(value)

        if value_int < 1:
            return []

        if value_int > max_value:
            return []

        x_int.append(value_int)

    x_set = set(x_int)
    if len(x_set) != num_values:
        return []

    for row in range(line_length):
        sum = 0
        for column in range(line_length):
            i_value = (row * line_length) + column

            sum += x_int[i_value]
            if sum > line_sum:
                return []
        
        if sum != line_sum:
            return []


    for column in range(line_length):
        sum = 0
        for row in range(line_length):
            i_value = (row * line_length) + column

            sum += x_int[i_value]
            if sum > line_sum:
                return []
        
        if sum != line_sum:
            return []

    sum_diagonal_1 = 0
    sum_diagonal_2 = 0
    for i in range(line_length):
        row = i
        column = i
        i_value = (row * line_length) + column

        sum_diagonal_1 += x_int[i_value]
        if sum_diagonal_1 > line_sum:
            return []

        column = (line_length - 1) - i_value
        i_value = (row * line_length) + column

        sum_diagonal_2 += x_int[i_value]
        if sum_diagonal_2 > line_sum:
            return []

    if sum_diagonal_1 != line_sum:
        return []

    if sum_diagonal_2 != line_sum:
        return []

    return x_int


def output_solutions(solutions, line_length, max_value):
    """ 
    Output solutions
    """

    output_line_length = 80

    space = " "

    values_space = 1 * space
    frames_space = 3 * space

    value_length = (max_value // 10) + 1
    value_format = "{:^" + f"{value_length}"+ "}"

    values_row = line_length * [1]
    one_frame_output = ""

    for i in range(len(values_row) - 1):
        one_frame_output += f"{value_format}{values_space}".format(values_row[i])
    one_frame_output += f"{value_format}".format(values_row[len(values_row) - 1])

    num_frames_per_output_row = (output_line_length - len(frames_space)) // (len(one_frame_output) + len(frames_space))

    frames_row = 0
    frames_column = 0
    values_row = 0

    print()
    print()
    while True:

        if frames_column >= num_frames_per_output_row:
            print()

            frames_column = 0

            values_row += 1
            if values_row >= line_length:
                values_row = 0
                frames_row += 1

                i_solution = (frames_row * num_frames_per_output_row) + frames_column
                if i_solution >= len(solutions):
                    break

                print()
                print()

                continue

        i_solution = (frames_row * num_frames_per_output_row) + frames_column
        if i_solution >= len(solutions):
            frames_column += 1
            continue

        solution = solutions[i_solution]

        for values_column in range(line_length - 1):
            i_value = (values_row * line_length) + values_column

            value_output = f"{value_format}{values_space}".format(solution[i_value])
            print(value_output, end=" ")

        values_column = line_length - 1
        i_value = (values_row * line_length) + values_column

        value_output = f"{value_format}".format(solution[i_value])
        print(value_output, end=" ")

        if frames_column < num_frames_per_output_row - 1:
            print(frames_space, end=" ")

        frames_column += 1


def main():
    # Get command line arguments
    if len(sys.argv) > 2:
        sys.exit("Usage: python quadrado-magico.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else ""

    # Load line length
    line_length = load_line_length(directory)

    # Set number of lines
    num_lines = line_length

    # Calculate max value
    max_value = line_length * num_lines

    # Calculate total number of values
    num_values = max_value

    # Calculate total sum of values
    total_sum = ((1 + max_value) * num_values) / 2

    # Calculate sum of values of each line
    line_sum = int(total_sum / num_lines)

    # Check if line length is valid
    if not line_length_is_valid(line_length, line_sum):
        sys.exit(f"Line length {line_length} is invalid")

    # Load defined lines
    def_lines = load_def_lines(directory, num_lines)

    # Check if defined lines are valid
    if not def_lines_are_valid(def_lines, line_length, num_lines, max_value, line_sum):
        sys.exit(f"Defined lines are invalid")

    # Calculate number of equations
    num_equations = num_values

    # Calculate number of defined lines
    num_def_lines = len(def_lines)

    # Calculate number of defined lines equations
    num_def_lines_equations = num_def_lines * line_length

    # Calculate number of fixed equations
    num_fixed_equations = num_equations - num_def_lines_equations
    if num_fixed_equations > num_lines:
        num_fixed_equations = num_lines

    # Check number of fixed equations
    if num_fixed_equations < num_lines:
        sys.exit(f"Number of fixed equations {num_fixed_equations} < number of lines {num_lines}")

    # Calculate number of estimated values equations
    num_estim_vals_equations = num_equations - num_def_lines_equations - num_fixed_equations

    # Build coefficients for fixed equations
    fixed_equations_coeffs = build_fixed_equations_coeffs(num_fixed_equations, num_values, line_length)

    # Build constants for fixed equations
    fixed_equations_consts = num_fixed_equations * [line_sum]

    # Build all estimated values
    all_estim_vals = build_estim_vals(max_value, def_lines)

    # Build estimated values permutations
    num_estim_vals_to_permut = num_estim_vals_equations

    estim_vals_permuts = build_estim_vals_permuts(
        all_estim_vals, num_estim_vals_to_permut
        )

    """
    count = 0
    for permut in estim_vals_permuts:
        count += 1
        # print(permut)

    print((len(all_estim_vals), num_estim_vals_equations))
    print(count)
    """

    solution_stats = {}

    solutions_count = 0
    solution_stats["solutions_count"] = solutions_count

    exceptions_stats = {}

    exception = None
    exceptions_stats["exception"] = exception

    exceptions = set()
    exceptions_stats["exceptions"] = exceptions

    exceptions_count = 0
    exceptions_stats["exceptions_count"] = exceptions_count

    valid_solution_count = 0
    valid_solutions = []

    # If there are not any defined lines
    if num_def_lines < 1:

        # Build coefficients for estimated values equations
        def_lines_pos_permut = []
        estim_vals_equations_coeffs = build_estim_vals_equations_coeffs(
            num_estim_vals_equations, def_lines_pos_permut, line_length, num_values
            )

        """
        print()
        print(def_lines_pos_permut) 
        for equation_coeffs in estim_vals_equations_coeffs:
            print(equation_coeffs)
        """

        # For each estimated values permutation
        for estim_vals_permut in estim_vals_permuts:
            
            # Build constants for estimated values equations
            estim_vals_equations_consts = build_estim_vals_equations_consts(estim_vals_permut)

            # Build coefficients for all equations
            def_lines_equations_coeffs = []
            coeffs_matrix = build_equations_coeffs(fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs)
            coeffs_array = np.array(coeffs_matrix)

            # Build constants for all equations
            def_lines_equations_consts = []
            consts_matrix = build_equations_consts(fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts)
            consts_array = np.array(consts_matrix)

            # Solve equations
            solution = solve_equations(coeffs_array, consts_array,
                coeffs_matrix, fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs,
                consts_matrix, fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts,
                solution_stats, exceptions_stats
                )

            solution_stats = solution["solution_stats"]
            exceptions_stats = solution["exceptions_stats"]
            x = solution["x"]

            solution_check = check_solution(x, line_length, num_values, max_value, line_sum)
            if len(solution_check) > 0:
                valid_solution_count += 1

                valid_solutions.append(solution_check)


    # Else there are defined lines
    else:

        # Convert estimated values permutations to list because if not it cause failures on iterating this sequence,
        # and if the conversion is made at the sequence generation it cause memory error when the sequence is too big
        estim_vals_permuts_list = list(estim_vals_permuts)

        # Build defined lines values permutations
        def_lines_vals_permuts = build_def_lines_vals_permuts(def_lines, num_def_lines)

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

        # Build defined lines positions permutations
        def_lines_pos_permuts = build_def_lines_pos_permuts(num_def_lines, line_length)

        """
        print()
        for permut in def_lines_pos_permuts:
            print(permut)

        print(len(def_lines_pos_permuts))
        """

        # For each defined lines positions permutation
        for def_lines_pos_permut in def_lines_pos_permuts:
            
            # Build coefficients for defined line equations
            def_lines_equations_coeffs = build_def_lines_equations_coeffs(
                def_lines_pos_permut, line_length, num_values
                )

            """
            print()
            print(def_lines_pos_permut) 
            for equation_coeffs in def_lines_equations_coeffs:
                print(equation_coeffs)
            """

            # Build coefficients for estimated values equations
            estim_vals_equations_coeffs = build_estim_vals_equations_coeffs(
                num_estim_vals_equations, def_lines_pos_permut, line_length, num_values
                )

            """
            print()
            print(num_estim_vals_equations)
            print(def_lines_pos_permut)
            # print(estim_vals_equations_coeffs) 
            for equation_coeffs in estim_vals_equations_coeffs:
                print(equation_coeffs)
            """

            # For each defined lines values permutations
            for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

                # Build constants for defined line equations
                def_lines_equations_consts = build_def_lines_equations_consts(def_lines_vals_permut)

                """
                print()
                print(def_lines_vals_permut)
                print(def_lines_equations_consts)

                print()
                print(def_lines_pos_permut) 
                for equation_coeffs in def_lines_equations_coeffs:
                    print(equation_coeffs)
                """

                # For each estimated values permutation
                estim_vals_permut_counts = 0
                for estim_vals_permut in estim_vals_permuts_list:
                    estim_vals_permut_counts += 1

                    # If estimated values crossed with defined lines values are valid
                    """
                    if estim_vals_cross_def_lines_are_valid(
                        estim_vals_permut, num_def_lines, def_lines_vals_permut, def_lines_pos_permut,
                        line_length, line_sum
                        ):
                    """
                    if True:

                        # Build constants for estimated values equations
                        estim_vals_equations_consts = build_estim_vals_equations_consts(estim_vals_permut)

                        # Build coefficients for all equations
                        coeffs_matrix = build_equations_coeffs(fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs)
                        coeffs_array = np.array(coeffs_matrix)

                        # Build constants for all equations
                        consts_matrix = build_equations_consts(fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts)
                        consts_array = np.array(consts_matrix)

                        # Solve equations
                        solution = solve_equations(coeffs_array, consts_array,
                            coeffs_matrix, fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs,
                            consts_matrix, fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts,
                            solution_stats, exceptions_stats
                            )

                        solution_stats = solution["solution_stats"]
                        exceptions_stats = solution["exceptions_stats"]
                        x = solution["x"]

                        solution_check = check_solution(x, line_length, num_values, max_value, line_sum)
                        if len(solution_check) > 0:
                            valid_solution_count += 1

                            valid_solutions.append(solution_check)


                # if there are not any estimated values permutations 
                if estim_vals_permut_counts < 1:

                    # Build coefficients for all equations
                    estim_vals_equations_coeffs = []
                    coeffs_matrix = build_equations_coeffs(fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs)
                    coeffs_array = np.array(coeffs_matrix)

                    # Build constants for all equations
                    estim_vals_equations_consts = []
                    consts_matrix = build_equations_consts(fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts)
                    consts_array = np.array(consts_matrix)

                    # Solve equations
                    solution = solve_equations(coeffs_array, consts_array,
                        coeffs_matrix, fixed_equations_coeffs, def_lines_equations_coeffs, estim_vals_equations_coeffs,
                        consts_matrix, fixed_equations_consts, def_lines_equations_consts, estim_vals_equations_consts,
                        solution_stats, exceptions_stats
                        )

                    solution_stats = solution["solution_stats"]
                    exceptions_stats = solution["exceptions_stats"]
                    x = solution["x"]

                    solution_check = check_solution(x, line_length, num_values, max_value, line_sum)
                    if len(solution_check) > 0:
                        valid_solution_count += 1

                        valid_solutions.append(solution_check)


    print()
    print()

    output_solutions(valid_solutions, line_length, max_value)

    print()
    print()

    solutions_count = solution_stats["solutions_count"]

    print()
    print('Number of Valid Solutions')
    print(valid_solution_count)

    print()
    print('Number of Solutions')
    print(solutions_count)

    exceptions_count = exceptions_stats["exceptions_count"]

    print()
    print('Number of Exceptions')
    print(exceptions_count)

    return


if __name__ == "__main__":
    main()
