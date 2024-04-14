from unittest import TestCase

from osbot_github.api.cache.GitHub__API__Cache import GitHub__API__Cache


class TestCase__GitHub__API(TestCase):
    github_api_cache : GitHub__API__Cache

    @classmethod
    def setUpClass(cls):
        cls.github_api_cache = GitHub__API__Cache().patch_apply()

    @classmethod
    def tearDownClass(cls):
        cls.github_api_cache.patch_restore()