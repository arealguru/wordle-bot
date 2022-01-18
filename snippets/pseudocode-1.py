wordle = Wordle()

# Expected entropy for each potential move
expected_entropies = []

# Any word in the dictionary is a feasible move
for potential_move in wordle.dictionary:
    # For every feasible secret word, calculate the entropy if
    # potential_move were played. Compute the average over these entropies.
    expected_entropy = avg(
        [
            entropy(
                wordle.new_feasible_set(
                    secret_word=potential_secret_word, move=potential_move
                )
            )
            for potential_secret_word in wordle.feasible_words
        ]
    )
    expected_entropies.append(expected_entropy)

print(wordle.dictionary[which_min(move_entropies)])
