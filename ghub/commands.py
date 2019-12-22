import sys
import os
from termcolor import colored

from .githubutils import (
    event_dict,
    authorize,
    get_user_tabs,
    get_tree,
    get_user,
    get_org,
    clone_repo,
    star_repo,
    unstar_repo,
    watch_repo,
    unwatch_repo,
    fork_repo,
    get_prs,
    get_pr,
    get_pr_info,
    get_issues,
    get_issue,
    get_issue_info,
)
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
            elif (
                ghub.context.context == "root"
                or ghub.context.context == "user"
                or ghub.context.context == "org"
            ):
                get_user_tabs(ghub, args[0])
            elif ghub.context.context == "repos" or ghub.context.context == "stars":
                if ghub.context.context == "repos":
                    repo = "{}/{}".format(ghub.context.location.split("/")[0], args[0])
                elif ghub.context.context == "stars":
                    repo = "{}".format(args[0])
                current_tree = get_tree(ghub, repo)
                if not current_tree:
                    print("Repo not found")
                    return
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.context = "repo"
                ghub.context.location = repo
                ghub.context.cache = current_tree
            elif ghub.context.context == "repo":
                if args[0] == "pull_requests":
                    get_prs(ghub)
                    return
                elif args[0] == "issues":
                    get_issues(ghub)
                    return
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
                print("{} does not exist.".format(args[0]))
            elif ghub.context.context == "pull_requests":
                get_pr(ghub, args[0])
            elif ghub.context.context == "issues":
                get_issue(ghub, args[0])
        elif len(args) == 2:
            if args[0] == "user":
                get_user(ghub, args[1])
            elif args[0] == "repo":
                repo = args[1]
                current_tree = get_tree(ghub, repo)
                if not current_tree:
                    print("Location not found")
                    return
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.context = "repo"
                ghub.context.location = repo
                ghub.context.cache = current_tree
            elif args[0] == "org":
                get_org(ghub, args[1])
        elif len(args) == 0:
            ghub.context.set_context_to_root()
        else:
            print("Under development")


