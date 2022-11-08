import csv
import sys

import itertools
import numpy as np


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

    defined_row = None
    defined_column = None
    if defined_line:
        if defined_line < 4:
            defined_row = defined_line
        elif defined_line < 8:
            defined_column = defined_line - 4
        elif defined_line == 9:
            defined_row = 0
            defined_column = 0
        elif defined_line == 10:
            defined_row = 1
            defined_column = 3


    for i in range(len(non_def_permutation)):
        coefficients = 16 * [0]

        if defined_row and defined_column:
            if i < 2:
                square_row = 0
                square_column = (i + 1) % 2

        square_row = i / 4
        square_column = i % 4


        cell = (square_row * 4) + square_column
        coefficients[cell] = 1

        # equations_coefficients[f"array_{i}"] = coefficients
        equations_coefficients.append(coefficients)

    return equations_coefficients



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

    # IF there are not any inline defined values
    if len(inline_defined_values) < 1:

        # For each permutation of non-defined values
        for non_def_permutation in non_def_permutations:

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
            coefficients_matrix.append(fixed_equations_constants)
            coefficients_matrix.append(estimated_equations_constants)

            b = np.array(constants_matrix)

            x = np.linalg.solve((a, b))

            solutions.append(x)

        # Else
        else:

            # For each permutation of inline defined values
            for def_permutation in def_permutations:

                # for each line of the magic square
                for defined_line in range(10):

                    # Build equations for defined line
                    def_line_equations_coefficients = build_def_line_equations_coefficients(def_permutation, defined_line)
                    def_line_equations_constants = build_def_line_equations_coefficients(def_permutation)

                    # For each permutation of non-defined values
                    for non_def_permutation in non_def_perm

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
                        coefficients_matrix.append(fixed_equations_constants)
                        coefficients_matrix.append(def_line_equations_constants)
                        coefficients_matrix.append(estimated_equations_constants)

                        b = np.array(constants_matrix)

                        x = np.linalg.solve((a, b))

                        solutions.append(x)


if __name__ == "__main__":
    main()


"""
import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}
"""

def load_data2(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main2():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

"""
if __name__ == "__main__":
    main()

"""
