from ghub.ghubutils import Context


class TestContextClass:
    def test_default_context(self):
        context = Context({"login": "testuser"})
        assert context.context == "root"
        assert context.location == "testuser"
        assert context.root_location == "testuser"
        assert context.cache == None

    def test_change_to_repo(self):
        context = Context({"login": "testuser"})
        context.set_context_to_repo("testuser1", "testrepo")
        assert context.context == "repo"
        assert context.location == "testuser1/testrepo"

    def test_change_to_repo(self):
        context = Context({"login": "testuser"})
        context.set_context_to_user("testuser1")
        assert context.context == "user"
        assert context.location == "testuser1/"
        context.set_context_to_user("testuser1", "stars")
        assert context.context == "user"
        assert context.location == "testuser1/stars"

    def test_default_context(self):
        context = Context({"login": "testuser"})
        context.set_context_to_repo("testuser1", "testrepo")
        assert context.context == "repo"
        context.set_context_to_root()
        assert context.context == "root"
        assert context.location == "testuser"
        assert context.root_location == "testuser"
        assert context.cache == None

    def test_change_to_repo(self):
        context = Context({"login": "testuser"})
        context.set_context_to_org("testorg")
        assert context.context == "orgs"
        assert context.location == "testorg/"
        context.set_context_to_org("testorg", "repos")
        assert context.context == "orgs"
        assert context.location == "testorg/repos"
