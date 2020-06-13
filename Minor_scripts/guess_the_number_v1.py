# Computer chooses random number, player tries to guess the number, program informs user if the chosen number is
# greater or smaller
import random  


def instruction():
    print("\tWelcome in the game 'Guess number'!")
    print("\nI will choose number between range that you provide")


def ask_number(number):
    guess = int(input("Guess the number: "))
    tries = 1
    while True:        
        if guess > number:
            print("Too large...")
        elif guess < number:
            print("Too small...")
        elif guess == number:
            print(f'Congratulations you guess the number and you needed {tries} tries for that')
            break
        guess = int(input("Ta liczba to: "))
        tries += 1


def how_hard():
    print("Decide of the difficulty level"
          "\nSpecify range")
    low = int(input("From...."))
    hight = int(input("To...."))
    number = random.randint(low, hight)
    return number


def main():
    instruction()
    ask_number(how_hard())


main()
