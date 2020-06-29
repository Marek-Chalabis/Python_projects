import todo
from unittest import mock
import pendulum


def return_hash(test_text, text_to_find):
    """return hashes from text"""
    test_list = test_text.split()
    # gets text with white spaces , etc...
    full_task_text = [elem for elem in test_list if text_to_find == elem][0]
    # gets index of given task text
    test_finds_task = test_list.index(full_task_text)
    # returns hash because its 2 elements later
    test_hash = test_list[test_finds_task + 2]
    return test_hash


def test_todo_application():
    """
    Fully automated tests for 3 task that takes place in past, 'today' and future.
    After tests they will be removed
    ! It's better to test it on Different DB go to todo_database and change DB_name
    """

    # different times to check
    today_to_operate = pendulum.today()
    today = today_to_operate.format("YYYY-MM-DD")
    text_for_today = "vsdfdsg453456TODAY978jhynyjku"
    name_for_today = "TEST TODAY"

    past = (today_to_operate.subtract(years=5)).format("YYYY-MM-DD")
    text_for_past = "65786785436569jkkPASTghsatgedhutyibnyiyun"
    name_for_past = "TEST PAST"

    future = today_to_operate.add(years=5).format("YYYY-MM-DD")
    text_for_future = "fdsgd45gFUTUREtry6yg7575"
    name_for_future = "TEST FUTURE"

    # tests add
    with mock.patch("sys.argv", [""] + ["add"]):
        test1 = todo.todo_action()
        assert test1 == "For this action(add) following flags are required: -n, -d, -t"

    # adds 3 tasks from past, today, future
    with mock.patch(
        "sys.argv", [""] + ["add", "-n", name_for_past, "-d", past, "-t", text_for_past]
    ):
        test_add = todo.todo_action()
        assert test_add == "Task created"

    with mock.patch(
        "sys.argv",
        [""] + ["add", "-n", name_for_today, "-d", today, "-t", text_for_today],
    ):
        test_add = todo.todo_action()
        assert test_add == "Task created"

    with mock.patch(
        "sys.argv",
        [""] + ["add", "-n", name_for_future, "-d", future, "-t", text_for_future],
    ):
        test_add = todo.todo_action()
        assert test_add == "Task created"

    # checks if list action with different flags return different tables
    with mock.patch("sys.argv", [""] + ["list"]):
        standard_table = todo.todo_action()

    with mock.patch("sys.argv", [""] + ["list", "-m"]):
        missed_table = todo.todo_action()

    with mock.patch("sys.argv", [""] + ["list", "-to"]):
        today_table = todo.todo_action()

    with mock.patch("sys.argv", [""] + ["list", "-c"]):
        current_table = todo.todo_action()
    assert (standard_table != missed_table != today_table != current_table) is True

    #  gets hashes for different tasks
    with mock.patch("sys.argv", [""] + ["list"]):
        text_with_hashes = todo.todo_action()
        past_hash = return_hash(text_with_hashes, text_for_past)
        today_hash = return_hash(text_with_hashes, text_for_today)
        future_hash = return_hash(text_with_hashes, text_for_future)
        assert (past_hash != today_hash != future_hash) is True

    # tests updates
    # new values to update
    new_today = (today_to_operate.add(days=32)).format("YYYY-MM-DD")
    new_text_for_today = "vsdfdsg453456TODAYNEW978jhynyjku"

    # without given flag
    with mock.patch(
        "sys.argv", [""] + ["update", "-d", new_today, "-t", new_text_for_today]
    ):
        test_add = todo.todo_action()
        assert test_add == "For this action(update) following flags are required: -th"

    # wrong hash
    with mock.patch(
        "sys.argv", [""] + ["update", "-d", new_today, "-th", "wrong hash"]
    ):
        test_add = todo.todo_action()
        assert test_add == "There is no task with this hash: wrong hash"

    # with  flags
    with mock.patch(
        "sys.argv",
        [""] + ["update", "-d", new_today, "-t", new_text_for_today, "-th", today_hash],
    ):
        test_add = todo.todo_action()
        assert test_add == "Task updated"

    # checks if data changed
    with mock.patch("sys.argv", [""] + ["list"]):
        text_for_list = todo.todo_action()
        text_list = text_for_list.split()
        for text in [new_today, new_text_for_today]:
            assert text in text_list
        for text in [today, text_for_today]:
            assert text not in text_list

    # test removes
    # without given flag
    with mock.patch("sys.argv", [""] + ["remove"]):
        test_remove = todo.todo_action()
        assert (
            test_remove == "For this action(remove) following flags are required: -th"
        )

    # wrong hash
    with mock.patch("sys.argv", [""] + ["remove", "-th", "wrong hash"]):
        test_remove = todo.todo_action()
        assert test_remove == "There is no task with this hash: wrong hash"

    # removes
    with mock.patch("sys.argv", [""] + ["remove", "-th", past_hash]):
        test_remove = todo.todo_action()
        assert test_remove == "Task removed"
    with mock.patch("sys.argv", [""] + ["remove", "-th", today_hash]):
        test_remove = todo.todo_action()
        assert test_remove == "Task removed"
    with mock.patch("sys.argv", [""] + ["remove", "-th", future_hash]):
        test_remove = todo.todo_action()
        assert test_remove == "Task removed"

    # checks if hashes are removed
    with mock.patch("sys.argv", [""] + ["list"]):
        text_for_list = todo.todo_action()
        text_list = text_for_list.split()
        for hash in [past_hash, today_hash, future_hash]:
            assert hash not in text_list

