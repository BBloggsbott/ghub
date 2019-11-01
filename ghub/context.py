import copy


class Context(object):
    """Class to maintain the context of the current GHub session"""

    def __init__(self, user=None, prev_context=None):
        """Initialize a Context object"""
        if prev_context != None:
            self.prev_context = prev_context.deepcopy()
            self.root_location = copy.deepcopy(prev_context.root_location)
            return
        self.context = "root"  # the current context
        self.location = user["login"]  # the current location in the GitHub tree
        self.root_location = user["login"]  # the root location
        self.prev_context = None
        self.cache = None

    def set_context_to_repo(self, username, reponame):
        """Set the context to that of a repository

        Keyword arguments:
        username -- the username of the repository owner
        reponame - the name of the repository
        """
        self.prev_context = self.deepcopy()
        self.context = "repo"
        self.location = username + "/" + reponame

    def set_context_to_user(self, username, tab=""):
        """Set the context to that of a user

        Keyword arguments:
        username -- the username of the user
        reponame - the current tab (example: repos, followers, following)
        """
        self.prev_context = self.deepcopy()
        self.context = "user"
        self.location = username + "/" + tab

    def set_context_to_root(self, user=None):
        """Set the context to that of the authorized user

        Keyword arguments:
        user -- the info of the authorized user from ghub session, for use while reauthorizing
        """
        self.prev_context = self.deepcopy()
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
        self.prev_context = self.deepcopy()
        self.context = "orgs"
        self.location = orgname + "/" + tab

    def deepcopy(self):
        return copy.deepcopy(self)

    def set_prev_context(self, prev_context):
        self.prev_context = prev_context.copy()
