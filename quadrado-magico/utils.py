import csv


# from numpy import det
import itertools


def load_def_lines(filename, lines_len):
    """
    Load defined lines from CSV file into memory.
    """

    # Defined lines default (none)
    def_lines = []

    num_rows = lines_len
    num_columns = lines_len

    try:
        with open(filename, encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:
                row_keys = row.keys()

                num_row_columns = len(row_keys)
                if num_row_columns > num_columns:
                    return None

                row_values = []

                for i in range(1, num_row_columns + 1):
                    key = f"value{i}"

                    try:
                        row_values.append(int(row[key]))

                    except Exception as e:
                        print("key exception")
                        print(e)

                        return None

                def_lines.append(row_values)

                if len(def_lines) > num_rows:
                    return None

    except Exception as e:
        print("with exception")
        print(e)

    return def_lines


# def lines_len_is_valid(lines_len, lines_sum):
    """
    Check if lines legth is valid
    """

    # return (lines_len > 0) and ((lines_len % 2) == (lines_sum % 2))


def def_lines_are_valid(
        def_lines,
        lines_len, lines_sum, max_value
        ):
    """
    Check if defined lines are valid
    """

    if def_lines is None:
        return False

    num_def_lines = len(def_lines)

    if num_def_lines == 0:
        return True

    num_lines = lines_len

    if num_def_lines > num_lines:
        return False

    lines_diff_values = set()

    for line_values in def_lines:
        line_values_count = len(line_values)

        if line_values_count > lines_len:
            return False

        line_diff_values = set(line_values)

        if len(line_diff_values) != line_values_count:
            return False

        if len(lines_diff_values.intersection(line_diff_values)) > 0:
            return False

        lines_diff_values = lines_diff_values.union(line_diff_values)

        values_sum = 0

        for value in line_values:
            if (value < 1) or (value > max_value):
                return False

            values_sum += value

            if values_sum > lines_sum:
                return False

        if line_values_count == lines_len:
            if values_sum != lines_sum:
                return False

    return True


def get_def_lines_vals(def_lines):
    """
    Get defined lines values
    """

    lines_vals = set()

    for line_vals in def_lines:
        lines_vals = lines_vals.union(set(line_vals))

    return lines_vals


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


def check_solution(
        values,
        lines_len, lines_sum, max_value, num_values
        ):
    """
    Check solution
    """

    # Check number of values of solution
    if len(values) != num_values:
        return []

    # Check each value of solution
    values_int = []
    for value in values:
        value_int = int(value)

        if (value_int < 1) or (value_int > max_value):
            return []

        values_int.append(value_int)

    # Check if values of solution are different
    valus_set = set(values_int)
    if len(valus_set) != num_values:
        return []

    num_rows = lines_len
    num_columns = lines_len

    # Check rows sums of solution
    for row in range(num_rows):
        values_sum = 0

        for column in range(num_columns):
            i_value = (row * num_columns) + column

            values_sum += values_int[i_value]

            if values_sum > lines_sum:
                return []

        if values_sum != lines_sum:
            return []

    # Check columns sums of solution
    for column in range(num_columns):
        values_sum = 0

        for row in range(num_rows):
            i_value = (row * num_columns) + column

            values_sum += values_int[i_value]

            if values_sum > lines_sum:
                return []

        if values_sum != lines_sum:
            return []

    # Check diagonals sums of solution
    sum_diagonal_1 = 0
    sum_diagonal_2 = 0

    for i in range(lines_len):
        row = i
        column = i

        i_value = (row * num_columns) + column

        sum_diagonal_1 += values_int[i_value]
        if sum_diagonal_1 > lines_sum:
            return []

        column = (num_columns - 1) - i

        i_value = (row * num_columns) + column

        sum_diagonal_2 += values_int[i_value]
        if sum_diagonal_2 > lines_sum:
            return []

    if sum_diagonal_1 != lines_sum:
        return []

    if sum_diagonal_2 != lines_sum:
        return []

    return values_int


def output_solutions(solutions, lines_len, max_value):
    """
    Output solutions
    """

    output_line_len = 80

    space = " "

    values_space = 1 * space
    frames_space = 3 * space

    value_length = (max_value // 10) + 1

    value_format = "{:^" + f"{value_length}" + "}"

    num_values_rows = lines_len
    num_values_columns = lines_len

    example_value = 1

    frame_output = ""

    for i in range(num_values_columns - 1):
        frame_output += (
            f"{value_format}{values_space}".format(example_value)
        )

    frame_output += (
        f"{value_format}".format(example_value)
    )

    num_frames_per_output_line = (
        (output_line_len - len(frames_space))
        //
        (len(frame_output) + len(frames_space))
    )

    frames_row = 0
    frames_column = 0
    values_row = 0

    print()
    print()
    
    while True:

        if frames_column >= num_frames_per_output_line:
            print()

            frames_column = 0

            values_row += 1

            if values_row >= num_values_rows:
                values_row = 0

                frames_row += 1

                i_solution = (
                    (frames_row * num_frames_per_output_line) + frames_column
                )

                if i_solution >= len(solutions):
                    break

                print()
                print()

                continue

        i_solution = (frames_row * num_frames_per_output_line) + frames_column

        if i_solution >= len(solutions):
            frames_column += 1

            continue

        solution = solutions[i_solution]

        for values_column in range(num_values_columns - 1):
            i_value = (values_row * num_values_columns) + values_column

            value_output = (
                f"{value_format}{values_space}".format(solution[i_value])
            )

            print(value_output, end=" ")

        values_column = num_values_columns - 1

        i_value = (values_row * num_values_columns) + values_column

        value_output = f"{value_format}".format(solution[i_value])

        print(value_output, end=" ")

        if frames_column < num_frames_per_output_line - 1:
            print(frames_space, end=" ")

        frames_column += 1
