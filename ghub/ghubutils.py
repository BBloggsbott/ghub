"""Utilities for GHub"""
from pathlib import Path
from requests_oauthlib import OAuth2Session
import json
import sys

from .githubutils import authorize
from .context import Context


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

    def __init__(self, reauthorize=False, fromenv=False):
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
        try:
            authorize(self, reauthorize, fromenv)
        except:
            print(
                "Error performing Authorization from existing credentials. Restarting Authorization procedure."
            )
            authorize(self, reauthorize=True)
        try:
            self.user = json.loads(
                self.github.get(self.api_url + self.endpoints["user"]).content.decode(
                    "utf-8"
                )
            )  # Info of the Authorized user
        except:
            print(
                "Error getting user details. Check network connection and try again.\nQuiting GHub."
            )
            sys.exit(1)
        self.context = Context(user=self.user)
        self.print_auth_user()

    def print_auth_user(self):
        """Print the user Authorized with GHub"""
        print("Logged in as {}".format(self.get_user_username()))

    def get_user_username(self):
        """Get the username of the user Authorized with GHub"""
        return self.user["login"]
