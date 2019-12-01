from ghub.commands import (
    REAUTHORIZE,
    EXIT,
    CD,
    LS,
    CLEAR,
    CAT,
    STAR,
    UNSTAR,
    WATCH,
    UNWATCH,
)
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

    def test_star_unstar(self):
        cd = CD()
        star = STAR()
        unstar = UNSTAR()
        ghub = GHub(fromenv=True)
        cd(["repos"], ghub)
        cd(["ghub"], ghub)
        star_url = (
            ghub.api_url
            + ghub.endpoints["user"]
            + "/"
            + "starred/"
            + "BBloggsbott/ghub"
        )
        response = ghub.github.get(star_url)
        starred = False
        if response.status_code == 204:
            starred = True
            unstar([], ghub)
        response = ghub.github.get(star_url)
        assert response.status_code == 404
        star([], ghub)
        response = ghub.github.get(star_url)
        assert response.status_code == 204
        unstar([], ghub)
        response = ghub.github.get(star_url)
        assert response.status_code == 404
        if starred:
            star([], ghub)
        repo_name = "BBloggsbott/ghub"
        star_url = ghub.api_url + ghub.endpoints["user"] + "/" + "starred/" + repo_name
        response = ghub.github.get(star_url)
        starred = False
        if response.status_code == 204:
            starred = True
            unstar([repo_name], ghub)
        response = ghub.github.get(star_url)
        assert response.status_code == 404
        star([repo_name], ghub)
        response = ghub.github.get(star_url)
        assert response.status_code == 204
        unstar([repo_name], ghub)
        response = ghub.github.get(star_url)
        assert response.status_code == 404
        if starred:
            star([repo_name], ghub)

    def test_watch_unwatch(self):
        cd = CD()
        watch = WATCH()
        unwatch = UNWATCH()
        ghub = GHub(fromenv=True)
        cd(["repos"], ghub)
        cd(["ghub"], ghub)
        watch_url = (
            ghub.api_url
            + ghub.endpoints["repos"]
            + "BBloggsbott/ghub"
            + "/subscription"
        )
        response = ghub.github.get(watch_url)
        watching = False
        if response.status_code == 200:
            watching = True
            unwatch([], ghub)
        response = ghub.github.get(watch_url)
        assert response.status_code == 404
        watch([], ghub)
        response = ghub.github.get(watch_url)
        assert response.status_code == 200
        unwatch([], ghub)
        response = ghub.github.get(watch_url)
        assert response.status_code == 404
        if watching:
            watch([], ghub)
        repo_name = "BBloggsbott/ghub"
        watch_url = ghub.api_url + ghub.endpoints["repos"] + repo_name + "/subscription"
        response = ghub.github.get(watch_url)
        watching = False
        if response.status_code == 200:
            watching = True
            unwatch([repo_name], ghub)
        response = ghub.github.get(watch_url)
        assert response.status_code == 404
        watch([repo_name], ghub)
        response = ghub.github.get(watch_url)
        assert response.status_code == 200
        unwatch([repo_name], ghub)
        response = ghub.github.get(watch_url)
        assert response.status_code == 404
        if watching:
            watch([repo_name], ghub)
