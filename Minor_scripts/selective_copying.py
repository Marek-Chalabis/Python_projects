# Program copy a specific kind of documents to specific path
import os
import shutil
#  ---------change directory of search
path = r'C:\Users\Piotr Woźniak\Desktop\python'
# ----------choose path to place files
path_to_save = path + r'\notatki\poczatkujacy'
# ----------choose what kind of documents are you looking for
ends = '.docx'
try:
    os.makedirs(path_to_save)
except:
    print('Directory exists')

list_of_files = []
print(os.path.abspath('DB_filler.py'))

for r, d, f in os.walk(path + r'\Udemy-poczatek'):
    for files in f:
        if files.endswith(ends):
            list_of_files.append(os.path.join(r, files))

for file in list_of_files:
    try:
        shutil.copy(file, path_to_save)
    except:
        print('File {}\nExists in directory {}'.format(file, path_to_save))
