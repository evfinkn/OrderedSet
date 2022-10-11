import collections
import collections.abc


class OrderedSet(collections.abc.MutableSet):

    def __init__(self, iterable=()):
        self.odict = collections.OrderedDict.fromkeys(iterable)

    def __contains__(self, elem):
        return elem in self.odict

    def __iter__(self):
        return iter(self.odict.keys())

    def __len__(self):
        return len(self.odict)

    def __str__(self):
        return "{" + str(list(self.odict.keys()))[1:-1] + "}"

    def __repr__(self):
        return f"OrderedSet({list(self.odict.keys())})"

    def add(self, elem):
        self.odict[elem] = None

    def discard(self, elem):
        self.odict.pop(elem, None)  # second arg None prevent KeyError if not in dict

    def popitem(self, last=True):
        return self.odict.popitem(last)[0]

    def move_to_end(self, elem, last=True):
        self.odict.move_to_end(elem, last)
