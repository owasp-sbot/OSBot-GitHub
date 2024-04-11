from os import environ
from unittest import TestCase

from dotenv import load_dotenv

from osbot_github.dbs.Sqlite__GitHub import Sqlite__GitHub, ENV_NAME_PATH_LOCAL_DBS, DB_NAME__GIT_HUB, \
    SQLITE_TABLE__REPOS
from osbot_utils.utils.Files import parent_folder, file_name, file_exists, folder_exists


class test_Sqlite__GitHub(TestCase):

    def setUp(self):
        load_dotenv()
        self.db_github = Sqlite__GitHub()

    def test_setup(self):
        with self.db_github as _:
            assert _.exists()                         is True
            assert parent_folder(_.db_path)           == _.path_github_dbs()
            assert parent_folder(_.path_github_dbs()) == environ.get(ENV_NAME_PATH_LOCAL_DBS)
            assert file_name    (_.db_path)           == DB_NAME__GIT_HUB
            assert folder_exists(_.path_db_folder() ) is True
            assert folder_exists(_.path_github_dbs()) is True
            assert file_exists(_.db_path)             is True
            assert _.tables_names()                   == [SQLITE_TABLE__REPOS]
