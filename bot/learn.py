from entropy import all_entropies
from game import Game
from words import DICTIONARY
from random import sample
import csv
from multiprocessing import Pool
import pandas as pd


def avg(values):
    return sum(values) / len(values)


def simulate(potential_guess, feasible_solution, g):
    return all_entropies(g.peek(potential_guess, feasible_solution))


def learn(starting_from, until):
    g = Game()

    f = open(
        f"data/opening_word/standardized_entropy/entropy_data_{starting_from}_{until}.csv",
        "w",
    )
    writer = csv.writer(f)

    potential_guesses = DICTIONARY[starting_from:until]

    for ind, potential_guess in enumerate(potential_guesses):
        feasible_solutions = g.feasible_solutions
        if len(feasible_solutions) > 1000:
            feasible_solutions = sample(feasible_solutions, 1000)

        entropies = []
        for feasible_solution in feasible_solutions:
            entropies.append(
                simulate(
                    potential_guess,
                    feasible_solution,
                    g,
                )
            )

        writer.writerow(
            [potential_guesses[ind], *pd.DataFrame(entropies).mean().tolist()]
        )
        print(
            f"Moving onto next potential guess. Completed {ind} / {len(potential_guesses)}"
        )

    f.close()


if __name__ == "__main__":
    pagination_start = 0
    page_length = 200
    num_pages = 65
    num_threads = 10

    pages = [
        (
            pagination_start + page_num * page_length,
            pagination_start + (page_num + 1) * page_length,
        )
        for page_num in range(num_pages)
    ]

    with Pool(num_threads) as p:
        p.starmap(learn, pages)
