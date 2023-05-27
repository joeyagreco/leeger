from dataclasses import dataclass
import unittest

from typing import Any, Optional

from leeger.util.equality import modelEquals
from unittest.mock import patch

# helper stuff


@dataclass
class Foo:
    field1: str
    field2: int
    idField1: str
    nestedField: Optional[Any] = None

    def fooEquals(self, otherFoo: Any, *, ignoreIdFields: bool = False) -> bool:
        return modelEquals(
            objA=self,
            objB=otherFoo,
            baseFields={"field1", "field2", "nestedField"},
            idFields={"idField1"},
            parentKey="Foo",
            ignoreIdFields=ignoreIdFields,
        )

    def toJson(self):
        return {"field1": self.field1, "field2": self.field2, "idField1": self.idField1}


class TestEquality(unittest.TestCase):
    @patch("leeger.util.CustomLogger.CustomLogger.getLogger")
    def test_equals(self, mockGetLogger):
        mockLogger = mockGetLogger.return_value

        # basic equal object
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id")

        result = modelEquals(
            objA=objA, objB=objB, baseFields={"field1", "field2"}, idFields={"idField1"}
        )

        self.assertTrue(result)
        mockLogger.info.assert_not_called()

        # basic unequal object
        objA = Foo("a", 1, "id")
        objB = Foo("b", 1, "id")

        result = modelEquals(
            objA=objA, objB=objB, baseFields={"field1", "field2"}, idFields={"idField1"}
        )

        self.assertFalse(result)
        mockLogger.info.assert_not_called()

        # basic equal object when ignoring id fields
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id2")
        mockLogger.info.assert_not_called()

        result = modelEquals(
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

        result = modelEquals(
            objA=objA, objB=objB, baseFields={"field1", "field2"}, idFields={"idField1"}
        )

        self.assertFalse(result)

        # basic unequal object logging differences
        objA = Foo("a", 1, "id")
        objB = Foo("b", 1, "id")

        result = modelEquals(
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

        result = modelEquals(
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

        result = modelEquals(
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

        # basic equal object with equality function map
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id")

        def checkField1(a, b, **kwargs):
            return a == b

        result = modelEquals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2"},
            idFields={"idField1"},
            equalityFunctionMap={"field1": checkField1},
        )

        self.assertTrue(result)
        mockLogger.info.assert_not_called()

        # basic equal object with equality function map with function that makes them unequal
        objA = Foo("a", 1, "id")
        objB = Foo("a", 1, "id")

        def checkField1(a, b, **kwargs):
            return False

        result = modelEquals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2"},
            idFields={"idField1"},
            equalityFunctionMap={"field1": checkField1},
        )

        self.assertFalse(result)
        mockLogger.info.assert_not_called()

        # basic equal object with nested field
        nestedFooA = Foo("b", 2, "id")
        nestedFooB = Foo("b", 2, "id")
        objA = Foo("a", 1, "id", [nestedFooA])
        objB = Foo("a", 1, "id", [nestedFooB])

        def checkNestedField(a, b, **kwargs):
            equals = True
            for curA, curB in zip(a, b):
                equals = equals and curA.fooEquals(curB, **kwargs)
            return equals

        result = modelEquals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2", "nestedField"},
            idFields={"idField1"},
            equalityFunctionMap={"nestedField": checkNestedField},
        )

        self.assertTrue(result)
        mockLogger.info.assert_not_called()

        # basic unequal object with nested field
        nestedFooA = Foo("b", 2, "idwrong")
        nestedFooB = Foo("b", 2, "id")
        objA = Foo("a", 1, "id", [nestedFooA])
        objB = Foo("a", 1, "id", [nestedFooB])

        def checkNestedField(a, b, **kwargs):
            equals = True
            for curA, curB in zip(a, b):
                equals = equals and curA.fooEquals(curB, **kwargs)
            return equals

        result = modelEquals(
            objA=objA,
            objB=objB,
            baseFields={"field1", "field2", "nestedField"},
            idFields={"idField1"},
            equalityFunctionMap={"nestedField": checkNestedField},
        )

        self.assertFalse(result)
        mockLogger.info.assert_not_called()
