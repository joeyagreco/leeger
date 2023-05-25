from dataclasses import dataclass
import unittest

from leeger.util.equality import equals
from unittest.mock import patch

# helper stuff


@dataclass
class Foo:
    field1: str
    field2: int
    idField1: str

    def toJson(self):
        return {"field1": self.field1, "field2": self.field2, "idField1": self.idField1}


class TestEquality(unittest.TestCase):
    @patch("leeger.util.CustomLogger.CustomLogger.getLogger")
    def test_equals_happyPath(self, mockGetLogger):
        mockLogger = mockGetLogger.return_value

        # basic equal object
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id")

        result = equals(
            objA=objA, objB=objB, baseFields={"field1", "field2"}, idFields={"idField1"}
        )

        self.assertTrue(result)
        mockLogger.info.assert_not_called()

        # basic unequal object
        objA = Foo("a", 1, "id")
        objB = Foo("b", 1, "id")

        result = equals(
            objA=objA, objB=objB, baseFields={"field1", "field2"}, idFields={"idField1"}
        )

        self.assertFalse(result)
        mockLogger.info.assert_not_called()

        # basic equal object when ignoring id fields
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id2")
        mockLogger.info.assert_not_called()

        result = equals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2"},
            idFields={"idField1"},
            ignoreIdFields=True,
        )

        self.assertTrue(result)

        # basic unequal object when not ignoring id fields
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id2")
        mockLogger.info.assert_not_called()

        result = equals(
            objA=objA, objB=objB, baseFields={"field1", "field2"}, idFields={"idField1"}
        )

        self.assertFalse(result)

        # basic unequal object logging differences
        objA = Foo("a", 1, "id")
        objB = Foo("b", 1, "id")

        result = equals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2"},
            idFields={"idField1"},
            logDifferences=True,
        )

        self.assertFalse(result)
        mockLogger.info.assert_called_once_with("Differences: [('field1', ('a', 'b'))]")
        mockLogger.reset_mock()

        # basic unequal object logging differences with parent key
        objA = Foo("a", 1, "id")
        objB = Foo("b", 1, "id")

        result = equals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2"},
            idFields={"idField1"},
            logDifferences=True,
            parentKey="Foo",
        )

        self.assertFalse(result)
        mockLogger.info.assert_called_once_with("Differences: [('Foo.field1', ('a', 'b'))]")
        mockLogger.reset_mock()

        # basic unequal object logging differences with json method name
        objA = Foo("a", 1, "id")
        objB = Foo("b", 1, "id")

        result = equals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2"},
            idFields={"idField1"},
            logDifferences=True,
            toJsonMethodName="toJson",
        )

        self.assertFalse(result)
        mockLogger.info.assert_called_once_with("Differences: [('field1', ('a', 'b'))]")
        mockLogger.reset_mock()
