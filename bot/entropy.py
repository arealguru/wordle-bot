from typing import List
from collections import Counter
from scipy.stats import entropy
from words import DICTIONARY


def word_entropy(words: List[str]):
    """
    Calculate the entropy of a set of words of the same length. Calculates
    the entropy over each letter position in the word, then adds them together.
    """
    word_length = len(words[0])
    num_words = len(words)

    # An empty array for each letter in the words
    letters_by_index = [[] for _ in range(word_length)]

    # Add letters to each array, word by word
    for word in words:
        for i in range(word_length):
            letters_by_index[i].append(word[i])

    # Calculate the total entropy over each letter, and sum them together
    return sum(
        [
            entropy(
                [count / num_words for count in Counter(index_letters).values()],
                base=2,
            )
            for index_letters in letters_by_index
        ]
    )
