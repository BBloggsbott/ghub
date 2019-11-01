import sys
import os
from termcolor import colored

from .githubutils import authorize, get_user_tabs, get_tree
from .repoutils import get_items_in_tree, get_blob_content
from .context import Context


class CD(object):
    def __init__(self):
        self.help = "Change context. Usage: \ncd user USERNAME\ncd org ORGNAME\ncd USERNAME/REPONAME"
        self.argnos = [0, 1, 2]

    def __call__(self, args, ghub):
        if len(args) == 1:
            if args[0] == "..":
                ghub.context = ghub.context.prev_context
            elif ghub.context.context == "root" or ghub.context.context == "user":
                get_user_tabs(ghub, args[0])
            elif ghub.context.context == "repos":
                repo = "{}/{}".format(ghub.context.location.split("/")[0], args[0])
                current_tree = get_tree(ghub, repo)
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
