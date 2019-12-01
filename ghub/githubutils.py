"""Utilities for interacting with GitHub"""
import os
import json
import webbrowser
import stat
import sys
from git import Repo

from .context import Context


def authorize(ghub, reauthorize=False, fromenv=False):
    """Authorize a user for GHub

    Keyword arguments:
    ghub -- the ghub object that needs authorization
    reauthorize -- performs authorization again (default False)
    """
    if fromenv:
        oauth_data = json.loads(os.environ["GHUB_CRED"])
        ghub.oauth_data = oauth_data
        ghub.github.token = oauth_data
        return True
    if not os.path.isfile(ghub.data_path / ghub.auth_filename) or reauthorize:
        authorization_base_url = "https://github.com/login/oauth/authorize"
        token_url = "https://github.com/login/oauth/access_token"
        authorization_url, _ = ghub.github.authorization_url(authorization_base_url)
        webbrowser.open(authorization_url)
        print("Please visit this site and grant access: {}".format(authorization_url))
        redirect_response = input(
            "Please enter the URL you were redirected to after granting access: "
        )
        # try:
        response = ghub.github.fetch_token(
            token_url,
            client_secret=ghub.client_secret,
            authorization_response=redirect_response,
        )
        # except Exception as e:
        #    print(e)
        #    print(
        #        "Network Error. Make sure you have a working internet connection and try again."
        #    )
        #    sys.exit(1)
        if not os.path.isdir(ghub.data_path):
            os.makedirs(ghub.data_path)
        data_file = open(ghub.data_path / ghub.auth_filename, "w+")
        json.dump(response, data_file)
        data_file.close()
        os.chmod(ghub.data_path / ghub.auth_filename, stat.S_IRUSR | stat.S_IWUSR)
        ghub.oauth_data = response
        return True
    else:
        data_file = open(ghub.data_path / ghub.auth_filename, "r")
        oauth_data = json.loads(data_file.read())
        data_file.close()
        ghub.oauth_data = oauth_data
        ghub.github.token = oauth_data
        return True


def get_user(ghub, user):
    url = ghub.api_url + ghub.endpoints["users"] + user
    response = ghub.github.get(url)
    if response.status_code == 200:
        ghub.context = Context(prev_context=ghub.context)
        ghub.context.context = "user"
        ghub.context.location = user
        ghub.context.cache = response.json()
        return True
    return False


def get_user_tabs(ghub, tab=""):
    tabs = ["repos", "stars", "followers", "following", "notifications"]
    if tab not in tabs:
        print("{} is not a valid user tab".format(tab))
        return
    if ghub.context.context == "root":
        if tab == "":
            ghub.context.set_context_to_root()
        elif tab == "repos":
            response = ghub.github.get(ghub.api_url + ghub.endpoints["user"] + "/repos")
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = ghub.user["login"] + "/" + "repos"
                ghub.context.context = "repos"
            else:
                print("Error getting data - " + response.status_code)
        elif tab == "stars":
            response = ghub.github.get(
                ghub.api_url + ghub.endpoints["user"] + "/starred"
            )
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = ghub.user["login"] + "/" + "stars"
                ghub.context.context = "stars"
            else:
                print("Error getting data - " + response.status_code)
        elif tab == "followers" or tab == "following":
            response = ghub.github.get(
                ghub.api_url + ghub.endpoints["user"] + "/" + tab
            )
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = ghub.user["login"] + "/" + tab
                ghub.context.context = tab
            else:
                print("Error getting data - " + response.status_code)
        elif tab == "notifications":
            response = ghub.github.get(ghub.api_url + ghub.endpoints["notifications"])
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = ghub.user["login"] + "/" + tab
                ghub.context.context = tab
            else:
                print("Error getting data - " + response.status_code)
    elif ghub.context.context == "user":
        if tab == "":
            ghub.context.set_context_to_root()
        elif tab == "repos":
            response = ghub.github.get(
                ghub.api_url
                + ghub.endpoints["users"]
                + ghub.context.location
                + "/repos"
            )
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = (
                    ghub.context.prev_context.location + "/" + "repos"
                )
                ghub.context.context = "repos"
            else:
                print("Error getting data - " + response.status_code)
        elif tab == "stars":
            response = ghub.github.get(
                ghub.api_url
                + ghub.endpoints["users"]
                + ghub.context.location
                + "/starred"
            )
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = (
                    ghub.context.prev_context.location + "/" + "star"
                )
                ghub.context.context = "stars"
            else:
                print("Error getting data - " + response.status_code)
        elif tab == "followers" or tab == "following":
            response = ghub.github.get(
                ghub.api_url
                + ghub.endpoints["users"]
                + ghub.context.location
                + "/"
                + tab
            )
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = ghub.context.prev_context.location + "/" + tab
                ghub.context.context = tab
            else:
                print("Error getting data - " + response.status_code)
    else:
        pass


