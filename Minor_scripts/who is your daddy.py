# Find out whos your daddy

print("Thanks to this app you will find out whos your daddy and and grandfather :o")
familia = {"Kowalski": ("Jan", "Marek"),
           "Zabłoccy": ("Czesław", "Mosiwór", "Kamil"),
           "Krawczyk": ("Adam", "Jan", "Karol")}

while True:
    print('These are the families I have in the database')
    for key in familia:
        print(key)
    print("\nWhat you want to do?"
          "\n1-Add your last name"
          "\n2-Change names in your family"
          "\n3-Delete family from database"
          "\n4-Check family tree"
          "\n5-Find last_name thru name"
          "\n7-End")
    decision = int(input())

    if decision == 1:
        last_name = input("Your last name")
        child_name = input("Your child name")
        familia[last_name] = child_name
        decision_father = input("Do you want to add your father name? \nWrite 'father'")

        if decision_father == 'father':
            father_name = input("Father name")
            familia[last_name] = (child_name, father_name)
            decision_grandfather = int(input("Do you want to add your grandfather name? \nWrite 'grandfather'"))

            if decision_grandfather == 1:
                grandfather_name = input("Grandfather name")
                familia[last_name] = (child_name, father_name, grandfather_name)

        a = 0
        for i in familia[last_name]:
            a += 1
            if a == 1:
                print(f"Son: {i} {last_name}")
            if a == 2:
                print(f"Father: {i} {last_name}")
            if a == 3:
                print(f"Grandfather: {i} {last_name}")

    elif decision == 2:
        last_name = (input("Write family last_name you want to modify")).capitalize()

        if last_name in familia:
            decision_name = int(input("Whose name you want to change?\n1-son \n2-father \n3-grandfather"))
            change = familia.get(last_name)
            new_name = input("New name")
            change = list(change)
            change[decision_name] = new_name
            change = tuple(change)
            familia[last_name] = change

    elif decision == 3:
        last_name = (input("Write family last_name you want to delete")).capitalize()

        if last_name in familia:
            del familia[last_name]

    elif decision == 4:
        last_name = input("Write family last_name you want to see")
        a = 0
        for i in familia[last_name]:
            a += 1
            if a == 1:
                print(f"Son: {i} {last_name}")
            if a == 2:
                print(f"Father: {i} {last_name}")
            if a == 3:
                print(f"Grandfather: {i} {last_name}")

    elif decision == 5:
        name = input("Write name you are looking for")
        list_last = []
        for key in familia:
            for name_family in familia[key]:
                if name_family == name:
                    list_last.append(key)
                print(name_family)
        print(f"{name} appears with the {list_last}")

    elif decision == 6:
        break
