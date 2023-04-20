import tkinter as tk
from NumberGuesser import NumberGuesser

class NumberGuessingGame:

    def __init__(self, title, root):
        self.title = title
        self.root = root
        self.NumberGuesser = NumberGuesser()

    def set_up_game(self):
        for i in range(1, 11):
            guess_button = tk.Button(self.root, text=str(i), width=5, height=2, command=lambda num=i: self.check_guess(num))
            if i >= 6:
                guess_button.grid(row=2, column=i-5, padx=5, pady=5)
            else:
                guess_button.grid(row=1, column=i, padx=5, pady=5)

        self.status_label = tk.Label(self.root, text="Good luck!")
        self.status_label.grid(row=3, columnspan=10, pady=5, padx=5)

    def check_guess(self, num):
        if num in self.NumberGuesser.clicked_numbers:
            self.status_label.config(text="You already guessed that number")
        else:
            result = self.NumberGuesser.check_guess(num)
            if result == 'correct':
                self.status_label.config(text='Correct!')
                self.set_restart()
            elif result == 'low':
                self.status_label.config(text='Guess was low')
            else:
                self.status_label.config(text='Guess was high')
        self.update_buttons(result)

    def update_buttons(self, result):
        for button in self.root.winfo_children():
            if isinstance(button, tk.Button) and str.isdigit(button['text']):
                if result == 'correct':
                    button.config(state='disabled')

                if int(button['text']) in self.NumberGuesser.clicked_numbers:
                    button.config(state="disabled")

    def set_restart(self):
        self.restart = tk.Button(self.root, text='Restart game', command=lambda : self.restart_game())
        self.restart.grid(row=4, columnspan=10, pady=5, padx=5)

    def restart_game(self):
        self.restart.grid_forget()
        self.NumberGuesser.clicked_numbers.clear()
        self.NumberGuesser.reset_winning_num()
        self.start_game()

    def start_game(self):
        self.root.title(self.title)
        self.set_up_game()
        self.root.mainloop()

if __name__ == "__main__":
    window = tk.Tk()
    game = NumberGuessingGame('Nunber Guessing Game', window)
    game.start_game()