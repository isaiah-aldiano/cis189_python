import unittest
from NumberGuesser import NumberGuesser as n

class NumberGuesserTests(unittest.TestCase):

    def setUp(self):
        self.numGuess = n()

    def tearDown(self):
        del self.numGuess

    def test_add_to_guess_list(self):
        self.numGuess.add_guess(1)
        self.numGuess.add_guess(2)
        self.numGuess.add_guess(3)
        self.numGuess.add_guess(4)

        guesses = self.numGuess.return_guesses()
        expected = [1, 2, 3, 4]

        self.assertEqual(guesses, expected)

if __name__ == '__main__':
    unittest.main()