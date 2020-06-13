# Program will complete the text with user-provided phrases, an current date

import os

import datetime
print('Witaj w historii o kocie\nUzupełnij poniższe odpowiedzi aby otrzymąć historie o kocie')
imie = input('Jak ma imię kot?\n')
futro = input('Jakie ma futro?\n')
przymiotnik = input('Jaki jest kot?\n')
miejsce = input('Gdzie jest kot?\n')
time = datetime.datetime.now().strftime("%H:%M:%S")
story = 'PRZYMIOTNIK kot o imieniu: IMIE, mający FUTRO futro przechadzał się o GODZINA w oklichach MIEJSCE, gdy.... '
indywidual_story = story\
    .replace('PRZYMIOTNIK', przymiotnik)\
    .replace('IMIE', imie)\
    .replace('FUTRO', futro)\
    .replace('GODZINA', time)\
    .replace('MIEJSCE', miejsce)
print(indywidual_story)
with open('{}.txt'.format(imie), 'w') as file:
    file.write(indywidual_story)
input('Twoja historia o kocie została zapisana w:\n{}\nNaciśnij dowolny przycisk aby zakończyć'
      .format(os.path.dirname(os.path.realpath('{}.txt'.format(imie)))))




