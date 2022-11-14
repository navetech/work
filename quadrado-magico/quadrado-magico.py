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
        permuts = itertools.permutations(iterable, permut_length)

    elif permut_length == 1:
        for elem in iterable:
            permuts.append([elem])

    return permuts


def build_estim_vals_permuts(estim_vals, num_estim_vals_equations, line_length, line_sum, num_def_lines):
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


def build_estim_vals_equations_coeffs(num_estim_vals_equations, def_lines_pos_permut, line_length, num_values):
    """ 
    Build coefficients for estimated values equations
    """

    equations_coeffs = []

    max_num_cells_per_line = num_estim_vals_equations // line_length

    total_free_rows = set(list(range(line_length)))
    total_free_columns = set(list(range(line_length)))

    occupied_cells = set()

    for position in def_lines_pos_permut:
        if position < line_length:
            row = position
            total_free_rows.discard(row)

            for column in range(line_length):
                total_free_columns.discard(column)

        elif position < 2 * line_length:
            column = position % line_length
            total_free_columns.discard(column)

            for row in range(line_length):
                total_free_rows.discard(row)

        elif position == 2 * line_length:
            for i_value in range(line_length):
                row = i_value
                column = i_value
                occupied_cells.add((row, column))

        elif position == (2 * line_length) + 1:
            for i_value in range(line_length):
                row = i_value
                column = (line_length - 1) - i_value
                occupied_cells.add((row, column))

    if len(total_free_rows) > 0:
        total_free_rows = list(total_free_rows)
        total_free_rows.sort()

        cells_count = 0
        i_free_row = 0
        column = 0
        i_equation = 0
        while i_equation < num_estim_vals_equations:
            one_equation_coeffs = num_values * [0]

            if i_free_row >= len(total_free_rows):
                break

            if (cells_count >= max_num_cells_per_line) or (column >= line_length):
                cells_count = 0
                column = 0
                i_free_row += 1

                continue

            row = total_free_rows[i_free_row]

            if (row, column) in occupied_cells:
                column += 1
                continue

            if column < line_length:
                i_x = (row * line_length) + column
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

                cells_count += 1
                column += 1
                i_equation += 1

    elif len(total_free_columns) > 0:
        total_free_columns = list(total_free_columns)
        total_free_columns.sort()

        cells_count = 0
        i_free_column = 0
        row = 0
        i_equation = 0
        while i_equation < num_estim_vals_equations:
            one_equation_coeffs = num_values * [0]

            if i_free_column >= len(total_free_columns):
                break

            if (cells_count >= max_num_cells_per_line) or (row >= line_length):
                cells_count = 0
                row = 0
                i_free_column += 1

                continue

            column = total_free_columns[i_free_column]

            if (row, column) in occupied_cells:
                row += 1
                continue

            if row < line_length:
                i_x = (row * line_length) + column
                one_equation_coeffs[i_x] = 1
                equations_coeffs.append(one_equation_coeffs)

                cells_count += 1
                row += 1
                i_equation += 1


    return equations_coeffs    


