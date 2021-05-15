import gspread
import codecs
import pickle


def encode(obj):
    return codecs.encode(pickle.dumps(obj), "base64").decode()


def decode(obj):
    return pickle.loads(codecs.decode(obj.encode(), "base64"))


class GspreadDB(dict):
    def __init__(
        self, worksheet: gspread.models.Worksheet, encode=encode, decode=decode
    ):
        self.worksheet = worksheet
        self.encode = encode
        self.decode = decode

    def clear(self):
        self.worksheet.clear()

    def copy(self) -> dict:
        return dict(self.items())

    def popitem(self):
        index = len(self)
        if index == 0:
            raise KeyError
        item = tuple(self.worksheet.row_values(index))
        self.worksheet.delete_row(index)
        return item

    def setdefault(self, key, default):
        if self.__contains__(key):
            return self.__getitem__(key)

        self.__setitem__(key, default)
        return default

    def update(self, items, **kwargs):
        try:
            items.keys()  # Check for keys method
            for key in items:
                self.__setitem__(key, items[key])
        except AttributeError:
            for key, value in items:
                self.__setitem__(key, value)

        for key in kwargs:
            self.__setitem__(key, kwargs[key])

    def keys(self):
        return map(decode, self.worksheet.col_values(1))

    def values(self):
        return map(decode, self.worksheet.col_values(2))

    def items(self):
        items = self.worksheet.get_all_values()
        for key, value in items:
            yield self.decode(key), self.decode(value)

    def __len__(self):
        return len(self.worksheet.get_all_values())

    def __getitem__(self, key):
        try:
            row = self.worksheet.find(self.encode(key), in_column=1).row
            return self.decode(self.worksheet.cell(row, 2).value)
        except gspread.models.CellNotFound:
            raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        try:
            row = self.worksheet.find(self.encode(key), in_column=1).row
            self.worksheet.update_cell(row, 2, self.encode(value))
        except gspread.models.CellNotFound:  # Insert new
            self.worksheet.append_row([self.encode(key), self.encode(value)])

    def __delitem__(self, key):
        try:
            row = self.worksheet.find(self.encode(key), in_column=1).row
            self.worksheet.delete_rows(row)
        except gspread.models.CellNotFound:
            raise KeyError(key)

    def __iter__(self):
        return self.keys()

    def __str__(self):
        return str(dict(self.items()))

    def __repr__(self):
        return str(self)

    def __contains__(self, key):
        try:
            self.worksheet.find(self.encode(key), in_column=1)
            return True
        except gspread.models.CellNotFound:
            return False
