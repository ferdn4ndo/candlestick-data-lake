import glob
import os
import sys

import importlib


def get_commands_list():
    scripts = []
    ignored_files = ["__init__.py"]
    for file in glob.glob(os.path.join(sys.path[0], "commands", "*.py")):
        if os.path.basename(file) in ignored_files:
            continue
        scripts.append(os.path.basename(file).replace(".py", ""))
    return scripts


def run_script():
    available_commands = get_commands_list()
    sys.argv.pop(0)  # Removes the 'manage.py' argument

    if not len(sys.argv) or sys.argv == ["--help"]:
        print("You must specify at least the first argument, which is the name of the management script to run")
        print("The list of available commands are:")
        print("\t" + "\n\t".join(available_commands))
        return

    command = sys.argv[0]
    script_path = os.path.join(sys.path[0], "commands", "{}.py".format(command))

    if not os.path.exists(script_path):
        raise FileNotFoundError("The script file {} was not found!".format(script_path))

    command_module = importlib.import_module("app.commands.{}".format(command))

    if not hasattr(command_module, "execute") or not hasattr(command_module, "show_help"):
        raise TypeError("The command script must have the methods 'execute' and 'show help'")

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Help for command {}:".format(command))
        print(command_module.show_help())
        return

    command_module.execute(sys.argv)


if __name__ == "__main__":
    run_script()
