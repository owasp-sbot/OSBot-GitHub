from dotenv import load_dotenv
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests

SQLITE_DB_NAME__GIT_HUB_API_CACHE = 'github_api_cache'
SQLITE_TABLE__BEDROCK_REQUESTS    = 'github_api_requests'

class GitHub__API__Cache(Sqlite__Cache__Requests):
    db_name: str
    table_name: str

    def __init__(self, db_path=None):
        load_dotenv()
        self.db_name    = SQLITE_DB_NAME__GIT_HUB_API_CACHE
        self.table_name = SQLITE_TABLE__BEDROCK_REQUESTS
        super().__init__(db_path=db_path, db_name=self.db_name, table_name=self.table_name)