def build_estim_vals_equations_consts(estim_vals_permut):
    """ 
    Build constants for estimated values equations
    """

    equations_consts = []

    for estim_values in estim_vals_permut:
        for value in estim_values:
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
    estim_vals = build_estim_vals(max_value, def_lines)

    """
    # Build valid estimated values permutations
    valid_estim_vals_permuts = build_valid_estim_vals_permuts(
        estim_vals, num_estim_vals_equations, line_length, line_sum, max_value
        )

    # Build estimated values permutations for equations
    equations_estim_vals_permuts = itertools.permutations(valid_estim_vals_permuts, line_length)
    """

    # Build estimated values permutations
    estim_vals_permuts = build_estim_vals_permuts(
        estim_vals, num_estim_vals_equations, line_length, line_sum, num_def_lines
        )

    """
    count = 0
    for permut in estim_vals_permuts:
        count += 1
        # print(permut)

    print(count)
    """

    solutions_count = 0
    solve_exceptions_count = 0

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
            coeffs_matrix = []

            for coeffs in fixed_equations_coeffs:
                coeffs_matrix.append(coeffs)

            for coeffs in estim_vals_equations_coeffs:
                coeffs_matrix.append(coeffs)

            # Build constants for all equations
            consts_matrix = []

            consts_matrix.extend(fixed_equations_consts)
            consts_matrix.extend(estim_vals_equations_consts)

            # Solve equations
            a = np.array(coeffs_matrix)
            b = np.array(consts_matrix)

            try:
                x = np.linalg.solve(a, b)

                solutions_count += 1

                print(x)

            except:
                solve_exceptions_count += 1

                print(solve_exceptions_count)

                pass

    # Else there are defined lines
    else:

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

        # For each defined lines values permutations
        for def_lines_vals_permut in def_lines_vals_permuts["inverted"]:

            # Build constants for defined line equations
            def_lines_equations_consts = build_def_lines_equations_consts(def_lines_vals_permut)

            """
            print()
            print(def_lines_vals_permut)
            print(def_lines_equations_consts)
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

                print()
                print(num_estim_vals_equations)
                print(def_lines_pos_permut)
                print(estim_vals_equations_coeffs) 
                for equation_coeffs in estim_vals_equations_coeffs:
                    print(equation_coeffs)

                continue

                # For each estimated values permutation
                estim_vals_permut_counts = 0
                for estim_vals_permut in estim_vals_permuts:
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
                        coeffs_matrix = []

                        for coeffs in fixed_equations_coeffs:
                            coeffs_matrix.append(coeffs)

                        for coeffs in def_lines_equations_coeffs:
                            coeffs_matrix.append(coeffs)

                        for coeffs in estim_vals_equations_coeffs:
                            coeffs_matrix.append(coeffs)

                        # Build constants for all equations
                        consts_matrix = []

                        consts_matrix.extend(fixed_equations_consts)
                        consts_matrix.extend(def_lines_equations_consts)
                        consts_matrix.extend(estim_vals_equations_consts)

                        # Solve equations
                        a = np.array(coeffs_matrix)
                        b = np.array(consts_matrix)

                        try:
                            x = np.linalg.solve(a, b)

                            solutions_count += 1

                            print(x)

                        except:
                            solve_exceptions_count += 1

                            print(solve_exceptions_count)

                            pass

                # if there are not any estimated values permutations 
                if estim_vals_permut_counts < 1:

                    # Build coefficients for all equations
                    coeffs_matrix = []

                    for coeffs in fixed_equations_coeffs:
                        coeffs_matrix.append(coeffs)

                    for coeffs in def_lines_equations_coeffs:
                        coeffs_matrix.append(coeffs)

                    # Build constants for all equations
                    consts_matrix = []

                    consts_matrix.extend(fixed_equations_consts)
                    consts_matrix.extend(def_lines_equations_consts)

                    # Solve equations
                    a = np.array(coeffs_matrix)
                    b = np.array(consts_matrix)

                    try:
                        x = np.linalg.solve(a, b)

                        solutions_count += 1

                        print(x)

                    except:
                        solve_exceptions_count += 1

                        print(solve_exceptions_count)

                        pass
    
    print()
    print('Number of Solutions')
    print(solutions_count)

    print()
    print('Number of Solve Exceptions')
    print(solve_exceptions_count)

    return

    inline_defined_values = loaded_data["inline_defined_values"]

    # Build non-define values
    non_defined_values = set(range(1,17)) - inline_defined_values

    # Calculate number of estimated equations
    number_of_estimated_equations = 6 - len(inline_defined_values)

    # Build permutations of non-defined values
    permutations = itertools.permutations(non_defined_values, number_of_estimated_equations)
    non_def_permutations = set()
    for permutation in permutations:
        non_def_permutations.add(permutation)

    # Get permutations of inline defined values
    one_line_def_values = list(inline_defined_values)
    if len(inline_defined_values) > 0:
        for i in range(len(inline_defined_values), 4):
            one_line_def_values.append(None)

    permutations = itertools.permutations(one_line_def_values)
    def_permutations = set()
    for permutation in permutations:
        def_permutations.add(permutation)

    # Build fixed equations
    fixed_equations_coefficients = build_fixed_equations_coefficients()
    fixed_equations_constants = 10 * [34]

    # IF there are not any inline defined valuese
    if len(inline_defined_values) < 1:

        # For each permutation of non-defined values
        for non_def_permutation in non_def_permutations:

            break

            # Build estimated equations
            estimated_equations_coefficients = build_estimated_equations_coefficients(non_def_permutation)
            estimated_equations_constants = list(non_def_permutation)

            # Solve equations
            coefficients_matrix = []

            for coefficients in fixed_equations_coefficients:
                coefficients_matrix.append(coefficients)

            for coefficients in estimated_equations_coefficients:
                coefficients_matrix.append(coefficients)

            a = np.array(coefficients_matrix)

            constants_matrix = []
            constants_matrix.extend(fixed_equations_constants)
            constants_matrix.extend(estimated_equations_constants)

            b = np.array(constants_matrix)

            """
            for matrix in coefficients_matrix:
                print(matrix)

            print(constants_matrix)
            """

            try:
                x = np.linalg.solve(a, b)
                print(x)
            except:
                pass

            # x = np.linalg.solve(a, b)

            # print(x)


        # Else
        else:

            # For each permutation of inline defined values
            for def_permutation in def_permutations:

                # for each line of the magic square
                for defined_line in range(10):

                    # Build equations for defined line
                    def_line_equations_coefficients = build_def_line_equations_coefficients(def_permutation, defined_line)
                    def_line_equations_constants = build_def_line_equations_constants(def_permutation)

                    # For each permutation of non-defined values
                    for non_def_permutation in non_def_permutations:

                        # Build estimated equations
                        estimated_equations_coefficients = build_estimated_equations_coefficients(non_def_permutation, defined_line)
                        estimated_equations_constants = list(non_def_permutation)

                        # Solve equationsutations:
                        coefficients_matrix = []

                        for coefficients in fixed_equations_coefficients:
                            coefficients_matrix.append(coefficients)

                        for coefficients in def_line_equations_coefficients:
                            coefficients_matrix.append(coefficients)

                        for coefficients in estimated_equations_coefficients:
                            coefficients_matrix.append(coefficients)

                        a = np.array(coefficients_matrix)

                        constants_matrix = []
                        constants_matrix.extend(fixed_equations_constants)
                        constants_matrix.extend(def_line_equations_constants)
                        constants_matrix.extend(estimated_equations_constants)

                        b = np.array(constants_matrix)

                        x = np.linalg.solve(a, b)

                        # print(x)




    c00 = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c01 = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    c02 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    c03 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    c04 = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    c05 = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    c06 = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
    c07 = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
    c08 = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    c09 = [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    # c10 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # c11 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # c12 = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # c13 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # c14 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # c15 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    c00 = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c01 = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c02 = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c03 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c04 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c05 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c06 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c07 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    c08 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    c09 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    c10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    c11 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    c12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    c14 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    c15 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]



    c = []
    for i in range(16):
        l = 16 * [0]
        for j in range(16):
            if i == 0:
                l = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
            elif i == 1:
                l = [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0]
            elif i == 2:
                l = [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0]
            elif i == 3:
                l = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
            elif i == 4:
                # l = [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]
                l = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            elif i == 5:
                # l = [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0]
                l = [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
            elif i == 6:
                # l = [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0]
                l = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
            elif i == 7:
                # l = [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1]
                l = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
            elif i == 8:
                # l = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
                l = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            elif i == 9:
                # l = [0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0]
                l = [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
            elif i == 10:
                l = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
            elif i == 11:
                l = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
            elif i == 12:
                l = [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
            elif i == 13:
                l = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
            elif i == 14:
                l = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
            elif i == 15:
                l = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
            else:
                l[j] = random.randint(2, 258)
        c.append(l)

    for l in c:
        print(l)
            
        


    # a = np.array([c00,c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15])
    a = np.array(c)

    # v = [34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 1, 8, 2, 3, 5, 4]
    # v = [34, 34, 34, 34, 1, 8, 10, 15, 12, 13, 3, 6, 7, 2, 16, 9]
    v = [34, 34, 34, 34, 1, 12, 15, 6, 8, 13, 10, 3, 14, 7, 4, 9]

    b = np.array(v)

    print(np.linalg.det(a))

    x = np.linalg.solve(a, b)

    print(x)


if __name__ == "__main__":
    main()
