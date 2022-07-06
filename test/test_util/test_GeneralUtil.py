import unittest

from src.leeger.util.GeneralUtil import GeneralUtil


class TestGeneralUtil(unittest.TestCase):
    def test_filter_None(self):
        l = [None, "test", None]
        response = GeneralUtil.filter(value=None, list_=l)
        self.assertEqual(["test"], response)

    def test_filter_emptyList(self):
        l = list()
        response = GeneralUtil.filter(value=None, list_=l)
        self.assertEqual([], response)
