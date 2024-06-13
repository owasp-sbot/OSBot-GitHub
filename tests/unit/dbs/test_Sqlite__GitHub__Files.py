import inspect
from unittest import TestCase

from osbot_github.api.GitHub__Repo import GitHub__Repo
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database

from osbot_github.api.GitHub__API                   import GitHub__API
from osbot_github.api.cache.TestCase__GitHub__API   import TestCase__GitHub__API
from osbot_github.dbs.Sqlite__GitHub__Files         import Sqlite__GitHub__Files, SQLITE_DB_NAME
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Files import Sqlite__DB__Files
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.trace.Trace_Call import trace_calls
from osbot_utils.utils.Dev                          import pprint
from osbot_utils.utils.Files import parent_folder, current_temp_folder, file_name, temp_file, file_extension
from osbot_utils.utils.Misc                         import list_set
from osbot_utils.utils.Objects                      import obj_methods, obj_data, base_types, type_mro
from tests.unit.api.cache.test_GitHub__API__Cache    import GIT_HUB__REPO__OSBOT_GITHUB


class test_Sqlite__GitHub__Files(TestCase__GitHub__API):
    expected_db_name: str
    github_files    : Sqlite__GitHub__Files
    repo_full_name  : str
    temp_db_path    : str

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repo_full_name   = GIT_HUB__REPO__OSBOT_GITHUB
        cls.temp_db_path     = temp_file(extension='sqlite')
        cls.github_files     = Sqlite__GitHub__Files(repo_full_name=cls.repo_full_name, db_path=cls.temp_db_path)
        cls.github_files.setup()



    @classmethod
    def tearDownClass(cls):
        with cls.github_files as _:
            assert _.deleted  is False                          # check deleted flag
            assert _.delete() is True                           # deleting db should work first time
            assert _.deleted  is True                           # deleted flag should now be set
            assert _.delete() is False                          # deleting db should NOT work second time

    def tearDown(self):
        self.github_files.table_files().clear()

    def test___init__(self):
        #cls.expected_db_name = SQLITE_DB_NAME.format(repo_full_name=cls.repo_full_name)
        with self.github_files as _:
            assert _.exists()               is True
            assert parent_folder (_.db_path) == current_temp_folder()
            assert file_extension(_.db_path) == '.sqlite'
            assert type(_.github_api)       is GitHub__API
            assert _.__locals__() == { 'auto_schema_row': False              ,
                                       'closed'         : False              ,
                                       'connected'      : True               ,
                                       'db_name'        : _.db_name          ,
                                       'db_path'        : _.db_path          ,
                                       'deleted'        : False              ,
                                       'full_name'      : self.repo_full_name,
                                       'github_api'     : _.github_api       ,
                                       'in_memory'      : False              }

            assert type_mro  (_) == [Sqlite__GitHub__Files, Sqlite__DB__Files, Sqlite__DB__Local, Sqlite__Database, GitHub__Repo, Kwargs_To_Self, object]
            assert base_types(_) == [                       Sqlite__DB__Files, GitHub__Repo, Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object, Kwargs_To_Self, object]

            #methods_list = list_set(obj_data(_, show_methods=True, only_show_methods=True))
            # assert methods_list == [ 'close', 'commits', 'config', 'connect', 'connection', 'connection_string', 'cursor',
            #                          'delete', 'deserialize_from_dict', 'dict_factory',
            #                          'exists',
            #                          'file_content', 'file_parsed_content', 'folder_contents', 'folder_files', 'folder_folders', 'folders_and_files', 'from_json',
            #                          'info', 'json',
            #                          'merge_with',
            #                          'parse_raw_content', 'path_db_folder', 'path_local_db', 'path_temp_database', 'path_temp_databases', 'print',
            #                          'raw_contents', 'repo', 'repo_data', 'repo_obj', 'reset',
            #                          'save_to', 'serialize_to_dict', 'setup',
            #                          'table', 'table__sqlite_master', 'table_files', 'tables', 'tables_names', 'tables_raw',
            #                          'update_from_kwargs']

    def test_add_github_files_to_db(self):
        add_all = False
        path    = ''

        with self.github_files as _:
            assert _.files() == []
            rows_added = _.add_github_files_to_db(path=path, add_all=add_all)
            assert len(_.files()) > 0
            assert len(_.files()) == len(rows_added)


    def test_folder_files(self):
        initial_path = '/'
        with self.github_files as _:
            files = _.folder_files(path=initial_path, index_by='path')
            assert list_set(files) == [ '.gitignore'           ,
                                        'LICENSE'              ,
                                        'README.md'            ,
                                        'git-publish-main.sh'  ,
                                        'poetry.lock'          ,
                                        'pyproject.toml'       ,
                                        'requirements-test.txt',
                                        'requirements.txt'     ]
            # return
            # all_items = _.folder_files(path=initial_path)
            # for item in all_items:
            #     print(item.get('path'))

