import unittest

from wingman.util.indexedrecord import IndexedRecord


class Fruit(IndexedRecord):
    _indexed_attrs = ['first_letter', 'name']

    _create_from_attr = {
        'name': lambda n: Fruit(n)
    }

    def __init__(self, name):
        if len(name) > 0:
            self.first_letter = name[0]
        else:
            self.first_letter = None
        self.name = name
        super().__init__()


class TestIndexedRecord(unittest.TestCase):
    def test_get_by_attr(self):
        name = 'grape'
        record = Fruit(name)
        self.assertEqual(record, Fruit._get_by_attr('name', name))
        self.assertEqual(record, Fruit._get_by_attr('first_letter', name[0]))

    def test_get_invalid_attribute_name(self):
        with self.assertRaises(ValueError):
            Fruit._get_by_attr('weight', 47)

    def test_get_attribute_value_none(self):
        with self.assertRaises(ValueError):
            Fruit._get_by_attr('name', None)

    def test_get_attribute_value_nonexistent(self):
        with self.assertRaises(KeyError):
            Fruit._get_by_attr('name', 'cheesecake')

    def test_create_from_attr(self):
        pear = Fruit._get_by_attr('name', 'pear', create_if_absent=True)
        self.assertIsNotNone(pear)

    def test_create_conflicting_name(self):
        name = 'banana'
        with self.assertRaises(ValueError):
            Fruit(name)
            Fruit(name)

    def test_create_conflicting_first_letter(self):
        with self.assertRaises(ValueError):
            Fruit('apple')
            Fruit('apricot')
    
    def test_alias(self):
        tangerine = Fruit('tangerine')
        Fruit._set_by_attr('name', 'clementine', tangerine)
        self.assertEqual(tangerine, Fruit._get_by_attr('name', 'clementine'))

    def test_create_attr_value_none(self):
        empty = Fruit('')

