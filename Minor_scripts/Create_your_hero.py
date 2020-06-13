import random

points = random.randint(15, 40)
limits = int(points * 0.6)
character = {
    'DEX': 1,
    'STR': 1,
    'HP': 1,
    'WI': 1,
    'total': 1,
}
print("Welcome you have: ", points, "points to crate your own character")
print("How do you want to spent your points?"
      "\nDEX-dexterity"
      "\nSTR-strength"
      "\nHP-Health"
      "\nWI-Wisdom")

while character['total'] != points:
    statistic_choice = (input("Podaj statystyke")).upper()
    while statistic_choice not in character.keys():
        statistic_choice = (input("Podaj statystyke")).upper()
    stat = int(character[statistic_choice])

    math = (input('You want to add or subtract?')).lower()
    while math not in ('add', 'subtract'):
        math = (input('You want to add or subtract?')).lower()

    value = int(input("How much?"))

    if math == 'add':

        if character[statistic_choice] + value > limits:
            print(f"You are trying to {math} points to {statistic_choice} over your points limit"
                  f"({limits})")
        else:
            character[statistic_choice] = stat + value
            character['total'] = character['total'] + value

    elif math == 'subtract':
        if stat - value < 0:
            print(f"You cant {math} under 0")
        else:
            character[statistic_choice] = stat - value
            character['total'] = character['total'] - value

    print(f'Left points = {points - character["total"]}'
          f'\nCurrent STATISTICS:'
          f'\nDEX-{character["DEX"]}'
          f'\nSTR-{character["STR"]}'
          f'\nHP-{character["HP"]}'
          f'\nWI-{character["WI"]}')

print(f'Here is your hero!:'
      f'\nDEX-{character["DEX"]}'
      f'\nSTR-{character["STR"]}'
      f'\nHP-{character["HP"]}'
      f'\nWI-{character["WI"]}')
