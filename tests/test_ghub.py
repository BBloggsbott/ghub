from ghub.ghubutils import GHub


class TestGHubClass:
    def test_instance_creation(self):
        ghub = GHub(fromenv=True)
        assert ghub.user["login"] == "BBloggsbott"
        assert ghub.context.context == "root"
