from ghub import repoutils
from ghub.githubutils import get_tree
from ghub.ghubutils import GHub


class TestRepoUtils:
    def test_get_items(self):
        ghub = GHub(fromenv=True)
        ghub.context.cache = get_tree(ghub, "BBloggsbott/ghub")
        items = repoutils.get_items_in_tree(ghub)
        assert len(items) != 0
