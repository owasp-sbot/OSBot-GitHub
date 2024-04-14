from unittest import TestCase

from osbot_github.api.GitHub__Repo import GitHub__Repo
from osbot_github.api.cache.GitHub__API__Cache import GitHub__API__Cache
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

from osbot_github.dbs.Table__GitHub__Repos import Table__GitHub__Repos, REPO__OSBOT_GIT_HUB
from osbot_utils.utils.Dev import pprint


class test_Table__GitHub__Repos(TestCase):
    github_api_cache : GitHub__API__Cache

    @classmethod
    def setUpClass(cls):
        cls.github_api_cache = GitHub__API__Cache().patch_apply()

    @classmethod
    def tearDownClass(cls):
        cls.github_api_cache.patch_restore()

    def setUp(self):
        self.github_repos = Table__GitHub__Repos()

    def test_create(self):
        assert self.github_repos.table().exists() is True

    def test_repo(self):
        repo_full_name = REPO__OSBOT_GIT_HUB
        github_repo    = self.github_repos.repo(repo_full_name=repo_full_name)
        assert type(github_repo) is GitHub__Repo
        assert github_repo.full_name == repo_full_name

    def test_table(self):
        with self.github_repos.table() as _:
            assert type(_) is Sqlite__Table
