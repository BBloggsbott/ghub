"""Utilities to run GHub"""
from .ghubutils import Context, GHub
from .cliutils import Interpreter
from ._version import __version__
from termcolor import colored
import colorama

import os
import sys


def run_ghub():
    """Run GHub"""
    colorama.init()
    if len(sys.argv) == 1:
        print("Welcome to GHub - Browse GitHub like it is UNIX")
        print("Starting initial setup...")
        ghub = GHub()
        interpreter = Interpreter()
        print("Setup done.")
        cli_runner(ghub, interpreter)
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--version" or sys.argv[1] == "-v":
            print(__version__)
            return
        ghub = GHub()
        interpreter = Interpreter()
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            interpreter.execute("help", ghub)
            return
        script_runner(sys.argv[1], ghub, interpreter)


def script_runner(filename, ghub, interpreter):
    try:
        script_file = open(filename, "r")
    except:
        print("Error opening file {}".format(filename))
        sys.exit(1)
    command = script_file.readlines()
    script_file.close()
    interpreter = Interpreter()
    for cmd in command:
        interpreter.execute(cmd, ghub)


def cli_runner(ghub, interpreter):
    while True:
        print(
            "ghub:{} {}>".format(
                colored(ghub.context.context, "yellow"),
                colored(ghub.context.location, "green"),
            ),
            end=" ",
        )
        command = input()
        interpreter.execute(command, ghub)
