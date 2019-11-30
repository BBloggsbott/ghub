"""Utilities for GHub"""
from pathlib import Path
from requests_oauthlib import OAuth2Session
import json
import sys
import os

from .githubutils import authorize
from .context import Context


class GHub(object):
    """Object that creates a GHub session"""

    api_url = "https://api.github.com/"  # URL for GitHub API
    endpoints = {
        "users": "users/",
        "user": "user",
        "repos": "repos/",
        "notifications": "notifications",
    }  # Endpoints for GitHub API
    client_id = "ad1ef4c67333561cc9ea"  # client ID for GitHub's OAuth
    client_secret = (
        "b277d1af6490a841e88a3c61170598236e79dfdf"
    )  # client secret for GitHub's OAuth

    def __init__(self, reauthorize=False, fromenv=False):
        """Initialize the GHub session

        Keyword arguments:
        reauthorize -- performs authorization again (defauls False)
        """
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "TRUE"
        self.data_path = (
            Path.home() / ".ghub"
        )  # Path to all the files to locally save info for ghub
        self.auth_filename = "auth.json"  # Filename with OAuth info
        scopes = ["repo", "user", "notifications"]
        self.github = OAuth2Session(
            self.client_id, scope=scopes
        )  # OAuth2Session for github
        self.oauth_data = ""  # Data from GitHub OAuth
        # try:
        authorize(self, reauthorize, fromenv)
        # except:
        #    print(
        #        "Error performing Authorization from existing credentials. Restarting Authorization procedure."
        #    )
        #    authorize(self, reauthorize=True)
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
