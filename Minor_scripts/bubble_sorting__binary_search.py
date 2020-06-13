import random


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
    return None


list_to_sort = random.sample(list(x for x in range(100)), k=50)
print('List to bubble sort:\n', list_to_sort)

bubble_sorting(list_to_sort)
print('sorted list:\n', list_to_sort)

random_number = random.choice(list(x for x in range(100)))
print('Radnom number: {}'.format(random_number))

print(binary_search(list_to_sort, random_number))
