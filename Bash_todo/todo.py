import argparse
import datetime
import sys

from sqlalchemy import asc
from terminaltables import AsciiTable
from todo_database import Todo, loadSession


def todo_action():
    """Decides which action to take by action flag

    Returns:
        [str]: specific information about action on todo application DB
    """

    # start session for DB
    global session
    session = loadSession()

    args = _get_flags_for_todo()
    information = "Provide correct flag"
    if args.action == "add":
        information = _add(args)
    elif args.action == "update":
        information = _update(args)
    elif args.action == "remove":
        information = _remove(args)
    elif args.action == "list":
        information = _list(args)

    # saves changes to DB
    session.commit()
    # prints information for user
    return information


def _get_flags_for_todo():
    """Gathers information from terminal flags

    Returns:
        [list]: Return parser with args by given flags
    """

    parser = argparse.ArgumentParser(description="Operations on todo app")
    # main arguments
    parser.add_argument(
        "action",
        type=str,
        choices=["add", "update", "remove", "list"],
        help="choose action to perform",
    )
    # optional arguments
    parser.add_argument("-n", "--name", type=str, nargs="*", help="name of the task")
    parser.add_argument(
        "-d",
        "--deadline",
        type=_valid_date,
        help="deadline of the task (format: YYYY-MM-DD)",
    )
    parser.add_argument(
        "-t", "--task", type=str, nargs="*", help="description of the task"
    )
    parser.add_argument("-th", "--task_hash", type=str, help="hash to search for task")
    # group flags only one can be active, used only for action-list
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m", "--missed", action="store_true", help="prints missed tasks"
    )
    group.add_argument(
        "-to", "--today", action="store_true", help="prints tasks for today"
    )
    group.add_argument(
        "-c", "--current", action="store_true", help="prints current not missed tasks"
    )

    return parser.parse_args()


def _valid_date(date_to_check):
    """Returns datetime object from string

    Args:
        date_to_check ([str]): string to check

    Raises:
        argparse.ArgumentTypeError: error about wrong format

    Returns:
        [datetime]: datetime object
    """
    try:
        return datetime.datetime.strptime(date_to_check, "%Y-%m-%d")
    except ValueError:
        msg = f"Not a valid date: {date_to_check}"
        raise argparse.ArgumentTypeError(msg)


def _add(args):
    """Adds task to todo DB

    Args:
        args ([list]): information from flags to work with

    Returns:
        [str]: Information about action
    """
    if all([args.name, args.deadline, args.task]):
        task_name = _format_list_from_flag_into_text(args.name)
        task_text = _format_list_from_flag_into_text(args.task)
        obj_to_add = Todo(name=task_name, deadline=args.deadline, task=task_text)
        session.add(obj_to_add)
        return "Task created"
    else:
        return _information_about_missing_flags("-n, -d, -t", args)


def _update(args):
    if args.task_hash:
        # try to catch object
        object_to_update = (
            session.query(Todo).filter(Todo.TASK_HASH == args.task_hash).first()
        )

        if object_to_update:
            if not any([args.name, args.deadline, args.task]):
                return "Provide information what you want to update by at least one flag from: -n, -d, -t"
            else:
                if args.name:
                    object_to_update.name = _format_list_from_flag_into_text(args.name)
                if args.deadline:
                    object_to_update.deadline = args.deadline
                if args.task:
                    object_to_update.task = _format_list_from_flag_into_text(args.task)
                return "Task updated"
        else:
            return f"There is no task with this hash: {args.task_hash}"
    else:
        return _information_about_missing_flags("-th", args)


def _remove(args):
    if args.task_hash:
        object_to_remove = (
            session.query(Todo).filter(Todo.TASK_HASH == args.task_hash).first()
        )
        if object_to_remove:
            session.delete(object_to_remove)
            return "Task removed"
        else:
            return f"There is no task with this hash: {args.task_hash}"
    else:
        return _information_about_missing_flags("-th", args)


def _list(args):
    if args.missed:
        query = (
            session.query(Todo)
            .filter(Todo.deadline < datetime.datetime.today())
            .order_by(asc(Todo.deadline))
            .all()
        )
    elif args.today:
        query = (
            session.query(Todo)
            .filter(Todo.deadline == datetime.datetime.today())
            .order_by(asc(Todo.deadline))
            .all()
        )
    elif args.current:
        query = (
            session.query(Todo)
            .filter(Todo.deadline >= datetime.datetime.today())
            .order_by(asc(Todo.deadline))
            .all()
        )
    else:
        query = session.query(Todo).order_by(asc(Todo.deadline)).all()

    table_data = [["Name", "Deadline", "Task", "Task hash"]]
    for task in query:
        table_data.append([task.name, task.deadline, task.task, task.TASK_HASH])

    table = AsciiTable(table_data)
    return table.table


def _information_about_missing_flags(required_flags, args):
    """Returns info about missing flags

    Args:
        required_flags ([str]): string with required flags
        args ([object]): objet with information about action

    Returns:
        [str]: Information about wrong flags for given action
    """

    return (
        f"For this action({args.action}) following flags are required: {required_flags}"
    )


def _format_list_from_flag_into_text(text_to_format_in_list):
    """Returns formatted text from given list

    Args:
        text_to_format_in_list ([list]): list to format

    Returns:
        [str]: String from list separeted by ' '
    """

    return " ".join(text_to_format_in_list)


if __name__ == "__main__":
    print(todo_action())
