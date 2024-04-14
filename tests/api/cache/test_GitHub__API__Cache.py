from unittest                                                   import TestCase

from github.NamedUser import NamedUser
from github.Organization import Organization
from github.Repository import Repository

from osbot_github.api.GitHub__API import GitHub__API
from osbot_github.api.cache.GitHub__API__Cache import GitHub__API__Cache, SQLITE_DB_NAME__GIT_HUB_API_CACHE, \
    SQLITE_TABLE__BEDROCK_REQUESTS, Sqlite__Cache__Requests__Patch
from osbot_utils.helpers.sqlite.Sqlite__Database                import Sqlite__Database
from osbot_utils.base_classes.Kwargs_To_Self                    import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local       import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests    import Sqlite__DB__Requests
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files                                    import temp_file, parent_folder, current_temp_folder, file_exists, file_not_exists
from osbot_utils.utils.Json import json_dumps, from_json_str
from osbot_utils.utils.Objects import base_types, obj_info, pickle_save_to_bytes, pickle_load_from_bytes, obj_data

GIT_HUB__ORG_NAME__OWASP_SBOT = 'owasp-sbot'
GIT_HUB__USER_NAME            = 'DinisCruz'
GIT_HUB__REPO__OSBOT_GITHUB   = 'owasp-sbot/OSBot-GitHub'

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
            assert base_types(_)                == [Sqlite__Cache__Requests__Patch, Sqlite__Cache__Requests, Kwargs_To_Self, object]
            assert _.db_name                    == SQLITE_DB_NAME__GIT_HUB_API_CACHE
            assert _.table_name                 == SQLITE_TABLE__BEDROCK_REQUESTS
            assert type      (_.sqlite_bedrock) is Sqlite__DB__Requests
            assert base_types(_.sqlite_bedrock) == [Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object]
            assert _.sqlite_bedrock.db_name     == _.db_name
            assert _.sqlite_bedrock.table_name  == _.table_name
            assert _.pickle_response            is True


    # this is tested ok in test_GitHub_API
    # def test_user(self):
    #     self.github_api_cache.patch_apply()
    #     print()
    #     #self.github_api_cache.disable()
    #     user_name   = GIT_HUB__USER_NAME
    #     user_1      = self.github_api_cache.user(user_name=user_name)
    #     user_2      = self.github_api_cache.user(user_name=user_name)
    #     user_3      = self.github_api_cache.user(user_name=user_name)
    #     assert type(user_1) is NamedUser
    #     assert type(user_2) is NamedUser
    #     assert type(user_3) is NamedUser

    # def test_monkey_patch(self):
    #     self.github_api_cache.patch_apply()
    #
    #     print()
    #     print()
    #     github_api = GitHub__API()
    #     user_name = 'DinisCruz'
    #     user_1  = github_api.user(user_name=user_name)
    #     user_1.get_repos()[0]
    #     user_1.get_repos()[0]
    #
    #     user_2 = github_api.user(user_name=user_name)
    #     user_3 = github_api.user(user_name=user_name)
    #     #pprint(user)
    #     #repos = user.get_repos()
    #     #repo = repos[30]
    #     # list(repos)
    #     # list(repo.get_commits())
    #     #
    #
    #     #self.github_api_cache.organization(org_name='OWASP')




