"""Utilities for interacting with GitHub"""
import os
import json
import webbrowser

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
        response = ghub.github.fetch_token(
            token_url,
            client_secret=ghub.client_secret,
            authorization_response=redirect_response,
        )
        if not os.path.isdir(ghub.data_path):
            os.makedirs(ghub.data_path)
        data_file = open(ghub.data_path / ghub.auth_filename, "w+")
        json.dump(response, data_file)
        data_file.close()
        ghub.oauth_data = response
        return True
    else:
        data_file = open(ghub.data_path / ghub.auth_filename, "r")
        oauth_data = json.loads(data_file.read())
        data_file.close()
        ghub.oauth_data = oauth_data
        ghub.github.token = oauth_data
        return True


def get_user_tabs(ghub, tab=""):
    if ghub.context.context == "root":
        if tab == "":
            new_context = ghub.context.deepcopy()
            new_context.set_prev_context(ghub.context)
            ghub.context = new_context
            ghub.context.set_context_to_root()
        elif tab == "repos":
            response = ghub.github.get(ghub.api_url + ghub.endpoints["user"] + "/repos")
            if response.status_code == 200:
                ghub.context = Context(prev_context=ghub.context)
                ghub.context.cache = response.json()
                ghub.context.location = ghub.user["login"] + "/" + "repos"
                ghub.context.context = "repos"
            else:
                print("Error getting repo data - " + response.status_code)
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
