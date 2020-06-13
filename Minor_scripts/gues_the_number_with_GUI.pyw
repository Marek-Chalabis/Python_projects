# guess the number with GUI

from tkinter import *
import random


class ShowGame(Frame):
    # creates frame
    def __init__(self, master):
        super(ShowGame, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.counter = 0
        self.number = random.randint(0, 20)

    def create_widgets(self):
        # create label
        information = Label(self)
        information.grid(row=0, column=0, sticky=W)
        information["text"] = "Lets plat a game you have 5 chances"

        Label(self, text="Please give me number:").grid(row=1, column=0, columnspan=2, sticky=W)

        self.pole = Entry(self)
        self.pole.grid(row=2, column=0, sticky=W)

        self.buttonSubmit = Button(self, text="Submit number", command=self.two_fuction).grid(row=3, column=0, sticky=W)

        self.textInfo = Text(self, width=40, height=2, wrap=WORD)
        self.textInfo.grid(row=4, column=0, sticky=W)

        self.buttonSubmit = Button(self, text="Restart the game", command=self.game_reset)\
            .grid(row=5, column=0, sticky=W)

    def check_number(self):
        guess = self.pole.get()
        print(self.counter)
        guess = int(guess)
        print(self.number, "is the number")
        if self.counter > 3:
            info = "You used all of your chances"
        else:
            if self.number < guess:
                info = "Smaller!"
            elif self.number > guess:
                info = "Higher!"
            else:
                info = "Correct, the number is: "+str(self.number) + "\nGame was automatically restarted"
                self.game_reset()

        self.textInfo.delete(0.0, END)
        self.textInfo.insert(0.0, info)

    def check_counter(self):
        self.counter += 1
        
    def two_fuction(self):
        self.check_number()
        self.check_counter()

    def game_reset(self):
        self.number = random.randint(0,20)
        self.counter = 0


root = Tk()
root.title("Guess the number?")
root.geometry("350x150")
show = ShowGame(root)
root.mainloop()
