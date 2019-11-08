from ghub.commands import REAUTHORIZE, EXIT, CD, LS, CLEAR, CAT
from ghub.ghubutils import GHub


class TestCommandsClass:
    def test_cd_repos(self):
        cd = CD()
        assert cd.name == "cd"
        assert len(cd.argnos) == 3
        assert sum([i in cd.argnos for i in range(3)]) == 3
        ghub = GHub(fromenv=True)
        assert ghub.context.context == "root"
        args = ["repos"]
        cd(args, ghub)
        assert ghub.context.context == "repos"
        args = ["ghub"]
        cd(args, ghub)
        assert ghub.context.context == "repo"
        assert ghub.context.location == "BBloggsbott/ghub"
        args = [".."]
        cd(args, ghub)
        assert ghub.context.context == "repos"
        args = ["ghub"]
        cd(args, ghub)
        cd(args, ghub)
        assert ghub.context.location == "BBloggsbott/ghub/ghub"
        cd([], ghub)
        assert ghub.context.context == "root"
        cd(["user", "defunkt"], ghub)
        assert ghub.context.context == "user"
        args = ["repos"]
        cd(args, ghub)
        assert ghub.context.context == "repos"
        cd([".."], ghub)
        args = ["repo", "BBloggsbott/ghub"]
        cd(args, ghub)
        assert ghub.context.context == "repo"
        assert ghub.context.location == "BBloggsbott/ghub"

    def test_cd_stars(self):
        cd = CD()
        ghub = GHub(fromenv=True)
        assert ghub.context.context == "root"
        args = ["stars"]
        cd(args, ghub)
        assert ghub.context.context == "stars"
        cd([], ghub)
        assert ghub.context.context == "root"
        cd(["user", "defunkt"], ghub)
        assert ghub.context.context == "user"
        args = ["stars"]
        cd(args, ghub)
        assert ghub.context.context == "stars"

    def test_cd_followers(self):
        cd = CD()
        ghub = GHub(fromenv=True)
        assert ghub.context.context == "root"
        args = ["followers"]
        cd(args, ghub)
        assert ghub.context.context == "followers"
        assert ghub.context.location == "BBloggsbott/followers"
        args = [".."]
        cd(args, ghub)
        assert ghub.context.context == "root"
        cd(["user", "defunkt"], ghub)
        assert ghub.context.context == "user"
        args = ["followers"]
        cd(args, ghub)
        assert ghub.context.context == "followers"
        assert ghub.context.location == "defunkt/followers"
        args = [".."]
        cd(args, ghub)
        assert ghub.context.context == "user"

    def test_cd_following(self):
        cd = CD()
        ghub = GHub(fromenv=True)
        assert ghub.context.context == "root"
        args = ["following"]
        cd(args, ghub)
        assert ghub.context.context == "following"
        assert ghub.context.location == "BBloggsbott/following"
        cd(["defunkt"], ghub)
        assert ghub.context.context == "user"
        assert ghub.context.location == "defunkt"
        args = []
        cd(args, ghub)
        assert ghub.context.context == "root"
        cd(["user", "defunkt"], ghub)
        assert ghub.context.context == "user"
        args = ["following"]
        cd(args, ghub)
        assert ghub.context.context == "following"
        assert ghub.context.location == "defunkt/following"
        args = [".."]
        cd(args, ghub)
        assert ghub.context.context == "user"

    def test_cat(self):
        cd = CD()
        cat = CAT()
        ghub = GHub(fromenv=True)
        res = cat([], ghub)
        assert ghub.context.context == "root"
        assert not res
        cd(["repos"], ghub)
        cd(["ghub"], ghub)
        assert ghub.context.context == "repo"
        res = cat(["dummy.txt"], ghub)
        assert not res
        res = cat(["requirements.txt"], ghub)
        assert res
