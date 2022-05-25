import unittest

from src.leeger.model.abstract.UniqueId import UniqueId


class TestUniqueId(unittest.TestCase):

    def test_uniqueId_newIdForEveryInstance(self):
        uniqueId1 = UniqueId()
        uniqueId2 = UniqueId()

        self.assertIsNotNone(uniqueId1)
        self.assertIsNotNone(uniqueId2)
        self.assertNotEqual(uniqueId1, uniqueId2)
        self.assertIsInstance(uniqueId1.id, str)

    def test_uniqueId_idGetter(self):
        uniqueId = UniqueId()
        id = uniqueId.id

        self.assertIsNotNone(id)

    def test_uniqueId_idSetter(self):
        uniqueId = UniqueId()

        with self.assertRaises(Exception) as e:
            uniqueId.id = "something"
        self.assertEqual("ID cannot be set.", str(e.exception))

    def test_uniqueId_idDeleter(self):
        uniqueId = UniqueId()

        with self.assertRaises(Exception) as e:
            del uniqueId.id
        self.assertEqual("ID cannot be deleted.", str(e.exception))
