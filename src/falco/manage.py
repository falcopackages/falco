import sys

COMMANDS = {}


def register(name):
    def wrapper(func):
        COMMANDS[name] = func
        return func

    return wrapper


@register("manage")
def run_manage(argv):
    """
    Run Django's manage.py commands.
    """
    from django.core.management import execute_from_command_line

    execute_from_command_line(argv[1:])


def main(default_command):
    command_key = sys.argv[1] if len(sys.argv) > 1 else None
    run_func = COMMANDS.get(command_key) or COMMANDS.get(default_command)

    if run_func:
        run_func(sys.argv)
    else:
        print(f"Unknown command: {command_key}, available options are {', '.join(COMMANDS.keys())}")
        sys.exit(1)
