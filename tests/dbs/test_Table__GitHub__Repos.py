from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

from osbot_github.dbs.Table__GitHub__Repos import Table__GitHub__Repos, REPO__OSBOT_GIT_HUB
from osbot_utils.utils.Dev import pprint


class test_Table__GitHub__Repos(TestCase):

    def setUp(self):
        self.github_repos = Table__GitHub__Repos()

    def test_create(self):
        assert self.github_repos.table().exists() is True

    def test_repo(self):
        repo_full_name = REPO__OSBOT_GIT_HUB
        result         = self.github_repos.repo(repo_full_name=repo_full_name)

        assert self.github_repos.table().rows() == []

        #pprint(result)
    def test_table(self):
        with self.github_repos.table() as _:
            assert type(_) is Sqlite__Table
            assert _.rows() == []

    # def test_raw_github_repos(self):
    #     result = self.github_repos.raw_github_repos()
    #     pprint(result)
