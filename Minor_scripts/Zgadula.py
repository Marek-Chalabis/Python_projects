# pop-quiz in python
import random
import string

list_of_words = ("mama", "tata", "europejczyk", 'zamek', 'motorniczy', 'Lublin')
answer = (random.choice(list_of_words)).lower()
attempts = 5

print(f"Welcome in the game 'Zgadula', your task is to find out a word that im thinking about "
      f"\nFor your convenience  i will give you one hint:"
      f"\nlength of the word is: {len(answer)} letters")

print(f"Lets start"
      f"\n-Give me {attempts} letters and finds out if any off them is in the word"
      f"\n-After that you have one try to guess my word")

letter = ""
correct_letters = ''
guess = ""

while attempts != 0:
    attempts -= 1
    guess = input("Choose your letter:\t").lower()
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        print(f"Are you trying to cheat?! You just lost one attempt")
    elif guess in answer:
        print(f"Yes!, the letter '{guess}' is in my word")
        if guess not in correct_letters:
            correct_letters += guess
    elif guess not in answer:
        print(f"No!, the letter '{guess}' is not in my word")
    elif attempts == 1:
        print('You have last letter, choose wisely')

print("\nYou used all of your attempts")
print("This is a letters in my word you find out:", correct_letters)
word = input("So what is my word?\n").lower()
if word == answer:
    print("You Won")
else:
    print("You Lost")

