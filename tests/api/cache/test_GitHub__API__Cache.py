from unittest                                                   import TestCase
from osbot_github.api.cache.GitHub__API__Cache                  import GitHub__API__Cache, SQLITE_DB_NAME__GIT_HUB_API_CACHE, SQLITE_TABLE__BEDROCK_REQUESTS
from osbot_utils.helpers.sqlite.Sqlite__Database                import Sqlite__Database
from osbot_utils.base_classes.Kwargs_To_Self                    import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local       import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests    import Sqlite__DB__Requests
from osbot_utils.utils.Files                                    import temp_file, parent_folder, current_temp_folder, file_exists, file_not_exists
from osbot_utils.utils.Objects                                  import base_types


class test_GitHub__API__Cache(TestCase):
    github_api_cache : GitHub__API__Cache
    temp_db_path     : str

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path                   = temp_file(extension='sqlite')
        cls.github_api_cache               = GitHub__API__Cache(db_path = cls.temp_db_path)            # the db_path to the tmp file path
        cls.github_api_cache.add_timestamp = False                                                     # disabling timestamp since it complicates the test data verification below
        assert parent_folder(cls.github_api_cache.sqlite_bedrock.db_path) == current_temp_folder()
        assert file_exists  (cls.temp_db_path)                            is True

    @classmethod
    def tearDownClass(cls):    #file_delete(cls.temp_db_path)
        cls.github_api_cache.sqlite_bedrock.delete()
        assert file_not_exists(cls.temp_db_path) is True

    def tearDown(self):
        self.github_api_cache.cache_table().clear()

    def test___init__(self):
        with self.github_api_cache as _:
            assert type      (_)                is GitHub__API__Cache
            assert base_types(_)                == [Sqlite__Cache__Requests, Kwargs_To_Self, object]
            assert _.db_name                    == SQLITE_DB_NAME__GIT_HUB_API_CACHE
            assert _.table_name                 == SQLITE_TABLE__BEDROCK_REQUESTS
            assert type      (_.sqlite_bedrock) is Sqlite__DB__Requests
            assert base_types(_.sqlite_bedrock) == [Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object]
            assert _.sqlite_bedrock.db_name     == _.db_name
            assert _.sqlite_bedrock.table_name  == _.table_name