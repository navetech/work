import csv
import sys

# from numpy import det
import itertools
import numpy as np

import random



def load_data(directory):
    """
    Load data from CSV files into memory.
    """

    # Load data
    data_loaded = {}
    data_loaded["precision"] = 0.1
    data_loaded["inline_defined_values"] = set()

    try:
        with open(f"{directory}/precision.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_loaded["precision"] = float(row["precision"])
    except:
        pass

    try:
        with open(f"{directory}/inline-defined-values.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_loaded["inline_defined_values"].add(int(row["inline-defined-values"]))
    except:
        pass

    return data_loaded


def build_fixed_equations_coefficients():
    """
    Build coefficients for fixed equations
    """

    # equations_coefficients = {}
    equations_coefficients = []

    for horizontal_equation in range(4):
        coefficients = 16 * [0]
        square_row = horizontal_equation
        for square_column in range(4):
            cell = (square_row * 4) + square_column
            coefficients[cell] = 1

        # equations_coefficients[f"array_{horizontal_equation}"] = coefficients
        equations_coefficients.append(coefficients)
    
    for vertical_equation in range(4):
        coefficients = 16 * [0]
        square_column = vertical_equation
        for square_row in range(4):
            cell = (square_row * 4) + square_column
            coefficients[cell] = 1

        # equations_coefficients[f"array_{4 + vertical_equation}"] = coefficients
        equations_coefficients.append(coefficients)
    
    coefficients = 16 * [0]
    for square_row in range(4):
        square_column = square_row
        cell = (square_row * 4) + square_column
        coefficients[cell] = 1

    # equations_coefficients[f"array_8"] = coefficients
    equations_coefficients.append(coefficients)
    
    coefficients = 16 * [0]
    for square_row in range(4):
        square_column = 3 - square_row
        cell = (square_row * 4) + square_column
        coefficients[cell] = 1

    # equations_coefficients[f"array_9"] = coefficients
    equations_coefficients.append(coefficients)

    return equations_coefficients


def build_estimated_equations_coefficients(non_def_permutation, defined_line=None):
    """
    Build coefficients for estimated equations
    """

    # equations_coefficients = {}
    equations_coefficients = []

    for i in range(len(non_def_permutation)):
        coefficients = 16 * [0]

        square_row = i // 4
        square_column = i % 4
        
        if defined_line is not None:
            if defined_line < 4:
                if square_row == defined_line:
                    square_row = (square_row + 3) % 4

            elif defined_line < 8:
                if square_column == defined_line - 4:
                    square_column = (square_column + 3) % 4

            elif defined_line == 8:
                if i < 3:
                    square_row = 0
                    square_column = (square_column + 1) % 4
                else:
                    square_column = 3
                    square_row = i - 2

            elif defined_line == 9:
                if i < 3:
                    square_row = 0
                else:
                    square_column = 0
                    square_row = i - 2

        cell = (square_row * 4) + square_column
        coefficients[cell] = 1

        # equations_coefficients[f"array_{i}"] = coefficients
        equations_coefficients.append(coefficients)

    return equations_coefficients


def build_def_line_equations_coefficients(def_permutation, defined_line):
    """
    Build coefficients for defined line equations
    """

    # equations_coefficients = {}
    equations_coefficients = []

    for i in range(len(def_permutation)):
        if def_permutation[i] is not None:
            coefficients = 16 * [0]

            if defined_line < 4:
                square_row = (i // 4) + defined_line
                square_column = i % 4

            elif defined_line < 8:
                square_column = (i // 4) + defined_line - 4
                square_row = i % 4

            elif defined_line == 8:
                square_row = i
                square_column = i

            elif defined_line == 9:
                square_row = i
                square_column = 3 - i

            cell = (square_row * 4) + square_column

            coefficients[cell] = 1

            # equations_coefficients[f"array_{i}"] = coefficients
            equations_coefficients.append(coefficients)

    return equations_coefficients


def build_def_line_equations_constants(def_permutation):
    """
    Build constants for defined line equations
    """

    equations_constants = []

    for value in def_permutation:
        if value is not None:
            equations_constants.append(value)

    return equations_constants


def main():
    # Get command line arguments
    if len(sys.argv) > 2:
        sys.exit("Usage: python quadrado-magico.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else ""

    # Load data from files into memory
    print("Loading data...")
    loaded_data = load_data(directory)
    print("Data loaded.")

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
