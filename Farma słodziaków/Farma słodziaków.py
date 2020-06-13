import random


class Animal(object):
    # Class that creates "słodziaka"

    def __init__(self, name, mood=random.randrange(0, 10)):
        print("Ooooo:)\nNew słodziaczek just born and you just name him/her: \n", name)
        hunger = random.randrange(0, 10)
        self.name = name
        self.hunger = hunger
        self.mood = mood

    def __str__(self):
        info = "Name: " + self.name + "\n"
        info += "mood: " + self.check_mood() + "\n"
        info += "hunger: " + self.check_hunger()
        return info

    def check_mood(self):
        mood = self.mood
        if 3 > mood:
            mood = "Sad :("
        elif 3 <= mood < 7:
            mood = "Happy :)"
        else:
            mood = f"{self.name} loves you :*"
        return mood

    def check_hunger(self):
        hunger = self.hunger
        if 3 > hunger:
            hunger = "Hungry!!"
        elif 3 <= hunger < 7:
            hunger = "Full"
        elif 7 <= hunger:
            hunger = "One more serniczek!!"
        return hunger

    def change_name(self, new_name):
        # change name of the słodziaczek
        self.name = new_name

    def eat(self, dinner):
        # feed słodziak
        if dinner >= 0:
            dinner += 1
        self.hunger += dinner

    def play(self, play):
        # play with słodziak
        if play >= 0:
            play += 1
        self.mood += play


def input_number(message, range):
    while True:
        try:
            user_input = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            if user_input < range:
                return user_input
                break


def main():
    print("Welcome to the farma słodziaków :)")
    list_of_animals = []
    choice = None
    while choice != 0:
        print('What you want to do?'
              '\n1-Add new słodziak'
              '\n2-Check hunger and mood of yours słodziaków'
              '\n3-Kill one of yours słodziak :o'
              '\n4-Change słodziak name'
              '\n5-Feed słodziaki'
              '\n6-Play with yours słodziaki')
        choice = input()

        if choice == "1":
            print("What do you want to call a new słodziak?")
            name = input("Give name\n")
            name = Animal(name)
            list_of_animals.append(name)

            for i in list_of_animals:
                i.eat(-1)
                i.play(-1)

        elif choice == "2":
            for i in list_of_animals:
                print(i)
                i.eat(-1)
                i.play(-1)

        elif choice == "3":
            if len(list_of_animals) == 0:
                print('What?! There is no more słodziak in your farma o.O')
            else:
                print("Here is the list of yours słodziak to butcher O.O")

                y = 0
                for i in list_of_animals:
                    print(y, ' - ', i.name)
                    y += 1

                nick = input_number("Choose one to massacre\n", len(list_of_animals))

                print(f"Rest of yours słodziak just eat {list_of_animals[nick].name}, nom nom nom :)")
                list_of_animals.pop(nick)

                for i in list_of_animals:
                    i.eat(5)
                    i.play(-2)

        elif choice == "4":
            if len(list_of_animals) == 0:
                print('What?! There is no more słodziak in your farma o.O')
            else:
                print("Here is the list of yours słodziak to change name?")
                y = 0
                for i in list_of_animals:
                    print(y, "-", i.name)
                    i.eat(-1)
                    i.play(-1)
                    y += 1

                nick = input_number("Choose one...\n", len(list_of_animals))

                new_name = input("New name...")
                print(list_of_animals[nick].name, "is now called:", end=" ")
                list_of_animals[nick].change_name(new_name)
                print(list_of_animals[nick].name)

        elif choice == "5":
            if len(list_of_animals) == 0:
                print('What?! There is no more słodziak in your farma o.O')
            else:
                print("Choose meal: "
                      "\n0 - fodder"
                      "\n1 - bread"
                      "\n2 - szarlotka")

                dinner = input_number('select meal', 3)
                for i in list_of_animals:
                    i.eat(dinner)
                    i.play(-2)

        elif choice == "6":
            if len(list_of_animals) == 0:
                print('What?! There is no more słodziak in your farma o.O')
            else:
                print("Choose play: "
                      "\n0 - Bowling"
                      "\n1 - Running"
                      "\n2 - Torture :P")

                play = input_number('select play', 3)

                for i in list_of_animals:
                    i.eat(-1)
                    i.play(play)


main()
