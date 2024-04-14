from os import environ
from unittest import TestCase

from dotenv import load_dotenv

from osbot_github.api.cache.TestCase__GitHub__API import TestCase__GitHub__API
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

from osbot_github.dbs.Sqlite__GitHub import Sqlite__GitHub, ENV_NAME_PATH_LOCAL_DBS, DB_NAME__GIT_HUB, \
    SQLITE_TABLE__REPOS
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import parent_folder, file_name, file_exists, folder_exists, current_temp_folder

GIT_HUB__TEST__ORGANIZATION = 'Owasp-SBot'

class test_Sqlite__GitHub(TestCase__GitHub__API):

    def setUp(self):
        load_dotenv()
        self.db_github  = Sqlite__GitHub()
        self.github_api = self.db_github.github_api

    def test_setup(self):
        with self.db_github as _:
            assert _.exists()                         is True
            assert parent_folder(_.db_path)           == _.path_github_dbs()
            if environ.get(ENV_NAME_PATH_LOCAL_DBS):
                assert parent_folder(_.path_github_dbs()) == environ.get(ENV_NAME_PATH_LOCAL_DBS)
            else:
                assert parent_folder(_.path_github_dbs()) == current_temp_folder()
            assert file_name    (_.db_path)           == DB_NAME__GIT_HUB
            assert folder_exists(_.path_db_folder() ) is True
            assert folder_exists(_.path_github_dbs()) is True
            assert file_exists(_.db_path)             is True
            assert _.tables_names()                   == [SQLITE_TABLE__REPOS]

    def test_table_repos(self):

        with self.db_github.table_repos() as _:
            assert type(_) is Sqlite__Table
            assert _.exists() is True
            assert _.rows() == []


            organisation = self.github_api.organization(GIT_HUB__TEST__ORGANIZATION)
            repos        = organisation.get_repos()
            #pprint(repos[0])

