from multiprocessing import Pool
import sys
from game import Game
from words import DICTIONARY
from entropy import all_entropies
from random import sample
import pandas as pd
from alive_progress import alive_bar
from os import mkdir


def avg(values):
    return sum(values) / len(values)


def simulate(potential_guess, feasible_solution, g):
    return all_entropies(g.peek(potential_guess, feasible_solution))


def analyze_guess(feasible_solutions, potential_guess):
    game = Game()
    game.feasible_solutions = feasible_solutions

    is_feasible = int(potential_guess in feasible_solutions)

    if len(feasible_solutions) > 1000:
        feasible_solutions = sample(feasible_solutions, 1000)

    entropies = [
        simulate(potential_guess, feasible_solution, game)
        for feasible_solution in feasible_solutions
    ]
    expected_entropy = pd.DataFrame(entropies).mean().tolist()[0:5]
    return [potential_guess, *expected_entropy, is_feasible]


def call_analyze_guess(job_params):
    return analyze_guess(*job_params)


def normalize_df_entropies(df):
    words = df["Word"]
    feasibility = df["IsFeasible"]
    df = df.drop(columns=["Word", "IsFeasible"])

    std = df.std().replace(0, 1)
    df = (df - df.mean()) / std
    df.insert(0, "Word", words)
    df["IsFeasible"] = feasibility

    return df


def calculate_best_moves(feasible_solutions, potential_guesses) -> pd.DataFrame:
    with alive_bar(len(potential_guesses)) as bar:
        guess_jobs = []
        for potential_guess in potential_guesses:
            guess_jobs.append((feasible_solutions, potential_guess))

        results = []
        with Pool() as pool:
            for result in pool.imap(call_analyze_guess, guess_jobs):
                results.append(result)
                bar()

    df = pd.DataFrame(
        results,
        columns=[
            "Word",
            "Letter1",
            "Letter2",
            "Letter3",
            "Letter4",
            "Letter5",
            "IsFeasible",
        ],
    )

    df = normalize_df_entropies(df)

    # Sort by ExpectedEntropy, tie break with feasible solutions.
    df["ExpectedEntropy"] = (
        df["Letter1"] + df["Letter2"] + df["Letter3"] + df["Letter4"] + df["Letter5"]
    )
    df = df.sort_values(by=["ExpectedEntropy", "IsFeasible"], ascending=[True, False])

    return df


def save_moves(best_moves, next_move, solution, round_num):
    if round_num == 0:
        mkdir(f"data/gameplay/{solution}")

    # Mark next move
    with open(f"data/gameplay/{solution}/moves.txt", "a+") as f:
        f.write(next_move + "\n")

    # Save move reasoning
    if round_num > 0:
        best_moves.to_csv(f"data/gameplay/{solution}/round_{round_num}_entropy.csv")
        best_moves = best_moves.sort_values(
            by=["IsFeasible", "ExpectedEntropy"], ascending=[False, True]
        )
        best_moves.to_csv(f"data/gameplay/{solution}/round_{round_num}_feasibility.csv")


def play(word, opening_move):
    g = Game(word)
    potential_guesses = DICTIONARY

    print(f"The answer is {g.solution}")

    # For the six rounds
    for round_num in range(0, 6):
        print(f"The answer could be one of {len(g.feasible_solutions)}")
        next_move = None
        best_moves = None
        if round_num == 0:
            next_move = opening_move
        else:
            best_moves = calculate_best_moves(g.feasible_solutions, potential_guesses)
            next_move = best_moves.iloc[0][0]
        print(f"I'm playing {next_move}")
        save_moves(best_moves, next_move, word, round_num)
        if g.play(next_move):
            print("Ha! I won!")
            return


if __name__ == "__main__":
    play(sys.argv[1], "tales")
