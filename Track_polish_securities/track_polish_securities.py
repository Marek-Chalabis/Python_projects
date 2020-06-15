import os
import requests
import csv

# csv file listing of the Polish stock exchange
url = 'https://stooq.pl/q/d/l/?s=wig&i=d'


def donwload_csv(url):
    try:
        response = requests.get(url)
        with open(os.path.join(os.getcwd(), "file.csv"), 'wb') as f:
            f.write(response.content)
        return "file.csv"
    except:
        print('Something is wrong with url, more details coming soon...')


class CsvFormat:
    # saves data
    list_of_data = []
    headers = []
    sort_list_of_diffrence = []

    def __init__(self, line):
        # fill object with data
        self.info = line
        CsvFormat.list_of_data.append(self)

    @classmethod
    def show_inf(cls):
        print(cls.list_of_data)
        for i in cls.list_of_data:
            print(i.info)

    @classmethod
    def show_headers(cls):
        i = 0
        for header in cls.headers:
            print(i, '-', header)
            i += 1

    @classmethod
    def transfer_data(cls, file_csv):
        # transform data from file and delete it
        with open(file_csv) as raw_csv:
            file = csv.reader(raw_csv)
            for i in next(file):
                cls.headers.append(i)
            for line in file:
                CsvFormat(line)
        os.remove("file.csv")

    @classmethod
    def add_difrence(cls):
        # calculate difference betweem closing and opening days and adds sorted list
        cls.headers.append('difference between days')
        x = 1
        for i in cls.list_of_data:
            if len(cls.headers) != len(i.info)+1:
                i.info.append(None)
            if x == 1:
                i.info.append(0)
                yesterday = float(i.info[4])
                x += 1
            math = round((1 - (float(i.info[4]) / yesterday)) * 100, 4)
            i.info.append(math)
            cls.sort_list_of_diffrence.append(math)
            yesterday = float(i.info[4])

        cls.bubble_sorting(cls.sort_list_of_diffrence)

    @classmethod
    def show_number_of_days(cls, operator, number):
        # shows the days when the difference between the closing day and the opening day was "> or <" then %
        if operator == '>':
            for i in range(len(cls.sort_list_of_diffrence)):
                if cls.sort_list_of_diffrence[i] > number:
                    print('There was {} days when % was {} then {}'.format(len(cls.sort_list_of_diffrence) - i, operator, number))
                    break
        elif operator == '<':
            for i in range(len(cls.sort_list_of_diffrence)):
                if cls.sort_list_of_diffrence[i] > number:
                    print('There was {} days when % was {} then {}'.format(i, operator, number))
                    break

        else:
            print('Check if yours arguments are correct')

    @classmethod
    def check_for_percent(cls, percent):
        number = CsvFormat.binary_search(cls.sort_list_of_diffrence, percent)
        if number is None:
            print('There wasn\'t this exactly % yet', percent)
            show_percent = input('Do you want to see available %?(write "%")')
            if show_percent == '%':
                print(cls.sort_list_of_diffrence)
        else:
            list_of_dates = []
            for a in cls.list_of_data:
                if a.info[6] == percent:
                    list_of_dates.append(a.info[0])
            print('There was this {}%, on {}'.format(percent, list_of_dates))

    @classmethod
    def best_days(cls):
        number = 5
        best = input(f'Do you wanna see {number} best days in history?(write "yes)')
        if best == 'yes':
            print('Best {} days were:'.format(number))
            temp_list = cls.sort_list_of_diffrence[-number-1: -1]
            for i in temp_list:
                for a in cls.list_of_data:
                    if a.info[6] == i:
                        print(a.info[0])

    @staticmethod
    def bubble_sorting(list):
        for y in range(len(list) - 1, 0, -1):
            for x in range(y):
                if list[x] > list[x + 1]:
                    temp = list[x + 1]
                    list[x + 1] = list[x]
                    list[x] = temp
        if len(list) == 0:
            return None
        elif len(list) == 1:
            return list[0]
        return list

    @staticmethod
    def binary_search(list, number_to_find):
        while len(list) > 1:
            slash = len(list) // 2
            if number_to_find > list[slash]:
                list = list[slash:]
            elif number_to_find < list[slash]:
                list = list[:slash]
            else:
                if list[slash] == number_to_find:
                    return list[slash]


file_too_work = donwload_csv(url)
CsvFormat.transfer_data(file_too_work)
CsvFormat.add_difrence()
# CsvFormat.show_headers()
while True:
    try:
        percent = float(input('Define % for data to show'))
    except ValueError:
        print("Not a number(write only numbers like 4.3845)")
    else:
        break
operator = input('Should data be > or < then your %')
CsvFormat.show_number_of_days(operator, percent)
CsvFormat.check_for_percent(percent)
CsvFormat.best_days()
