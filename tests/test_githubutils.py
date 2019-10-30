from ghub import githubutils
from ghub.ghubutils import GHub


class TestGitHubUtils:
    def test_authorize(self):
        ghub = GHub(fromenv=True)
        auth = githubutils.authorize(ghub, fromenv=True)
        assert auth == True

    def test_get_user_tabs(self):
        ghub = GHub(fromenv=True)
        githubutils.get_user_tabs(ghub, "repos")
        assert ghub.context.context == "repos"
        assert ghub.context.location == "BBloggsbott/repos"

    def test_latest_commit(self):
        ghub = GHub(fromenv=True)
        res = githubutils.get_latest_commit(ghub, "BBloggsbott/ghub")
        assert res != False

    def test_get_tree(self):
        ghub = GHub(fromenv=True)
        res = githubutils.get_tree(ghub, "BBloggsbott/ghub")
        assert res != False
