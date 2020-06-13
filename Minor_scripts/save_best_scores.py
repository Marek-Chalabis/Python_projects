# program saves players and their 5 best scores, first you need to populate data
import shelve
import pickle


player = input("Add player...")
score = int(input("Add player score..."))
list_of_scores = shelve.open("scores.dat", "c")

try:    
    print(listOfScores[player])
    print("Welcome, old player: ", player)
except:
    print("Welcome, new player: ", player)
    listOfScores = shelve.open("scores.dat", "c")
    
    listOfScores[player] = []

a = listOfScores[player]

for x in a:
    if score == x:
        a.remove(x)
a.append(score)
a.sort()

if len(a) > 5:
    a.remove(a[0])
a.reverse()
listOfScores[player] = a

listOfScores.sync()

print(listOfScores[player])
listOfScores.close()
