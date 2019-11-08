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
        ghub.context = ghub.context.prev_context
        githubutils.get_user_tabs(ghub, "stars")
        assert ghub.context.context == "stars"
        assert ghub.context.location == "BBloggsbott/stars"
        ghub.context = ghub.context.prev_context
        githubutils.get_user_tabs(ghub, "following")
        assert ghub.context.context == "following"
        assert ghub.context.location == "BBloggsbott/following"
        ghub.context = ghub.context.prev_context
        githubutils.get_user_tabs(ghub, "followers")
        assert ghub.context.context == "followers"
        assert ghub.context.location == "BBloggsbott/followers"
        ghub.context = ghub.context.prev_context

    def test_latest_commit(self):
        ghub = GHub(fromenv=True)
        res = githubutils.get_latest_commit(ghub, "BBloggsbott/ghub")
        assert res != False

    def test_get_tree(self):
        ghub = GHub(fromenv=True)
        res = githubutils.get_tree(ghub, "BBloggsbott/ghub")
        assert res != False

    def test_get_user(self):
        ghub = GHub(fromenv=True)
        res = githubutils.get_user(ghub, "BBloggsbott")
        assert res != False
