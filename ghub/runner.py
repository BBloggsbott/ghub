"""Utilities to run GHub"""
from .ghubutils import Context, GHub
from .cliutils import Interpreter

import os

def run_ghub():
    """Run GHub"""
    print("Welcome to GHub - Browse GitHub like it is UNIX")
    print("Starting initial setup...")
    ghub = GHub()
    interpreter = Interpreter()
    print("Setup done.")
    while(True):
        command = input("ghub:{} {}> ".format(ghub.context.context, ghub.context.location))
        interpreter.execute(command, ghub)
