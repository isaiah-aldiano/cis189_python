import random


class NumberGuesser:

    def __init__(self):
        self.winning_number = random.randint(1, 10)
        self.clicked_numbers = []

    def check_guess(self, guess):
        self.add_guess(guess)
        if guess == self.winning_number:
            return "correct"
        elif guess < self.winning_number:
            return "low"
        else:
            return "high"

    def add_guess(self, num):
        self.clicked_numbers.append(num)

    def reset_winning_num(self):
        self.winning_number = random.randint(1, 10)

    def return_guesses(self):
        return self.clicked_numbers

