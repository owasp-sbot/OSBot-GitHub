import sys
import types

from dotenv                                                     import load_dotenv
from github.Requester import Requester

from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info

SQLITE_DB_NAME__GIT_HUB_API_CACHE = 'github_api_cache.sqlite'
SQLITE_TABLE__BEDROCK_REQUESTS    = 'github_api_requests'

class Sqlite__Cache__Requests__Patch(Sqlite__Cache__Requests):
    db_name             : str
    table_name          : str
    pickle_response     : bool  = True
    target_function     : types.FunctionType
    target_class        : type
    target_function_name: str
    print_requests      : bool  = False

    def __init__(self, db_path=None):
        super().__init__(db_path=db_path, db_name=self.db_name, table_name=self.table_name)

    def invoke_target(self, target, target_kwargs):
        args = target_kwargs.get('args')
        if self.print_requests:
            patched_self, cnx, verb, url, requestHeaders, input = args
            print(f'> http call to : {verb} {url}')
        return target(*args)

    def patched_requestRaw(self, *args):
        request_data = self.request_data(*args)

        target_kwargs = {'args': args}
        invoke_kwargs = dict(target=self.target_function,
                             target_kwargs=target_kwargs,
                             request_data=request_data)

        return self.invoke_with_cache(**invoke_kwargs)

    def patch_apply(self):
        def proxy(*args):
            return self.patched_requestRaw(*args)

        setattr(self.target_class, self.target_function_name, proxy)
        return self

    def patch_restore(self):
        setattr(self.target_class, self.target_function_name, self.target_function)

    def request_data(self, *args, **kwargs):
        patched_self, cnx, verb, url, requestHeaders, input = args
        request_data = {'verb': verb, 'url': url}
        if self.print_requests:
            print(f'# call to : {verb} {url}')
        return request_data

        #return kwargs

class GitHub__API__Cache(Sqlite__Cache__Requests__Patch):
    db_name             : str                = SQLITE_DB_NAME__GIT_HUB_API_CACHE
    table_name          : str                = SQLITE_TABLE__BEDROCK_REQUESTS

    def __init__(self, db_path=None):
        self.target_function      = Requester._Requester__requestRaw
        self.target_class         = Requester
        self.target_function_name = "_Requester__requestRaw"
        super().__init__(db_path=db_path)




