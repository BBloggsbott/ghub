from ghub.commands import REAUTHORIZE, EXIT, CD, LS, CLEAR, CAT
from ghub.ghubutils import GHub


class TestCommandsClass:
    def test_cd(self):
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
