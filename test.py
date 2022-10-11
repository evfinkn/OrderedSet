from OrderedSet import OrderedSet
import unittest


class TestOrderedSet(unittest.TestCase):

    EMPTY_OSET = OrderedSet()
    ELEMENTS = [1, 4.76, 3, "y", 7, 11, "a", 9, 60, (1,)]

    def add_helper(self, *elements):
        for element in elements:
            self.oset.add(element)

    def discard_helper(self, *elements):
        for element in elements:
            self.oset.discard(element)

    def popitem_helper(self, num_elements, last=True, *expected):
        popped = []
        for _ in range(num_elements):
            popped.append(self.oset.popitem(last))
        if len(expected) != 0:
            self.assertEqual(expected, tuple(popped), "popping from oset")

    def move_to_end_helper(self, last=True, *elements):
        for element in elements:
            self.oset.move_to_end(element, last)

    def setUp(self):
        self.oset = OrderedSet(self.ELEMENTS)

    def test_contains(self):
        self.assertIn("a", self.oset, "\"a\" in oset")
        self.assertIn((1,), self.oset, "1 in oset")

        self.assertNotIn(4, self.oset, "4 not in oset")
        self.assertNotIn(0, self.EMPTY_OSET, "0 not in EMPTY_SET")

    def test_iter(self):
        # list calls __iter__, so easier to compare as list which __iter__ must work for
        self.assertEqual([], list(self.EMPTY_OSET), "iter of EMPTY_SET")
        self.assertEqual(self.ELEMENTS, list(self.oset), "oset iter before popping and adding")

        self.popitem_helper(5, False)  # {11, "a", 9, 60, (1,)}
        self.popitem_helper(2)  # {11, "a", 9}
        self.add_helper("b", ())  # {11, "a", 9, "b", ()}
        self.assertEqual([11, "a", 9, "b", ()], list(self.oset), "oset iter after popping and adding")

    def test_len(self):
        self.assertEqual(0, len(self.EMPTY_OSET), "length of EMPTY_SET")
        self.assertEqual(len(self.ELEMENTS), len(self.oset), "length of oset before removing all elements")

        self.popitem_helper(len(self.ELEMENTS))  # {}
        self.assertEqual(0, len(self.oset), "length of oset after removing all elements")

    def test_str(self):
        self.assertEqual("{}", str(self.EMPTY_OSET), "str of EMPTY_SET")
        self.assertEqual(f"{{{str(self.ELEMENTS)[1:-1]}}}", str(self.oset), "str of oset")

    def test_repr(self):
        self.assertEqual("OrderedSet([])", repr(self.EMPTY_OSET), "repr of empty OrderedSet")
        self.assertEqual(f"OrderedSet({self.ELEMENTS})", repr(self.oset), "repr of oset")

    def test_add(self):
        self.add_helper(0, 1, "y")  # {1, 4.76, 3, "y", 7, 11, "a", 9, 60, (1,), 0}
        self.assertEqual([1, 4.76, 3, "y", 7, 11, "a", 9, 60, (1,), 0], list(self.oset), "adding to oset")

        self.discard_helper(3, "a", 9, 60, (1,), 0)  # {1, 4.76, "y", 7, 11}
        self.add_helper(8, 6, "a")  # {1, 4.76, "y", 7, 11, 8, 6, "a"}
        self.assertEqual([1, 4.76, "y", 7, 11, 8, 6, "a"], list(self.oset), "discarding then adding to oset")

    def test_discard(self):
        self.discard_helper(1, 7, 11, 9, (1,))  # {4.76, 3, "y", "a", 60}
        self.assertEqual([4.76, 3, "y", "a", 60], list(self.oset), "discarding from oset")

        self.add_helper(3, 9, "string")  # {4.76, 3, "y", "a", 60, 9, "string"}
        self.discard_helper(4.76, 3)  # {"y", "a", 60, 9, "string"}
        self.assertEqual(["y", "a", 60, 9, "string"], list(self.oset), "adding then discarding from oset")

        self.discard_helper("string", *self.ELEMENTS)  # {}
        self.assertEqual([], list(self.oset), "discarding everything")

    def test_popitem(self):
        with self.assertRaises(KeyError, msg="popitem on EMPTY_SET"):
            self.EMPTY_OSET.popitem()

        self.popitem_helper(5, True, (1,), 60, 9, "a", 11)  # {1, 4.76, 3, "y", 7}
        self.assertEqual([1, 4.76, 3, "y", 7], list(self.oset), "popping from oset")

        self.add_helper("string", 20)  # {1, 4.76, 3, "y", 7, "string", 20}
        self.move_to_end_helper(True, 4.76)  # {1, 3, "y", 7, "string", 20, 4.76}
        self.popitem_helper(3, False, 1, 3, "y")  # {7, "string", 20, 4.76}
        self.assertEqual([7, "string", 20, 4.76], list(self.oset), "popping from oset after adding and moving")

    def test_move_to_end(self):
        with self.assertRaises(KeyError, msg="move_to_end on EMPTY_SET"):
            self.EMPTY_OSET.move_to_end(0)

        self.move_to_end_helper(False, (1,), 3, 11)  # {11, 3, (1,), 1, 4.76, "y", 7, "a", 9, 60}
        self.assertEqual([11, 3, (1,), 1, 4.76, "y", 7, "a", 9, 60], list(self.oset), "moving to beginning of oset")

        self.popitem_helper(2, False)  # {(1,), 1, 4.76, "y", 7, "a", 9, 60}
        self.move_to_end_helper(True, 4.76, "a")  # {(1,), 1, "y", 7, 9, 60, 4.76, "a"}
        self.assertEqual([(1,), 1, "y", 7, 9, 60, 4.76, "a"], list(self.oset), "moving to end after popping from oset")


if __name__ == "__main__":
    unittest.main()
