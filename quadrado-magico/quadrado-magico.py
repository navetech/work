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


def build_fixed_equations_coefs(num_fixed_equations, num_values, line_length):
    """
    Build coefficients for fixed equations
    """

    equations_coefs = []

    for equation in range(num_fixed_equations):
        coefs = num_values * [0]
        row = equation
        for column in range(line_length):
            cell = (row * num_fixed_equations) + column
            coefs[cell] = 1

        equations_coefs.append(coefs)

    return equations_coefs


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


def build_def_lines_vals_permuts(def_lines, num_def_lines):
    """
    Build defined lines values permutations
    """

    permutations = []

    for line in def_lines:
        line_permuts = itertools.permutations(line)

        permutations.append(line_permuts)


    all_permuts = []
    i_permut = 0
    while True:
        end = True
        permuts = []

        for i in range(num_def_lines):
            count = 0

            for permut in permutations[i]:
                if count == i_permut:
                    permuts.append(permut)
                    end = False
                    break

                count += 1

        if end:
            break

        all_permuts.append(permuts)

        i_permut += 1


    return all_permuts


def build_def_lines_pos_ids(num_lines):
    """
    Build defined lines positions ids
    """

    ids = []

    id_rows = list(range(num_lines))
    id_columns = list(range(num_lines, 2 * num_lines))
    id_diagonal_1 = (2 * num_lines) + 1
    id_diagonal_2 = (2 * num_lines) + 2

    ids.extend(id_rows)
    ids.extend(id_columns)
    ids.append(id_diagonal_1)
    ids.append(id_diagonal_2)

    return ids


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
    fixed_equations_coefs = build_fixed_equations_coefs(num_fixed_equations, num_values, line_length)

    # Build constants for fixed equations
    fixed_equations_consts = num_fixed_equations * [line_sum]

    # Build all estimated values
    estim_vals = build_estim_vals(max_value, def_lines)

    # Build valid estimated values permutations
    valid_estim_vals_permuts = build_valid_estim_vals_permuts(
        estim_vals, num_estim_vals_equations, line_length, line_sum, max_value
        )

    # Build estimated values permutations for equations
    equations_estim_vals_permuts = itertools.permutations(valid_estim_vals_permuts, line_length)

    # Build defined lines values permutations
    def_lines_vals_permuts = build_def_lines_vals_permuts(def_lines, num_def_lines)

    for permuts in def_lines_vals_permuts:
        print(permuts)

    print(len(def_lines_vals_permuts))

    """
    for line_permuts in def_lines_vals_permuts:
        count = 0
        for permut in line_permuts:
            count += 1
            print(permut)
        print(count)
    """


    # Build defined lines positions ids
    def_lines_pos_ids = build_def_lines_pos_ids(num_lines)

    # Build defined lines positions permutations
    def_lines_pos_permuts = itertools.permutations(def_lines_pos_ids, num_def_lines)

    # If there are not any defined lines
    if num_def_lines < 1:

        # Build coefficients for estimated values equations

        # For each estimated values permutation for equations
        for permut in equations_estim_vals_permuts:
            break
            
            # Build constants for estimated values equations

            # Build coefficients for all equations

            # Build constants for all equations

            # Solve equations

    # Else there are defined lines
    else:

        # For each defined lines values permutations
        
            # For each defined lines positions permutation
                
                # Build coefficients for defined line equations  
                
                # Build constants for defined line equations

                # Build coefficients for estimated values equations
    
                # For each estimated values permutation for equations
                for permut in equations_estim_vals_permuts:
                    break
                    
                    # Build constants for estimated values equations

                    # If constants for estimated values equations are valid

                        # Build coefficients for all equations

                        # Build constants for all equations

                        # Solve equations

    

    



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
