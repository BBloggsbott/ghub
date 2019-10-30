"""Utilities for GHub"""
from pathlib import Path
from requests_oauthlib import OAuth2Session
import json

from .githubutils import authorize


class GHub(object):
    """Object that creates a GHub session"""

    api_url = "https://api.github.com/"  # URL for GitHub API
    endpoints = {
        "users": "users/",
        "user": "user",
        "repos": "repos/",
    }  # Endpoints for GitHub API
    client_id = "ad1ef4c67333561cc9ea"  # client ID for GitHub's OAuth
    client_secret = (
        "1931c8c29d363fb5bbe9c3e885de8a8036790bcb"
    )  # client secret for GitHub's OAuth

    def __init__(self, reauthorize=False):
        """Initialize the GHub session

        Keyword arguments:
        reauthorize -- performs authorization again (defauls False)
        """
        self.data_path = (
            Path.home() / ".ghub"
        )  # Path to all the files to locally save info for ghub
        self.auth_filename = "auth.json"  # Filename with OAuth info
        self.github = OAuth2Session(self.client_id)  # OAuth2Session for github
        self.oauth_data = ""  # Data from GitHub OAuth
        authorize(self, reauthorize)
        self.user = json.loads(
            self.github.get(self.api_url + self.endpoints["user"]).content.decode(
                "utf-8"
            )
        )  # Info of the Authorized user
        self.context = Context(self.user)
        self.print_auth_user()

    def print_auth_user(self):
        """Print the user Authorized with GHub"""
        print("Logged in as {}".format(self.get_user_username()))

    def get_user_username(self):
        """Get the username of the user Authorized with GHub"""
        return self.user["login"]


class Context(object):
    """Class to maintain the context of the current GHub session"""

    def __init__(self, user):
        """Initialize a Context object"""
        self.context = "root"  # the current context
        self.location = user["login"]  # the current location in the GitHub tree
        self.root_location = user["login"]  # the root location
        self.cache = None

    def set_context_to_repo(self, username, reponame):
        """Set the context to that of a repository

        Keyword arguments:
        username -- the username of the repository owner
        reponame - the name of the repository
        """
        self.context = "repo"
        self.location = username + "/" + reponame

    def set_context_to_user(self, username, tab=""):
        """Set the context to that of a user

        Keyword arguments:
        username -- the username of the user
        reponame - the current tab (example: repos, followers, following)
        """
        self.context = "user"
        self.location = username + "/" + tab

    def set_context_to_root(self, user=None):
        """Set the context to that of the authorized user

        Keyword arguments:
        user -- the info of the authorized user from ghub session, for use while reauthorizing
        """
        self.context = "root"
        if user != None:
            self.root_location = user
        self.location = self.root_location

    def set_context_to_org(self, orgname, tab=""):
        """Set the context to that of an organisation

        Keyword arguments:
        orgname -- name of the arganisation
        tab -- the current tab (example: repos, followers, following)
        """
        self.context = "orgs"
        self.location = orgname + "/" + tab
