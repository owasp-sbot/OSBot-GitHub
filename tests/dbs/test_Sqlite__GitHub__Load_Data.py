from osbot_github.api.cache.TestCase__GitHub__API import TestCase__GitHub__API
from osbot_github.dbs.Sqlite__GitHub__Load_Data import Sqlite__GitHub__Load_Data


class test_Sqlite__GitHub__Load_Data(TestCase__GitHub__API):
    load_data : Sqlite__GitHub__Load_Data

    @classmethod
    def setUpClass(cls):
        cls.load_data = Sqlite__GitHub__Load_Data

