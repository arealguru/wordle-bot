from game import Game
from words import DICTIONARY
from entropy import word_entropy
from random import sample
import csv
from multiprocessing import Pool


def which_min(values):
    return min(range(len(values)), key=values.__getitem__)


def avg(values):
    return sum(values) / len(values)


def simulate(potential_guess, feasible_solution):
    return word_entropy(g.peek(potential_guess, feasible_solution))


def turn(starting_from, until):
    g = Game()

    f = open(f"data/entropy_data_{starting_from}_{until}.csv", "w")
    writer = csv.writer(f)

    potential_guesses = DICTIONARY[starting_from:until]
    expected_entropies = []
    original_entropy = word_entropy(g.feasible_solutions)
    print(f"The original entropy was {original_entropy}")

    for ind, potential_guess in enumerate(potential_guesses):
        feasible_solutions = g.feasible_solutions
        if len(feasible_solutions) > 1000:
            feasible_solutions = sample(feasible_solutions, 1000)

        expected_entropies.append(
            avg(
                [
                    simulate(
                        potential_guess,
                        feasible_solution,
                    )
                    for feasible_solution in feasible_solutions
                ]
            )
        )
        writer.writerow([potential_guesses[ind], expected_entropies[ind]])
        print(
            f"Moving onto next potential guess. Completed {ind} / {len(potential_guesses)}"
        )

    f.close()


if __name__ == "__main__":
    pagination_start = 1800
    page_length = 200
    num_pages = 8

    pages = [
        (
            pagination_start + page_num * page_length,
            pagination_start + (page_num + 1) * page_length,
        )
        for page_num in range(num_pages)
    ]

    with Pool(num_pages) as p:
        p.starmap(turn, pages)
