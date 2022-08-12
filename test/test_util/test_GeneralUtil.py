import unittest

from leeger.util.GeneralUtil import GeneralUtil


class TestGeneralUtil(unittest.TestCase):
    def test_filter_None(self):
        l = [None, "test", None]
        response = GeneralUtil.filter(value=None, list_=l)
        self.assertEqual(["test"], response)

    def test_filter_emptyList(self):
        l = list()
        response = GeneralUtil.filter(value=None, list_=l)
        self.assertEqual([], response)

    def test_warnForUnusedKwargs_happyPath(self):
        kwargs = {"a": 1, "b": 2}
        with self.assertLogs() as captured:
            GeneralUtil.warnForUnusedKwargs(kwargs)
        self.assertEqual(2, len(captured.records))
        self.assertEqual("Keyword argument 'a' unused.", captured.records[0].getMessage())
        self.assertEqual("Keyword argument 'b' unused.", captured.records[1].getMessage())
