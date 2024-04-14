import types

from dotenv                                                     import load_dotenv
from github.Requester import Requester

from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests

SQLITE_DB_NAME__GIT_HUB_API_CACHE = 'github_api_cache.sqlite'
SQLITE_TABLE__BEDROCK_REQUESTS    = 'github_api_requests'

class Sqlite__Cache__Requests__Patch(Sqlite__Cache__Requests):
    db_name             : str
    table_name          : str
    pickle_response     : bool  = True
    function_to_patch   : types.FunctionType
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
        patched_self, cnx, verb, url, requestHeaders, input = args
        request_data = {'verb': verb, 'url': url}
        target_kwargs = {'args': args}
        invoke_kwargs = dict(target=self.function_to_patch,
                             target_kwargs=target_kwargs,
                             request_data=request_data)
        if self.print_requests:
            print(f'# call to : {verb} {url}')
        return self.invoke_with_cache(**invoke_kwargs)

class GitHub__API__Cache(Sqlite__Cache__Requests__Patch):
    db_name             : str                = SQLITE_DB_NAME__GIT_HUB_API_CACHE
    table_name          : str                = SQLITE_TABLE__BEDROCK_REQUESTS

    def __init__(self, db_path=None):
        self.function_to_patch = Requester._Requester__requestRaw
        super().__init__(db_path=db_path)

    def patch_apply(self):
        def proxy(*args):
            return self.patched_requestRaw(*args)
        Requester._Requester__requestRaw = proxy
        return self

    def patch_restore(self):
        Requester._Requester__requestRaw = self.function_to_patch