class LS(Command):
    def __init__(self):
        self.setup("ls", "List everything in the current context")
        self.default_repo_items = ["pull_requests"]

    def __call__(self, args, ghub):
        if (
            ghub.context.context == "root"
            or ghub.context.context == "user"
            or ghub.context.context == "org"
        ):
            if ghub.context.context == "root":
                out = "repos\nstars\nfollowers\nfollowing\nnotifications"
            else:
                out = "repos\nstars\nfollowers\nfollowing"
            print(colored(out, "green", attrs=["bold"]))
        if ghub.context.context == "repos" or ghub.context.context == "stars":
            for i in ghub.context.cache:
                print(
                    i["name"] if not ghub.context.context == "stars" else i["full_name"]
                )
        elif ghub.context.context == "repo":
            for i in self.default_repo_items:
                print(colored(i, "yellow"))
            for i in get_items_in_tree(ghub):
                if i[1] == "tree":
                    print(colored(i[0], "green", attrs=["bold"]))
                else:
                    print(i[0])

        elif ghub.context.context == "followers" or ghub.context.context == "following":
            for i in ghub.context.cache:
                print(i["login"])
        elif ghub.context.context == "notifications":
            for i in ghub.context.cache:
                print(
                    "{}\n\t{}".format(
                        colored(
                            i["repository"]["owner"]["login"]
                            + "/"
                            + i["repository"]["name"],
                            "yellow",
                        ),
                        i["subject"]["title"],
                    )
                )
        elif ghub.context.context == "pull_requests":
            for i in ghub.context.cache:
                print("{} : {}".format(colored(i["number"], "yellow"), i["title"]))


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
        elif ghub.context.context == "pull_request":
            if len(args) == 0:
                pr = ghub.context.cache
                print(colored(pr["title"], "green"))
                print(
                    "{} wants to merge {} to {}".format(
                        pr["user"]["login"], pr["head"]["label"], pr["base"]["label"]
                    )
                )
                print("About:\n{}".format(pr["body"]))
            elif len(args) == 1:
                if args[0] == "comments":
                    pr = ghub.context.cache
                    content, code = get_pr_info(ghub)
                    if code == 200:
                        for i in content:
                            owner = (
                                i["author_association"] == "OWNER"
                                or i["author_association"] == "MEMBER"
                            )
                            color = "green" if owner else "yellow"
                            print(
                                "{}: {}".format(
                                    colored(i["user"]["login"], color), i["body"]
                                )
                            )
                    else:
                        print("Error fetching the comments")
                elif args[0] == "commits":
                    pr = ghub.context.cache
                    content, code = get_pr_info(ghub, "commits")
                    if code == 200:
                        for i in content:
                            print(
                                "{} by {}".format(
                                    colored(i["commit"]["message"], "yellow"),
                                    colored(i["committer"]["login"], "green"),
                                )
                            )
                    else:
                        print("Error fetching the commits")
                elif args[0] == "events":
                    events, response_code = get_issue_info(ghub, "events")
                    if response_code == 200:
                        for event in events:
                            if event["event"] in event_dict.keys():
                                print(event_dict[event["event"]](event))
                            else:
                                print(" ".join(event["event"].split("_")))
                    else:
                        print("There was an error getting the events.")
        elif ghub.context.context == "issue":
            if len(args) == 0:
                issue = ghub.context.cache
                labels = []
                for i in issue["labels"]:
                    label = i["name"]
                    labels.append(label)
                print(
                    "[{}] {}".format(
                        colored(issue["state"], "yellow"),
                        colored(issue["title"], "green"),
                    )
                )
                print("Created by {}".format(issue["user"]["login"]))
                print("Labels: {}".format(", ".join(labels)))
                print(issue["body"])
            if len(args) == 1:
                if args[0] == "comments":
                    content, code = get_issue_info(ghub)
                    if code == 200:
                        for i in content:
                            owner = (
                                i["author_association"] == "OWNER"
                                or i["author_association"] == "MEMBER"
                            )
                            color = "green" if owner else "yellow"
                            print(
                                "{}: {}\n".format(
                                    colored(i["user"]["login"], color), i["body"]
                                )
                            )
                    else:
                        print("Error fetching the comments")
                if args[0] == "events":
                    events, response_code = get_issue_info(ghub, "events")
                    if response_code == 200:
                        for event in events:
                            if event["event"] in event_dict.keys():
                                print(event_dict[event["event"]](event))
                            else:
                                print(" ".join(event["event"].split("_")))
                    else:
                        print("There was an error getting the events.")
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


class STAR(Command):
    def __init__(self):
        self.setup("star", "Star the repo")

    def __call__(self, args, ghub):
        if len(args) == 0:
            if ghub.context.context == "repo":
                star_repo(ghub)
            else:
                print("Not in repo context.")
        elif len(args) == 1:
            star_repo(ghub, args[0])


class UNSTAR(Command):
    def __init__(self):
        self.setup("unstar", "Unstar the repo")

    def __call__(self, args, ghub):
        if len(args) == 0:
            if ghub.context.context == "repo":
                unstar_repo(ghub)
            else:
                print("Not in repo context.")
        elif len(args) == 1:
            unstar_repo(ghub, args[0])


class WATCH(Command):
    def __init__(self):
        self.setup("watch", "Watch a repo")

    def __call__(self, args, ghub):
        if len(args) == 0:
            if ghub.context.context == "repo":
                watch_repo(ghub)
            else:
                print("Not in repo context.")
        elif len(args) == 1:
            watch_repo(ghub, args[0])


class UNWATCH(Command):
    def __init__(self):
        self.setup("unwatch", "Unwatch a repo")

    def __call__(self, args, ghub):
        if len(args) == 0:
            if ghub.context.context == "repo":
                unwatch_repo(ghub)
            else:
                print("Not in repo context.")
        elif len(args) == 1:
            unwatch_repo(ghub, args[0])


class FORK(Command):
    def __init__(self):
        self.setup("fork", "fork a repo")

    def __call__(self, args, ghub):
        if len(args) == 0:
            if ghub.context.context == "repo":
                fork_repo(ghub)
            else:
                print("Not in repo context.")
        elif len(args) == 1:
            fork_repo(ghub, args[0])
