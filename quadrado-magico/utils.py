import csv


# from numpy import det
import itertools


def load_line_len(directory):
    """
    Load line length from CSV file into memory.
    """

    # Line length default
    line_len = 4

    try:
        with open(f"{directory}/line-len.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                line_len = int(row["length"])

    except Exception:
        pass

    return line_len


def load_def_lines(directory, num_lines, line_len):
    """
    Load defined lines from CSV files into memory.
    """

    # Defined lines default (none)
    def_lines = set()

    lines = set()

    for i_line in range(num_lines):
        line_values = ()

        try:
            with open(
              f"{directory}/def-line-{num_lines}x{line_len}-{i_line}.csv",
              encoding="utf-8"
              ) as f:

                reader = csv.DictReader(f)

                for row in reader:
                    line_values.add(int(row["value"]))

        except Exception:
            pass

        line_values_count = len(line_values)

        if (line_values_count > 0) and (line_values_count <= line_len):
            lines.add(line_values)

    for line in lines:
        line_values = list(line)

        line_values_count = len(line_values)

        non_def_values = (line_len - line_values_count) * [None]

        line_values.extend(non_def_values)

        def_lines.add(line_values)

    return def_lines


def line_len_is_valid(line_len, line_sum):
    """
    Check if line legth is valid
    """

    return (line_len > 0) and ((line_len % 2) == (line_sum % 2))


def def_lines_are_valid(
        def_lines, line_len, num_lines, max_value, line_sum
        ):
    """
    Check if defined lines are valid
    """

    num_def_lines = len(def_lines)

    if num_def_lines == 0:
        return True

    elif num_def_lines > num_lines:
        return False

    else:
        for line in def_lines:
            values_count = 0
            values_sum = 0

            for value in line:
                if value is not None:
                    if (value < 1) or (value > max_value):
                        return False

                    else:
                        values_count += 1
                        values_sum += value

                        if values_sum > line_sum:
                            return False

            if values_count == line_len:
                if values_sum != line_sum:
                    return False

    return True


def get_def_lines_vals(def_lines):
    """
    Get defined lines values
    """

    def_lines_vals = set()

    for line in def_lines:
        for value in line:
            if value is not None:
                def_lines_vals.add(value)

    return def_lines_vals


def build_estim_vals(max_value, def_lines_vals):
    """
    Build estimated values
    """

    all_values = set(range(1, max_value + 1))

    estim_vals = all_values.difference(def_lines_vals)

    return estim_vals


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


def build_estim_vals_permuts(all_estim_vals, num_estim_vals_to_permut):
    """
    Build estimated values permutations
    """

    permut_length = num_estim_vals_to_permut

    permuts = build_permutations(all_estim_vals, permut_length)

    return permuts


def build_def_lines_pos_permuts(num_def_lines, line_len):
    """
    Build defined lines positions permutations
    """

    permuts = set()

    if num_def_lines < 1:
        return permuts

    id_rows = list(range(line_len))
    id_columns = list(range(line_len, 2 * line_len))
    id_diagonals = [2 * line_len, 2 * line_len + 1]

    rows_permuts = build_permutations(id_rows, num_def_lines)
    columns_permuts = build_permutations(id_columns, num_def_lines)

    permuts.union(rows_permuts)
    permuts.union(columns_permuts)

    if num_def_lines < 3:
        diagonals_permuts = build_permutations(id_diagonals, num_def_lines)
        permuts.union(diagonals_permuts)

    return permuts


def build_vals_pernuts_for_def_lines(
        def_lines, num_def_lines, line_len
        ):
    """
    Build values permutations for defined lines 
    """

    vals_permuts = set(0)

    # Build defined lines positions permutations
    def_lines_pos_permuts = build_def_lines_pos_permuts(
        num_def_lines, line_len
        )

    return vals_permuts


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


def output_solutions(solutions, line_length, max_value):
    """
    Output solutions
    """

    output_line_length = 80

    space = " "

    values_space = 1 * space
    frames_space = 3 * space

    value_length = (max_value // 10) + 1
    value_format = "{:^" + f"{value_length}" + "}"

    values_row = line_length * [1]
    one_frame_output = ""

    for i in range(len(values_row) - 1):
        one_frame_output += (
            f"{value_format}{values_space}".format(values_row[i])
        )
    one_frame_output += (
        f"{value_format}".format(values_row[len(values_row) - 1])
    )

    num_frames_per_output_row = (
        (output_line_length - len(frames_space))
        //
        (len(one_frame_output) + len(frames_space))
    )

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

                i_solution = (
                    (frames_row * num_frames_per_output_row) + frames_column
                )
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

            value_output = (
                f"{value_format}{values_space}".format(solution[i_value])
            )
            print(value_output, end=" ")

        values_column = line_length - 1
        i_value = (values_row * line_length) + values_column

        value_output = f"{value_format}".format(solution[i_value])
        print(value_output, end=" ")

        if frames_column < num_frames_per_output_row - 1:
            print(frames_space, end=" ")

        frames_column += 1


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
