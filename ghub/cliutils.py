"""Utilities for the command line interface"""
import sys

from .githubutils import authorize

class Interpreter(object):
    """Class to act as an in interpreter for the GHub command line"""
    def __init__(self):
        """Initialize the interpreter for GHub"""
        self.command_info = {}  # Stores met information about the commands supported by GHub
        self.add_command("reauthorize", "Perform GitHub OAuth procedure again.")
        self.add_command("cd", "Change context. Usage: \ncd user USERNAME\ncd org ORGNAME\ncd USERNAME/REPONAME", [1, 2])
        self.add_command("exit", "Exit GHub.")

    def verify(self, command):
        """Verify the syntax of the command
        
        Keyword arguments:
        command -- the command to verify
        """
        command, *args = command.split()
        if command not in self.command_info.keys():
            print("Command '{}' does not exist.".format(command))
            return False, command, args
        n_args = self.command_info[command]["num_args"]
        if len(args) not in n_args:
            print("Incorrect number of arguments passed. Accepted number of arguments: {}".format(", ".join([str(i) for i in n_args])))
            return False, command, args
        return True, command, args
        
    def help(self, command):
        """print the help string
        
        Keyword arguments:
        command -- the command to print help string
        """
        print("Command: {}\n{}".format(command, self.command_info[command]["help"]))

    def reauthorize(self, args, ghub, context):
        """execute the reauthorize command
        
        Keyword arguments:
        args -- arguments for the command
        ghub -- the GHub session
        context -- the current context of GHub
        """
        if len(args) == 0:
            authorize(ghub, True)
            context.set_context_to_root(ghub.get_user_username())
            ghub.print_auth_user()
        else:
            if args[0] != "help":
                print("Incorrect argument passed to reauthorize.")
            self.help("reauthorize")

    def exit(self, args):
        """execute the exit command
        
        Keyword arguments:
        args -- arguments for the command
        """
        if len(args) == 0:
            print("Goodbye.")
            sys.exit(0)
        else:
            if args[0] != "help":
                print("Incorrect argument passed to exit")
            self.help("exit")

    def cd(self, args):
        """execute the cd command
        
        Keyword arguments:
        args -- arguments for the command
        """
        print("Under Development.")

    def execute(self, command, ghub, context):
        """Execute a command

        Keyword arguments:
        command -- the command (as passed by user) to execute
        ghub -- the active GHub session
        context -- the current context
        """
        command = " ".join(i.strip() for i in command.split())
        verified, command, args = self.verify(command)
        if not verified:
            return
        if command == "reauthorize":
            self.reauthorize(args, ghub, context)
        elif command == "exit":
            self.exit(args)
        elif command == "cd":
            self.cd(args)

    def add_command(self, command, help = "", num_args = [0,1]):
        """Add meta information for a new command"""
        self.command_info[command] = {
            "num_args" : num_args,
            "help" : help
        }
