import csv


# from numpy import det
import itertools


def remove_duplicates_list(src):
    """
    Remove duplicates from a list.
    """

    dst = []

    for x in src:
        if x not in dst:
            dst.append(x)

    return dst


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


def def_lines_are_full_lines(def_lines, lines_len):
    """
    Check if defined lines are full lines
    """

    if len(def_lines) == 0:
        return True

    for line in def_lines:
        if len(line) != lines_len:
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
        permuts = itertools.permutations(iterable, permut_length)

    elif permut_length == 1:
        for elem in iterable:
            permuts.append([elem])

    return permuts


def build_lines_permuts(sequence, num_lines):
    """
    Build lines permutations
    """

    all_lines_permuts = []

    if num_lines < 1:
        return all_lines_permuts

    print()

    lines_indexes = list(range(num_lines))

    while lines_indexes[0] < (len(sequence) - num_lines + 1):
        lines = []
        lines_values = set()

        for i_line in range(num_lines):
            i = lines_indexes[i_line]

            one_line = sequence[i]
            line_is_valid = True

            for value in one_line:
                if value in lines_values:
                    line_is_valid = False
                    break

                lines_values.add(value)

            if not line_is_valid:
                break

            lines.append(one_line)

        if len(lines) == num_lines:
            lines_permuts = list(build_permutations(
                lines, permut_length=len(lines)
                ))

            all_lines_permuts.extend(lines_permuts)

            for permut in lines_permuts:
                print("  ", permut, end="\r")

        lines_indexes_incremented = (num_lines - 1) * [False]

        i_line = num_lines - 1
        lines_indexes[i_line] += 1

        for i_line in reversed(range(1, num_lines)):
            if (
                lines_indexes[i_line]
                == len(sequence) - num_lines + i_line + 1
            ):
                lines_indexes[i_line - 1] += 1
                lines_indexes_incremented[i_line - 1] = True

        for i_line in range(num_lines - 1):
            if lines_indexes_incremented[i_line]:
                lines_indexes[i_line + 1] = lines_indexes[i_line] + 1

    print()
    print()

    return all_lines_permuts


def group_sequences(
        sequences, sequence_index
        ):
    """
    Group sequences
    """

    groups = []

    if sequence_index == 0:
        group = []

        for sequence in sequences[sequence_index]:
            new_group = group.copy()

            new_group.append(sequence)

            groups.append(new_group)

    else:
        last_groups = group_sequences(sequences, sequence_index - 1)

        for sequence in sequences[sequence_index]:
            for group in last_groups:
                new_group = group.copy()

                new_group.append(sequence)

                groups.append(new_group)

    return groups


def build_def_lines_vals_permuts(
        def_lines, num_def_lines
        ):
    """
    Build defined lines values permutations
    """

    lines_permuts = []
    for line in def_lines:
        permut_length = len(line)

        line_permuts = build_permutations(line, permut_length)

        lines_permuts.append(line_permuts)

    permuts_groups = group_sequences(
        sequences=lines_permuts, sequence_index=num_def_lines - 1
        )

    return permuts_groups


def diagonal_1_sum_is_valid(values, lines_len, lines_sum):
    """
    Check sum of diagonal 1
    """

    num_rows = lines_len
    num_columns = lines_len

    diagonal_sum = 0
    i_value = 0

    for row in range(num_rows):
        diagonal_sum += values[i_value]

        i_value += num_columns + 1

    if diagonal_sum == lines_sum:
        return True

    return False


def diagonal_2_sum_is_valid(values, lines_len, lines_sum):
    """
    Check sum of diagonal 2
    """

    num_rows = lines_len
    num_columns = lines_len

    diagonal_sum = 0
    i_value = num_columns - 1

    for row in range(num_rows):
        diagonal_sum += values[i_value]

        i_value += num_columns - 1

    if diagonal_sum == lines_sum:
        return True

    return False


def diagonals_sums_are_valid(values, lines_len, lines_sum):
    """
    Check sums of diagonals
    """

    if not diagonal_1_sum_is_valid(values, lines_len, lines_sum):
        return False

    return diagonal_2_sum_is_valid(values, lines_len, lines_sum)


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


def print_solutions(solutions, lines_len, max_value):
    """
    Print solutions
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
