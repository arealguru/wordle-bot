# Wordle Bot (Python)

The goal of this repository was to create a program that could play [Wordle](https://www.powerlanguage.co.uk/wordle/), better than I can.

I'm cannot claim that I am amazing at the game, but I certainly can assert that the bot beat me almost every time.

If you want to learn more about the philosophy of the bot, and a higher level of how it works, I wrote a Medium article that you can find here: [TODO].

## What is Included

### Dependency Management

This project uses Pipenv to manage dependencies. If you have Pipenv installed, you should be able to run `pipenv install` within the project directory and all of the project dependencies should install if you have the right version of Python on your system (3.8).

You can activate the shell of this pipenv then, by running `pipenv shell`.

### Data Analysis

Since there are so many different ways to play the opening word, I had to run code to learn the best opening move offline (overnight). To explore the data I collected, you can look in `data/opening_word/entropies`, and you will see sharded csv files. The schema of these files is:
- Column 1: The word to "guess"
- Column 2: The expected entropy of the first letter if that word is played,
- ...
- Column 6: The expected entropy of the fifth letter if that word were to be played.
- Column 7: The expected entropy of the first two letters if that word were to be played.
- ...
- Column 10: The expected entropy of the last two letters if that word were to be played.

You can run a script that calculates the standardized entropies, derives a single expected entropy value, and sorts by this value, given this data, by running `python3 analysis/opening_word.py`.

You can also explore how the bot played some of the words by looking at the sample data in `data/gameplay`. Within each word directory, you will see a set of the moves that the player made, in addition to the actual reasoning each round.

### Playing against the Bot

If you want to play against the bot, you can run `python3 bot/player.py <word>`, where `<word>` is the secret word that you challenge the bot to guess. By default the bot will play the best opening word "tales", but if you want to change this, you can modify line 131 in the code with whatever opening word you wish.

To get an idea of good opening words, you should refer to the previous section of documentation and run `python3 analysis opening_word.py`.

## Demo

```
$ python3 bot/player.py shire
I'm playing tales
The answer could now be one of 228

I'm playing seine
The answer could now be one of 10

I'm playing spark
The answer could now be one of 2

I'm playing shire
Ha! I won!
```

```
Wordle 212 4/6

⬛⬛⬛🟨🟨
🟩⬛🟩⬛🟩
🟩⬛⬛🟩⬛
🟩🟩🟩🟩🟩
```