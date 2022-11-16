import csv


# from numpy import det
import itertools


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
    except Exception:
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
            with open(
              f"{directory}/defined-line-{i}.csv", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    line_values.append(int(row["value"]))
        except Exception:
            pass

        if len(line_values) > 0:
            def_lines.append(line_values)

    return def_lines


def line_length_is_valid(line_length, line_sum):
    """
    Check if line legth is valid
    """

    return (line_length % 2) == (line_sum) % 2


def def_lines_are_valid(
        def_lines, line_length, num_lines, max_value, line_sum
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
