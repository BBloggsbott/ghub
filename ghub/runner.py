"""Utilities to run GHub"""
from .ghubutils import Context, GHub
from .cliutils import Interpreter
from termcolor import colored

import os


def run_ghub():
    """Run GHub"""
    print("Welcome to GHub - Browse GitHub like it is UNIX")
    print("Starting initial setup...")
    ghub = GHub()
    interpreter = Interpreter()
    print("Setup done.")
    while True:
        command = input(
            "ghub:{} {}> ".format(
                colored(ghub.context.context, "yellow"),
                colored(ghub.context.location, "green"),
            )
        )
        interpreter.execute(command, ghub)
