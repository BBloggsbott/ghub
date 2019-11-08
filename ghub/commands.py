import sys
import os
from termcolor import colored

from .githubutils import authorize, get_user_tabs, get_tree, get_user, clone_repo
from .repoutils import get_items_in_tree, get_blob_content
from .context import Context


class Command(object):
    def __init__(self):
        pass

    def setup(self, name, help_text, argnos=[0, 1]):
        self.name = name
        self.help = help_text
        self.argnos = argnos

    def print_help(self):
        print(self.help)

    def __call__(self, args, ghub):
        print("Command not implemented")

    def is_this_command(self, cmd):
        return cmd == self.name

    def is_correct_argnos(self, args):
        return len(args) in self.argnos


class CD(Command):
    def __init__(self):
        self.setup(
            "cd",
            "Change context. Usage: \ncd user USERNAME\ncd org ORGNAME\ncd USERNAME/REPONAME",
            [0, 1, 2],
        )

    def __call__(self, args, ghub):
        if len(args) == 1:
            if args[0] == "..":
                ghub.context = ghub.context.prev_context
            elif ghub.context.context == "root" or ghub.context.context == "user":
                get_user_tabs(ghub, args[0])
            elif ghub.context.context == "repos" or ghub.context.context == "stars":
                if ghub.context.context == "repos":
                    repo = "{}/{}".format(ghub.context.location.split("/")[0], args[0])
                elif ghub.context.context == "stars":
                    repo = "{}".format(args[0])
                current_tree = get_tree(ghub, repo)
                if not current_tree:
                    print("Location not found")
                    return
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.context = "repo"
                ghub.context.location = repo
                ghub.context.cache = current_tree
            elif ghub.context.context == "repo":
                for i in ghub.context.cache["tree"]:
                    if i["path"] == args[0]:
                        if i["type"] == "tree":
                            ghub.context = Context(prev_context=ghub.context)
                            ghub.context.context = "repo"
                            ghub.context.location = (
                                ghub.context.prev_context.location + "/" + args[0]
                            )
                            ghub.context.cache = get_tree(ghub, tree_url=i["url"])
                            return
                        else:
                            print("{} is not a directory.".format(args[0]))
                            return
                print("{} does not exits.".format(args[0]))
            elif (
                ghub.context.context == "followers"
                or ghub.context.context == "following"
            ):
                for i in ghub.context.cache:
                    if i["login"] == args[0]:
                        get_user(ghub, args[0])
                        return
                print("{} does not exits.".format(args[0]))
        elif len(args) == 2:
            if args[0] == "user":
                get_user(ghub, args[1])
            if args[0] == "repo":
                repo = args[1]
                current_tree = get_tree(ghub, repo)
                if not current_tree:
                    print("Location not found")
                    return
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.context = "repo"
                ghub.context.location = repo
                ghub.context.cache = current_tree
        elif len(args) == 0:
            ghub.context.set_context_to_root()
        else:
            print("Under development")


class LS(Command):
    def __init__(self):
        self.setup("ls", "List everything in the current context")

    def __call__(self, args, ghub):
        if ghub.context.context == "root" or ghub.context.context == "user":
            print(
                colored("repos\nstars\nfollowers\nfollowing", "green", attrs=["bold"])
            )
        if ghub.context.context == "repos" or ghub.context.context == "stars":
            for i in ghub.context.cache:
                print(
                    i["name"] if not ghub.context.context == "stars" else i["full_name"]
                )
        elif ghub.context.context == "repo":
            for i in get_items_in_tree(ghub):
                if i[1] == "tree":
                    print(colored(i[0], "green", attrs=["bold"]))
                else:
                    print(i[0])
        if ghub.context.context == "followers" or ghub.context.context == "following":
            for i in ghub.context.cache:
                print(i["login"])


class EXIT(Command):
    def __init__(self):
        self.setup("exit", "Exit GHub")

    def __call__(self, args, ghub):
        if len(args) == 0:
            print("Goodbye")
            sys.exit(0)
        else:
            print("Incorrect arguments passed")


class REAUTHORIZE(Command):
    def __init__(self):
        self.setup("reauthorize", "Perform GitHub OAuth procedure again.")

    def __call__(self, args, ghub):
        authorize(ghub, True)
        ghub.context.set_context_to_root(ghub.get_user_username())
        ghub.print_auth_user()


class CLEAR(Command):
    def __init__(self):
        self.setup("clear", "Clear the screen")

    def __call__(self, args, ghub):
        os.system("cls" if os.name == "nt" else "clear")


class CAT(Command):
    def __init__(self):
        self.setup("cat", "Show the contents of a file")

    def __call__(self, args, ghub):
        if ghub.context.context == "repo":
            for i in ghub.context.cache["tree"]:
                if i["path"] == args[0]:
                    if i["type"] == "blob":
                        content = get_blob_content(ghub, i["url"])
                        print(content)
                        return True
                    else:
                        print("{} is not a file.".format(args[0]))
                        return False
            print("{} does not exits.".format(args[0]))
            return False
        else:
            print(
                "This command only works in the {} context".format(
                    colored("repo", "yellow")
                )
            )
            return False


class CLONE(Command):
    def __init__(self):
        self.setup("clone", "Clone the repo", [0, 1, 2])

    def __call__(self, args, ghub):
        if len(args) == 1:
            if ghub.context.context == "repo":
                clone_repo(ghub, args[0])
        elif len(args) == 2:
            clone_repo(ghub, args[1], args[0])
