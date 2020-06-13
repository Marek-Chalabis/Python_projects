import shelve


def results_of_the_game():
    # function keeps 5 best scores for each player
    print("Welcome to the tournament of knowledge"
          "\nGive me your name player!")
    player = input("Nick...")
    list_of_scores = shelve.open("scores.dat", "c")

    try:
        print(list_of_scores[player])
        print("\nWelcome, old player: ", player)
    except:
        print("\nWelcome, new player: ", player)
        list_of_scores = shelve.open("scores.dat", "c")
        list_of_scores[player] = []

    score = main()
    a = list_of_scores[player]

    for x in a:
        if score == x:
            a.remove(x)

    a.append(score)
    a.sort()

    if len(a) > 5:
        a.remove(a[0])

    a.reverse()
    list_of_scores[player] = a
    list_of_scores.sync()
    list_of_scores.close()
    return a


def generate_question(list_of_questions):
    # Generates questions from txt file
    category = list_of_questions.readline()
    question = list_of_questions.readline().replace("/", "\n")
    answer = []

    for i in range(4):
        answer.append(list_of_questions.readline().replace("/", "\n"))

    correct = list_of_questions.readline().replace("\n", "")
    correct = int(correct)
    points = list_of_questions.readline().replace("\n", "")
    points = int(points)
    explanation = list_of_questions.readline().replace("/", "\n")
    return category, question, answer, correct, explanation, points


def main():
    # Logic behind the game
    list_of_questions = open("quiz.txt", "r")
    title = list_of_questions.readline()
    print("Today episode:\n\n\t\t", title)
    score = 0
    category, question, answer, correct, explanation, points = generate_question(list_of_questions)
    try:
        while question:
            print("\n\n", category)
            print(question)

            for i in range(4):
                print(i + 1, "-", answer[i])
            player_choice = int(input("Choose answer\n"))

            if player_choice == correct:
                score += points
                print("Correct")
            else:
                print("Wrong")

            print("Explanation: ", explanation)
            category, question, answer, correct, explanation, points = generate_question(list_of_questions)
    except:
        print('Thats all the questions')

    print("Score of the game: ", score)
    return score


def show_results(a):
    # Display scores
    list_of_scores = shelve.open("scores.dat", "c")
    print("Here is the list of the best scores:")

    for i in a:
        print(i)

    print("\nDo you want to see other players results?")
    choice = input("Write player nick")

    a = list_of_scores[choice]
    print("Scores ", choice, ":")
    for i in a:
        print(i)

    list_of_scores.close()


show_results(results_of_the_game())
