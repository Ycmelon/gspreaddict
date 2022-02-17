import sys
import codecs
import pickle

import gspread


def encode(obj):
    return codecs.encode(pickle.dumps(obj), "base64").decode()


def decode(obj):
    return pickle.loads(codecs.decode(obj.encode(), "base64"))


class GspreadDB(dict):
    def __init__(self, worksheet: gspread.Worksheet, encode=encode, decode=decode):
        self.worksheet = worksheet
        self.encode = encode
        self.decode = decode

    def clear(self):
        self.worksheet.clear()

    def copy(self) -> dict:
        return dict(self)

    def popitem(self):
        index = len(self)
        if index == 0:
            raise KeyError
        item = tuple(map(self.decode, self.worksheet.row_values(index)))
        self.worksheet.delete_rows(index)
        return item

    def setdefault(self, key, default):
        if key in self:
            return self[key]

        self[key] = default
        return default

    def update(self, items=None, **kwargs):
        if items != None:
            try:
                items.keys()  # Check for keys method
                for key in items:
                    self[key] = items[key]
            except AttributeError:
                for key, value in items:
                    self[key] = value

        for key in kwargs:
            self[key] = kwargs[key]

    def keys(self):  # TODO dict views
        return map(decode, self.worksheet.col_values(1))

    def values(self):  # TODO dict views
        return map(decode, self.worksheet.col_values(2))

    def items(self):  # TODO dict views
        items = self.worksheet.get_all_values()
        for key, value in items:
            yield self.decode(key), self.decode(value)

    def __len__(self):
        return len(self.worksheet.get_all_values())

    def __getitem__(self, key):
        cell = self.worksheet.find(self.encode(key), in_column=1)
        if cell:
            return self.decode(self.worksheet.cell(cell.row, 2).value)
        else:
            raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        cell = self.worksheet.find(self.encode(key), in_column=1)

        if cell:
            self.worksheet.update_cell(cell.row, 2, self.encode(value))
        else:
            self.worksheet.append_row([self.encode(key), self.encode(value)])

    def __delitem__(self, key):
        cell = self.worksheet.find(self.encode(key), in_column=1)

        if cell:
            self.worksheet.delete_rows(cell.row)
        else:
            raise KeyError(key)

    def __iter__(self):
        return self.keys()

    if sys.version_info >= (3, 8):

        def __reversed__(self):
            return reversed(list(self.keys()))  # TODO dict views

    def __str__(self):
        return str(dict(self))

    if sys.version_info >= (3, 9):

        def __class_getitem__(cls, item):
            return f"{cls.__name__}[{item.__name__}]"

        def __or__(self, items):  # | (merge)
            return dict(self) | items

        def __ior__(self, items):  # |= (update)
            self.update(items)
            return self

    def __repr__(self):
        return str(self)

    def __contains__(self, key):
        return self.worksheet.find(self.encode(key), in_column=1) != None

    def __eq__(self, o: object) -> bool:
        return dict(self) == o
