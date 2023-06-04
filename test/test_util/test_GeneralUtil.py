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
        
        # with exclude keys
        kwargs = {"a": 1, "b": 2}
        with self.assertLogs() as captured:
            GeneralUtil.warnForUnusedKwargs(kwargs, excludeKeys=["a"])
        self.assertEqual(1, len(captured.records))
        self.assertEqual("Keyword argument 'b' unused.", captured.records[0].getMessage())

    def test_safeSum_happyPath(self):
        response = GeneralUtil.safeSum(None, 1, 1)
        self.assertEqual(2, response)

        response = GeneralUtil.safeSum(1, None, 1)
        self.assertEqual(2, response)

        response = GeneralUtil.safeSum(1, 1, None)
        self.assertEqual(2, response)

        response = GeneralUtil.safeSum(None, None, None)
        self.assertIsNone(response)

        response = GeneralUtil.safeSum(1, 1, 1)
        self.assertEqual(3, response)

    def test_findDifferentFields_noDifference_simpleDict(self):
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "baz", "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual(list(), response)

        # with list
        d1 = {"foo": ["baz", "boy"], "bar": "bot"}
        d2 = {"foo": ["baz", "boy"], "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual(list(), response)

        # with tuple
        d1 = {"foo": ("baz", "boy"), "bar": "bot"}
        d2 = {"foo": ("baz", "boy"), "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual(list(), response)

        # with ignore key names (some keys)
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "baz", "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2, ignoreKeyNames=["foo"])
        self.assertEqual(list(), response)

        # with ignore key names (all keys)
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "baz", "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2, ignoreKeyNames=["foo", "bar"])
        self.assertEqual(list(), response)

        # with parent key given
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "baz", "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2, parentKey="abc")
        self.assertEqual(list(), response)

    def test_findDifferentFields_someDifference_simpleDict(self):
        # single field difference
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "ba", "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo", ("baz", "ba"))], response)

        # list differences
        # single field difference with same list length
        d1 = {"foo": ["baz", "bar"]}
        d2 = {"foo": ["baz", "ba"]}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo[1]", ("bar", "ba"))], response)

        # all values in list differ, shows key as difference
        d1 = {"foo": ["baz", "bar", "bot", "boy"]}
        d2 = {"foo": ["ba", "ba", "bo", "bo"]}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual(
            [("foo", (["baz", "bar", "bot", "boy"], ["ba", "ba", "bo", "bo"]))], response
        )

        # lists have unequal length, shows key as difference
        d1 = {"foo": ["baz", "bar"]}
        d2 = {"foo": ["baz"]}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo", (["baz", "bar"], ["baz"]))], response)

        # tuple differences
        # single field difference with same list length
        d1 = {"foo": ("baz", "bar")}
        d2 = {"foo": ("baz", "ba")}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo[1]", ("bar", "ba"))], response)

        # all values in tuples differ, shows key as difference
        d1 = {"foo": ("baz", "bar", "bot", "boy")}
        d2 = {"foo": ("ba", "ba", "bo", "bo")}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual(
            [("foo", (("baz", "bar", "bot", "boy"), ("ba", "ba", "bo", "bo")))], response
        )

        # tuples have unequal length, shows key as difference
        d1 = {"foo": ("baz", "bar")}
        d2 = {"foo": ("baz")}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo", (("baz", "bar"), ("baz")))], response)

        # multiple field differences
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "ba", "bar": "bo"}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo", ("baz", "ba")), ("bar", ("bot", "bo"))], response)

        # difference with ignore key names (some keys)
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "ba", "bar": "bo"}
        response = GeneralUtil.findDifferentFields(d1, d2, ignoreKeyNames=["foo"])
        self.assertEqual([("bar", ("bot", "bo"))], response)

        # difference with ignore key names (all difference keys)
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "ba", "bar": "bo"}
        response = GeneralUtil.findDifferentFields(d1, d2, ignoreKeyNames=["foo", "bar"])
        self.assertEqual(list(), response)

        # with parent key given
        d1 = {"foo": "baz", "bar": "bot"}
        d2 = {"foo": "ba", "bar": "bot"}
        response = GeneralUtil.findDifferentFields(d1, d2, parentKey="abc")
        self.assertEqual([("abc.foo", ("baz", "ba"))], response)

    def test_findDifferentFields_nestedDict(self):
        # with dict nested
        d1 = {"foo": {"baz": "bar"}, "bot": {"boo": "boy"}}
        d2 = {"foo": {"baz": "ba"}, "bot": {"boo": "bo"}}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo.baz", ("bar", "ba")), ("bot.boo", ("boy", "bo"))], response)

        # with list nested
        # same list length, single index difference
        d1 = {"foo": {"bar": ["bot", "boy"]}}
        d2 = {"foo": {"bar": ["bot", "bo"]}}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo.bar[1]", ("boy", "bo"))], response)

        # same list length, all index difference
        d1 = {"foo": {"bar": ["bot", "boy"]}}
        d2 = {"foo": {"bar": ["bo", "bo"]}}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo.bar", (["bot", "boy"], ["bo", "bo"]))], response)

        # same list length, many (not all) index difference
        d1 = {"foo": {"bar": ["bot", "boy", "boz"]}}
        d2 = {"foo": {"bar": ["bo", "bo", "boz"]}}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo.bar[0]", ("bot", "bo")), ("foo.bar[1]", ("boy", "bo"))], response)

        # different list length
        d1 = {"foo": {"bar": ["bot", "boy"]}}
        d2 = {"foo": {"bar": ["bot"]}}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo.bar", (["bot", "boy"], ["bot"]))], response)

        # with ignore key names (some keys)
        d1 = {"foo": {"baz": "bar"}}
        d2 = {"foo": {"baz": "ba"}}
        response = GeneralUtil.findDifferentFields(d1, d2, ignoreKeyNames=["baz"])
        self.assertEqual(list(), response)

        # list with ignore key names
        d1 = {"foo": {"bar": [{"bot": "boy"}]}}
        d2 = {"foo": {"bar": [{"bot": "bo"}]}}
        response = GeneralUtil.findDifferentFields(d1, d2)
        self.assertEqual([("foo.bar[0].bot", ("boy", "bo"))], response)

        # with parent key given
        d1 = {"foo": {"baz": "bar"}, "bot": {"boo": "boy"}}
        d2 = {"foo": {"baz": "ba"}, "bot": {"boo": "bo"}}
        response = GeneralUtil.findDifferentFields(d1, d2, parentKey="abc")
        self.assertEqual([("abc.foo.baz", ("bar", "ba")), ("abc.bot.boo", ("boy", "bo"))], response)
