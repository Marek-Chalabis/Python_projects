import algorithm
import pytest


@pytest.mark.parametrize(
    "list_with_numbers, result",
    [
        ([7, 8, 4, 5, 5], False),
        ([7, 8, 8, 8, 8], True),
        ([7, 8, 8, 8, 8, -1], False),
        ([1, 2, 4, -1, 5, 5], False),
    ],
)
def test_is_it_bigger(list_with_numbers, result):
    assert algorithm.is_it_bigger(list_with_numbers) == result


@pytest.mark.parametrize(
    "element_to_find, list_to_check, result",
    [
        (7, [7, 8, 4, 5, 5], False),
        (5, [7, 8, 4, 5, 5], True),
        (1, [7, 8, 4, 5, 5], False),
        ("a", ["v", "g", "a", "a", "a"], True),
        ("v", ["v", "g", "a", "a", "a"], False),
        ("q", ["v", "g", "a", "a", "a"], False),
    ],
)
def test_check_for_adjacent(element_to_find, list_to_check, result):
    assert algorithm.check_for_adjacent(element_to_find, list_to_check) == result


@pytest.mark.parametrize(
    "start, end, groups_of_identical_adjacent_digits, result",
    [
        (100000, 110000, 2, 0),
        (100000, 110009, 2, 0),
        (1000, 1122, 2, 1),
        (100000, 112233, 3, 1),
        (100, 120, 1, 9),
    ],
)
def test_count_correct_numbers(start, end, groups_of_identical_adjacent_digits, result):
    test_object = algorithm.count_correct_numbers(
        start, end, groups_of_identical_adjacent_digits
    )
    assert test_object == result
