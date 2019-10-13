"""Utilities to run GHub"""
from .ghubutils import Context, GHub
from .cliutils import Interpreter

def run_ghub():
    """Run GHub"""
    print("Welcome to GHub - A Unix like CLI for GitHub.")
    print("Starting initial setup...")
    ghub = GHub()
    context = Context(ghub.user)
    interpreter = Interpreter()
    print("Setup done.")
    while(True):
        command = input("ghub:{} {}> ".format(context.context, context.location))
        interpreter.execute(command, ghub, context)
