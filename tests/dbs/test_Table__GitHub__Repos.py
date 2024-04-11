from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

from osbot_github.dbs.Table__GitHub__Repos import Table__GitHub__Repos
from osbot_utils.utils.Dev import pprint


class test_Table__GitHub__Repos(TestCase):

    def setUp(self):
        self.github_repos = Table__GitHub__Repos()

    def test_table(self):
        with self.github_repos.table() as _:
            assert type(_) is Sqlite__Table
            assert _.rows() == []

    # def test_raw_github_repos(self):
    #     result = self.github_repos.raw_github_repos()
    #     pprint(result)
