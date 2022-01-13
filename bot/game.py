from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set
from xmlrpc.client import Boolean
from words import DICTIONARY
from random import choice


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


@dataclass
class Constraint:
    present_at: List[int]
    not_present_at: List[int]
    bounds: List[int]
    char: str

    def is_met_by(self, word) -> Boolean:
        """
        True if and only if word meets constraint
        """
        for index in self.present_at:
            if word[index] != self.char:
                return False

        for index in self.not_present_at:
            if word[index] == self.char:
                return False

        times_present = word.count(self.char)

        if times_present > self.bounds[1] or times_present < self.bounds[0]:
            return False

        return True

    def __hash__(self):
        return hash(
            (
                tuple(self.present_at),
                tuple(self.not_present_at),
                tuple(self.bounds),
                self.char,
            )
        )


class Game:
    def __init__(self):
        self.solution = choice(DICTIONARY)
        self.feasible_solutions = DICTIONARY.copy()
        self.guesses_made = 0
        self.seen_constraints = defaultdict(lambda: set())

    def _construct_constraints(
        self, guess: str, solution: str
    ) -> Dict[str, Constraint]:
        """
        Construct a dictionary mapping from the letters guessed to a constraint for each letter.
        """
        constraints: Dict[str, Constraint] = keydefaultdict(
            lambda chr: Constraint([], [], [0, len(solution)], chr)
        )

        for ind in range(len(guess)):
            if guess[ind] == solution[ind]:
                constraints[guess[ind]].present_at.append(ind)
                continue

            if guess[ind] != solution[ind]:
                constraints[guess[ind]].not_present_at.append(ind)

        for guessed_letter in set(guess):
            times_guessed = guess.count(guessed_letter)
            times_solution = solution.count(guessed_letter)
            if times_guessed > times_solution:
                # If you guess too many times, then the lower and upper bound is the correct number.
                constraints[guessed_letter].bounds[0] = times_solution
                constraints[guessed_letter].bounds[1] = times_solution
            else:
                # Otherwise, you just know that there are at least how many you guessed.
                constraints[guessed_letter].bounds[0] = times_guessed

        return constraints

    def _compute_legal_words(self, constraint):
        for feasible_solution in self.feasible_solutions:
            if constraint.is_met_by(feasible_solution):
                self.seen_constraints[constraint].add(feasible_solution)

    def peek(self, guess: str, solution: str) -> List[str]:
        """
        Peek at what the feasible solutions would be if you were to play a word,
        given that the solution word is solution.
        """
        constraints = self._construct_constraints(guess, solution)

        for constraint in constraints.values():
            if constraint not in self.seen_constraints:
                self._compute_legal_words(constraint)

        new_feasible_solutions = self.seen_constraints[next(iter(constraints.values()))]
        for constraint in constraints.values():
            new_feasible_solutions = new_feasible_solutions.intersection(
                self.seen_constraints[constraint]
            )

        return list(new_feasible_solutions)

    def play(self, guess: str):
        """
        Makes a move, updating the feasible solutions, and tallying a guess.
        """
        self.feasible_solutions = self.peek(guess, self.solution)
        self.seen_constraints = {}
        self.guesses_made += 1