def get_latest_commit(ghub, repo, branch="master"):
    api_url = "https://api.github.com/repos/{}/branches/{}".format(repo, branch)
    response = ghub.github.get(api_url)
    if response.status_code == 200:
        response = response.json()
        return response["commit"]["commit"]
    else:
        return False


def get_tree(ghub, repo=None, branch="master", tree_url=None):
    if tree_url == None:
        latest_commit = get_latest_commit(ghub, repo, branch)
        if latest_commit == False:
            return False
        response = ghub.github.get(latest_commit["tree"]["url"])
        if response.status_code == 200:
            response = response.json()
            return response
        return False
    else:
        response = ghub.github.get(tree_url)
        if response.status_code == 200:
            response = response.json()
            return response


def get_blob(ghub, blob_url):
    response = ghub.github.get(blob_url)
    if response.status_code == 200:
        return response.json()
    return False


def clone_repo(ghub, dir, repo_name=None):
    print("Preparing to clone...")
    if repo_name == None:
        repo_name = "/".join(ghub.context.location.split("/")[:2])
    if dir[0] == "~":
        dir = os.path.expanduser("~") + dir[1:]
    dir = dir + "/" + repo_name.split("/")[1]
    try:
        Repo.clone_from("https://github.com/" + repo_name, dir)
        print("{} cloned to {}".format(repo_name, dir))
    except Exception as e:
        print(e)


def star_repo(ghub, repo_name=None):
    print("Starring repo...")
    if repo_name == None:
        repo_name = ghub.context.location
    star_url = ghub.api_url + ghub.endpoints["user"] + "/" + "starred/" + repo_name
    response = ghub.github.get(star_url)
    if response.status_code == 204:
        print("Repo is already starred.")
    elif response.status_code == 404:
        resp = ghub.github.put(star_url)
        if resp.status_code == 204:
            print("{} starred".format(repo_name))
        else:
            print("Error starring repo")


def unstar_repo(ghub, repo_name=None):
    print("Unstarring repo...")
    if repo_name == None:
        repo_name = ghub.context.location
    star_url = ghub.api_url + ghub.endpoints["user"] + "/" + "starred/" + repo_name
    response = ghub.github.get(star_url)
    if response.status_code == 204:
        resp = ghub.github.delete(star_url)
        if resp.status_code == 204:
            print("{} unstarred".format(repo_name))
        else:
            print("Error unstarring repo")
    elif response.status_code == 404:
        print("Repo is not starred.")


def watch_repo(ghub, repo_name=None):
    print("Subscribing to repo...")
    if repo_name == None:
        repo_name = ghub.context.location
    watch_url = ghub.api_url + ghub.endpoints["repos"] + repo_name + "/subscription"
    response = ghub.github.get(watch_url)
    if response.status_code == 200:
        print("You are already watching this repo.")
    elif response.status_code == 404:
        resp = ghub.github.put(watch_url)
        if resp.status_code == 200:
            print("Watching {}".format(repo_name))
        else:
            print("Error subscribing to repo")


def unwatch_repo(ghub, repo_name=None):
    print("Unsubscribing repo...")
    if repo_name == None:
        repo_name = ghub.context.location
    watch_url = ghub.api_url + ghub.endpoints["repos"] + repo_name + "/subscription"
    response = ghub.github.get(watch_url)
    if response.status_code == 200:
        resp = ghub.github.delete(watch_url)
        if resp.status_code == 204:
            print("{} unsubscribed".format(repo_name))
        else:
            print("Error unsubscribing to repo")
    elif response.status_code == 404:
        print("You are not watching this repo.")
