from typing import List
from collections import Counter
from scipy.stats import entropy


def individual_letter_entropies(words: List[str]):
    """
    Calculates the entropy over each letter position in the word, does not combine them.
    """
    word_length = len(words[0])
    num_words = len(words)

    # An empty array for each letter in the words
    letters_by_index = [[] for _ in range(word_length)]

    # Add letters to each array, word by word
    for word in words:
        for i in range(word_length):
            letters_by_index[i].append(word[i])

    # Calculate the total entropy over each letter
    return [
        entropy(
            [count / num_words for count in Counter(index_letters).values()],
            base=2,
        )
        for index_letters in letters_by_index
    ]


def bigram_entropies(words: List[str]):
    word_length = len(words[0])
    num_words = len(words)

    # An empty array for each bigram slot in the words
    bigrams_by_index = [[] for _ in range(word_length - 1)]

    # Add bigrams to each array, word by word
    for word in words:
        for i in range(word_length - 1):
            bigrams_by_index[i].append(word[i : i + 2])

    # Calculate the total entropy over each bigram
    return [
        entropy(
            [count / num_words for count in Counter(bigram_letters).values()],
            base=2,
        )
        for bigram_letters in bigrams_by_index
    ]


def all_entropies(words: List[str]):
    return [*individual_letter_entropies(words), *bigram_entropies(words)]


def word_entropy(words: List[str]):
    """
    Calculate the entropy of a set of words of the same length. Calculates
    the entropy over each letter position in the word, then adds them together.
    """
    sum(individual_letter_entropies(words))
