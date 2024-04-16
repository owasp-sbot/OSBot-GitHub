from dotenv import load_dotenv

from osbot_github.api.cache.TestCase__GitHub__API import TestCase__GitHub__API
from osbot_github.dbs.Sqlite__GitHub import Sqlite__GitHub, DB_NAME__GIT_HUB
from osbot_github.dbs.Sqlite__GitHub__Load_Data import Sqlite__GitHub__Load_Data
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_name
from tests.api.cache.test_GitHub__API__Cache import GIT_HUB__USER_NAME
from tests.dbs.test_Sqlite__GitHub import GIT_HUB__TEST__ORGANIZATION



class test_Sqlite__GitHub__Load_Data__for__Org(TestCase__GitHub__API):
    config_data   : dict
    load_data     : Sqlite__GitHub__Load_Data
    sqlite_github : Sqlite__GitHub

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config_data   = {'name': GIT_HUB__TEST__ORGANIZATION,
                             'name_type': 'organization'}
        cls.load_data     = Sqlite__GitHub__Load_Data(cls.config_data)
        cls.sqlite_github = cls.load_data.sqlite_github

    def test___init__(self):
        name      = self.config_data.get('name'     )
        name_type = self.config_data.get('name_type')
        with self.sqlite_github as _:
            assert self.sqlite_github.config_data() == self.config_data
            assert file_name(self.sqlite_github.db_path) == DB_NAME__GIT_HUB.format(name=name, type=name_type)

    def test_load_repos(self):
        result = self.load_data.load_repos()


class test_Sqlite__GitHub__Load_Data__for__User(TestCase__GitHub__API):
    config_data   : dict
    load_data     : Sqlite__GitHub__Load_Data
    sqlite_github : Sqlite__GitHub

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.config_data   = {'name': GIT_HUB__USER_NAME,
                             'name_type': 'user'}
        cls.load_data     = Sqlite__GitHub__Load_Data(cls.config_data)
        cls.sqlite_github = cls.load_data.sqlite_github

    def test___init__(self):
        name      = self.config_data.get('name'     )
        name_type = self.config_data.get('name_type')
        with self.sqlite_github as _:
            assert self.sqlite_github.config_data() == self.config_data
            assert file_name(self.sqlite_github.db_path) == DB_NAME__GIT_HUB.format(name=name, type=name_type)

    def test_load_repos(self):
        result = self.load_data.load_repos()
        #pprint(self.cache.sqlite_requests.db_path)
