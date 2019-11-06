"""Utilities for the command line interface"""
import sys
import os
from termcolor import colored

from .githubutils import authorize, get_user_tabs, get_tree
from .repoutils import get_items_in_tree, get_blob_content
from .context import Context
from .commands import REAUTHORIZE, EXIT, CD, LS, CLEAR, CAT, CLONE


class Interpreter(object):
    """Class to act as an in interpreter for the GHub command line"""

    def __init__(self):
        """Initialize the interpreter for GHub"""
        self.registered_commands = []

        self.register(REAUTHORIZE())
        self.register(EXIT())
        self.register(CD())
        self.register(LS())
        self.register(CLEAR())
        self.register(CAT())
        self.register(CLONE())

    def register(self, cmd):
        self.registered_commands.append(cmd)

    def verify(self, command):
        """Verify the syntax of the command

        Keyword arguments:
        command -- the command to verify
        """
        command, *args = command.split()
        command_name_verification = False
        args_verification = False
        for cmd in self.registered_commands:
            if cmd.is_this_command(command):
                command_name_verification = True
                args_verification = cmd.is_correct_argnos(args)
                command = cmd
                break
        return command_name_verification, args_verification, command, args

    def execute(self, command, ghub):
        """Execute a command

        Keyword arguments:
        command -- the command (as passed by user) to execute
        ghub -- the active GHub session
        context -- the current context
        """
        command = " ".join(i.strip() for i in command.split())
        command_name_verified, args_verified, command, args = self.verify(command)
        if command_name_verified:
            if not args_verified:
                print("Incorrect number of arguments.")
                command.print_help()
            else:
                if len(args) > 0:
                    if args[0] == "help":
                        command.print_help()
                        return
                return command(args, ghub)

    def add_command(self, command, help="", num_args=[0, 1]):
        """Add meta information for a new command"""
        self.command_info[command] = {"num_args": num_args, "help": help}
