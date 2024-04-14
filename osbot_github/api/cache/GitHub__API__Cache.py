import types

from dotenv                                                     import load_dotenv
from github.Requester import Requester

from osbot_github.api.GitHub__API                               import GitHub__API
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.utils.Dev import pprint

SQLITE_DB_NAME__GIT_HUB_API_CACHE = 'github_api_cache.sqlite'
SQLITE_TABLE__BEDROCK_REQUESTS    = 'github_api_requests'

class GitHub__API__Cache(Sqlite__Cache__Requests, GitHub__API):
    db_name             : str   = SQLITE_DB_NAME__GIT_HUB_API_CACHE
    table_name          : str   = SQLITE_TABLE__BEDROCK_REQUESTS
    pickle_response     : bool  = True
    original_requestRaw : types.FunctionType

    def __init__(self, db_path=None):
        #self.disable()
        load_dotenv()
        super().__init__(db_path=db_path, db_name=self.db_name, table_name=self.table_name)
        GitHub__API.__init__(self)

    def invoke_target(self, target, target_kwargs):
        #print('******* > invoking target')
        args = target_kwargs.get('args')
        return target(*args)

    def patch_apply(self):
        def patched_requestRaw(*args):
            patched_self, cnx, verb, url, requestHeaders, input = args
            request_data  = {'verb': verb, 'url': url}
            target_kwargs = {'args': args}
            invoke_kwargs = dict(target        = self.original_requestRaw,
                                 target_kwargs = target_kwargs           ,
                                 request_data  = request_data            )
            response = self.invoke_with_cache(**invoke_kwargs)
            status, responseHeaders, output = response
            #print(f'---> {url}')
            #print(len(output))

            return response

        self.original_requestRaw = Requester._Requester__requestRaw
        Requester._Requester__requestRaw = patched_requestRaw
        return self

    def patch_restore(self):
        Requester._Requester__requestRaw = self.original_requestRaw



