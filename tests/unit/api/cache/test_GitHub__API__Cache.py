from unittest                                                   import TestCase

from github import UnknownObjectException
from github.NamedUser                                           import NamedUser
from github.Requester                                           import Requester
from osbot_github.api.GitHub__API                               import GitHub__API
from osbot_github.api.cache.GitHub__API__Cache                  import GitHub__API__Cache, SQLITE_DB_NAME__GIT_HUB_API_CACHE, Sqlite__Cache__Requests__Patch, SQLITE_TABLE__GITHUB_API_REQUESTS
from osbot_utils.helpers.sqlite.Sqlite__Database                import Sqlite__Database
from osbot_utils.base_classes.Kwargs_To_Self                    import Kwargs_To_Self
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests   import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.cache.Sqlite__DB__Requests      import Sqlite__DB__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local       import Sqlite__DB__Local
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import in_github_action
from osbot_utils.utils.Files                                    import temp_file, parent_folder, current_temp_folder, file_exists, file_not_exists
from osbot_utils.utils.Json                                     import to_json_str
from osbot_utils.utils.Objects                                  import base_types

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
        assert file_exists  (cls.temp_db_path)                            is True

    @classmethod
    def tearDownClass(cls):    #file_delete(cls.temp_db_path)
        cls.github_api_cache.sqlite_requests.delete()
        assert file_not_exists(cls.temp_db_path) is True

    def tearDown(self):
        self.github_api_cache.cache_table.clear()

    def test___init__(self):
        with self.github_api_cache as _:
            assert type      (_)                            is GitHub__API__Cache
            assert base_types(_)                            == [Sqlite__Cache__Requests__Patch, Sqlite__Cache__Requests, Kwargs_To_Self, object]
            assert _.db_name                                == SQLITE_DB_NAME__GIT_HUB_API_CACHE
            assert _.table_name                             == SQLITE_TABLE__GITHUB_API_REQUESTS
            assert type      (_.sqlite_requests)            is Sqlite__DB__Requests
            assert base_types(_.sqlite_requests)            == [Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object]
            assert parent_folder(_.sqlite_requests.db_path) == current_temp_folder()
            assert _.sqlite_requests.db_name                == _.db_name
            assert _.sqlite_requests.table_name             == _.table_name
            #assert _.pickle_response                        is True
            assert _.target_function.__qualname__           == 'Requester.__requestRaw'
            assert _.target_class                           == Requester
        assert _.target_function                        == Requester._Requester__requestRaw
        assert _.target_class                           == Requester


    def test_patch_apply__patch_restore(self):
        with self.github_api_cache as _:
            assert Requester._Requester__requestRaw              != _.target_function           # the with context will already apply the patch
            assert Requester._Requester__requestRaw.__qualname__ == 'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'
            _.patch_restore()                                                                   # restore the origin function
            assert Requester._Requester__requestRaw              == _.target_function
            assert Requester._Requester__requestRaw.__qualname__ == 'Requester.__requestRaw'
            _.patch_apply()                                                                     # appy the patch
            assert Requester._Requester__requestRaw              != _.target_function
            assert Requester._Requester__requestRaw.__qualname__ == 'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'
        assert Requester._Requester__requestRaw                  == _.target_function           # confirm the patch_restore worked at the end of the with context
        assert Requester._Requester__requestRaw.__qualname__     == 'Requester.__requestRaw'

    def test___enter____exit__(self):
        assert Requester._Requester__requestRaw == self.github_api_cache.target_function
        assert Requester._Requester__requestRaw.__qualname__ == 'Requester.__requestRaw'
        with self.github_api_cache as _:
            assert _                                             == self.github_api_cache
            assert Requester._Requester__requestRaw              != self.github_api_cache.target_function
            assert Requester._Requester__requestRaw.__qualname__ == 'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'

        assert Requester._Requester__requestRaw              == self.github_api_cache.target_function
        assert Requester._Requester__requestRaw.__qualname__ == 'Requester.__requestRaw'



    def test_user(self):
        user_name_requested = 'aaaaa'
        user_name_returned  = 'aaaaa'

        def invoke_target(target, target_args, target_kwargs):
            return 200, {}, to_json_str({'login': user_name_returned})

        original_invoke_target               = self.github_api_cache.invoke_target
        self.github_api_cache.invoke_target  = invoke_target

        with self.github_api_cache as _:
            assert _.cache_entries() == []

            github_api = GitHub__API()
            user_1 = github_api.user(user_name=user_name_requested)
            user_2 = github_api.user(user_name=user_name_requested)
            user_3 = github_api.user(user_name=user_name_requested)
            assert type(user_1) is NamedUser
            assert type(user_2) is NamedUser
            assert type(user_3) is NamedUser
            assert user_1.login == user_name_returned
            assert user_2.login == user_name_returned
            assert user_3.login == user_name_returned

            # assert _.cache_entries() == [{'cache_hits'    : 0       ,
            #                               'comments'      : ''      ,
            #                               'id'            : 1       ,
            #                               'latest'        : 0       ,
            #                               'request_data'  : f'{{\n    "verb": "GET",\n    "url": "/users/{user_name_requested}"\n}}',
            #                               'request_hash'  : '93577d5fe0aff8d6baa8d7826a064bed612f175c6cc5e6af1dd05349de01abd0',
            #                               'response_bytes': b'\x80\x04\x95"\x00\x00\x00\x00\x00\x00\x00K\xc8}\x94\x8c'
            #                                                 b'\x18{\n    "login": "BBBBB"\n}\x94\x87\x94.',
            #                               'response_data' : ''      ,
            #                               'response_hash' : ''      ,
            #                               'timestamp'     : 0       }]

            if in_github_action():                                          # when running this locally we hit on GitHub's '403: rate limit exceeded'
                with self.assertRaises(UnknownObjectException) as context:
                    with Stdout() as stdout:
                        self.github_api_cache.print_requests = True
                        self.github_api_cache.invoke_target = original_invoke_target
                        github_api.user(user_name='ccccc_12344566')                         # call to get data from non-existent user

                assert context.exception.args[0] == 404
                assert context.exception.args[1] == {'documentation_url': 'https://docs.github.com/rest/users/users#get-a-user',
                                                     'message': 'Not Found'}
                assert stdout.value()            == ('# call to : GET /users/ccccc_12344566\n'
                                                     '> http call to : GET /users/ccccc_12344566\n')