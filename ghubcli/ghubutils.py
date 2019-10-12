from pathlib import Path
from requests_oauthlib import OAuth2Session
import json
import sys

from .githubutils import authorize

class GHub(object):
    api_url = "https://api.github.com/"
    endpoints = {
        "users" : "users/",
        "user" : "user"
    }
    client_id = "ad1ef4c67333561cc9ea"
    client_secret = "1931c8c29d363fb5bbe9c3e885de8a8036790bcb"
    def __init__(self, reauthorize = False):
        self.redir_response = ""
        self.data_path = Path.home() / ".ghub_cli"
        self.auth_filename = "auth.json"
        self.github = OAuth2Session(self.client_id)
        self.oauth_data = ""
        authorize(self, reauthorize)
        self.user = json.loads(self.github.get(self.api_url+self.endpoints["user"]).content.decode("utf-8"))
        self.print_auth_user()
    
    def print_auth_user(self):
        print("Logged in as {}".format(self.user["login"]))

class Context(object):
    def __init__(self, user):
        self.context = "root"
        self.location = user["login"]
        self.root_location = user["login"]

    def set_context_to_repo(self, username, reponame):
        self.context = "repo"
        self.location = username + "/" + reponame

    def set_context_to_user(self, username, tab = ""):
        self.context = "user"
        self.location = username + "/" + tab

    def set_context_to_root(self):
        self.context = "root"
        self.location = self.root_location

    def set_context_to_orf(self, orgname, tab=""):
        self.context = "orgs"
        self.location = orgname + "/" + tab


class Interpreter(object):
    def __init__(self):
        self.command_info = {}
        self.add_command("reauthorize", "Perform GitHub OAuth procedure again.")
        self.add_command("cd", "Change context. Usage: \ncd user USERNAME\ncd org ORGNAME\ncd USERNAME/REPONAME", [1, 2])
        self.add_command("exit", "Exit GHub.")

    def verify(self, command):
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
        print("Command: {}\n{}".format(command, self.command_info[command]["help"]))

    def reauthorize(self, args, ghub):
        if len(args) == 0:
            authorize(ghub, True)
            ghub.print_auth_user()
        else:
            if args[0] != "help":
                print("Incorrect argument passed to reauthorize.")
            self.help("reauthorize")

    def exit(self, args):
        if len(args) == 0:
            print("Goodbye.")
            sys.exit(0)
        else:
            if args[0] != "help":
                print("Incorrect argument passed to exit")
            self.help("exit")

    def cd(self, args):
        print("Under Development.")

    def execute(self, command, ghub, context):
        command = " ".join(i.strip() for i in command.split())
        verified, command, args = self.verify(command)
        if not verified:
            return
        if command == "reauthorize":
            self.reauthorize(args, ghub)
        elif command == "exit":
            self.exit(args)
        elif command == "cd":
            self.cd(args)

    def add_command(self, command, help = "", num_args = [0,1]):
        self.command_info[command] = {
            "num_args" : num_args,
            "help" : help
        }
