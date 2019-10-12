from pathlib import Path
from requests_oauthlib import OAuth2Session
import json

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
