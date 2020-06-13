# program checks if your password is strong
import re

def CheckPassword(password):
    '''Method - checks if the password is strong, if not telling what is mising'''
    print('Hasło: \n', end='')
    if len(password) < 8:
        print('ma mniej niż 8 znaków')
    if not re.compile(r'[a-z]').findall(PASSWORD):
        print('nie ma małych liter')
    if not re.compile(r'[A-Z]').findall(PASSWORD):
        print('nie ma dużych liter')
    if not re.compile(r'[0-9]').findall(PASSWORD):
        print('nie ma cyfr')
    if not re.compile(r'(?=.*?[^A-Za-z\s0-9])').findall(PASSWORD):
        print('nie ma znaku specjalnego')
    if re.compile(
               r'(?=.*?[0-9])' # checks if there is a number
               r'(?=.*?[a-z])' # checks if there is a lowcase letter
               r'(?=.*?[A-Z])' # checks if there is a uppercase letter
               r'(?=\S{6,25}$)' # checks if length of password is at least 8 characters
               r'(?=.*?[^A-Za-z\s0-9])' # checks if there is a special character
               ).findall(PASSWORD):
        print('POPRAWNE')


print('''
Sprawdź czy twoje hasło jeset silne\nDobre hasło powinno mieć:\nmin 8 znaków\nposiadać przynajmniej 1:\n\t*małą literę\n\t*dużą literę\n\t*znak specjalny''')
PASSWORD = input('Wprowadź hasło\n')
CheckPassword(PASSWORD)
input('Naciśnij enter by zakończyć')