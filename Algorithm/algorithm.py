def count_correct_numbers(start, end, groups_of_identical_adjacent_digits):
    """Function responsible for counting numbers for a given criteria
        1. Number must have x groups with identical adjacent digits
        2. Going from left to right, the digits never decrease; they only ever increase or stay the same
        3. It is a number in the given range (both ends inclusive).

    Args:
        start ([int]): start for range
        end ([int]): end for range
        groups_of_identical_adjacent_digits ([int]): Number of groups with identical adjacent digits

    Returns:
        [int]: Returns number of digits which accomplish criteria
    """

    # how many times numbers meets the criteria
    count = 0

    for number in range(start, end + 1):
        # creates list with single numbers
        list_of_int = list(map(int, str(number)))

        # checks if last number is greater then first, at least by: self.check_for_adjacent - 1
        # this will ensure that there is at least that many unique numbers
        if list_of_int[-1] - list_of_int[0] >= groups_of_identical_adjacent_digits - 1:

            # checks if digits decrease
            if is_it_bigger(list_of_int):

                # removes duplicates from list
                set_with_unique_numbers = set(list_of_int)

                # checks if there is adjacent duplicates in list
                adjacent_list = list(
                    map(
                        lambda x: check_for_adjacent(x, list_of_int),
                        set_with_unique_numbers,
                    )
                )

                # checks if there are at least x groups_of_identical_adjacent_digits
                if adjacent_list.count(True) >= groups_of_identical_adjacent_digits:
                    count += 1
    return count


def is_it_bigger(list_with_numbers):
    """
    Checks if number in list are greater or equal to next one
        :param list_with_numbers - List with integers
    """
    for index in range(len(list_with_numbers) - 1):
        if list_with_numbers[index] > list_with_numbers[index + 1]:
            return False
    return True


def check_for_adjacent(element_to_find, list_to_check):
    """
    Checks if given element have adjacent duplicate in list
        :param element_to_find - element to find
        :param list_to_check - list to perform action
    """
    for index in range(len(list_to_check) - 1):
        if list_to_check[index] == list_to_check[index + 1] == element_to_find:
            return True
    return False
