import requests
from pathlib import Path
import os
import json
import webbrowser

from requests_oauthlib import OAuth2Session

def authorize(ghcli, reauthorize = False):
    if not os.path.isfile(ghcli.data_path / ghcli.auth_filename) or reauthorize:
        authorization_base_url = 'https://github.com/login/oauth/authorize'
        token_url = 'https://github.com/login/oauth/access_token'
        authorization_url, state = ghcli.github.authorization_url(authorization_base_url)
        webbrowser.open(authorization_url)
        print("Please visit this site and grant access: {}".format(authorization_url))
        redirect_response = input("Please enter the URL you were redirected to after granting access: ")
        response = ghcli.github.fetch_token(token_url, client_secret=ghcli.client_secret, authorization_response=redirect_response)
        if not os.path.isdir(ghcli.data_path):
            os.makedirs(ghcli.data_path)
        data_file = open(ghcli.data_path / ghcli.auth_filename, "w+")
        json.dump(response, data_file)
        data_file.close()
        ghcli.oauth_data = response
    else:
        data_file = open(ghcli.data_path / ghcli.auth_filename, "r")
        oauth_data = json.loads(data_file.read())
        data_file.close()
        ghcli.oauth_data = oauth_data
        ghcli.github.token = oauth_data

        


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
        print("Logged in as {}".format(self.user["login"]))
