import os
import json
import unittest

import gspreaddb
import gspread

SERVICE_ACCOUNT_CREDENTIALS = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")
assert SERVICE_ACCOUNT_CREDENTIALS is not None
credentials = json.loads(SERVICE_ACCOUNT_CREDENTIALS)


class GspreadDBTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gc = gspread.service_account_from_dict(credentials)
        sheet = gc.open("gspreaddict").sheet1
        assert sheet is not None
        self.dict = gspreaddb.GspreadDB(sheet)
        self.dict.clear()

    def test_str_repr(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertEqual(str(self.dict), str({"key1": "value1", "key2": "value2"}))
        self.assertEqual(repr(self.dict), str({"key1": "value1", "key2": "value2"}))

    def test_len(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertEqual(len(self.dict), 2)

        self.dict["key3"] = "value3"
        self.assertEqual(len(self.dict), 3)

    def test_bool(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertTrue(bool(self.dict))

        self.dict.clear()
        self.assertFalse(bool(self.dict))

    def test_keys(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertEqual(list(self.dict.keys()), ["key1", "key2"])

    def test_values(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertEqual(list(self.dict.values()), ["value1", "value2"])

    def test_items(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertEqual(
            list(self.dict.items()), [("key1", "value1"), ("key2", "value2")]
        )

    def test_contains(self):
        self.dict.clear()
        self.dict["key"] = "value"
        self.assertIn("key", self.dict)

    def test_set_get_update(self):
        self.dict.clear()
        self.dict["key"] = "value"
        self.assertEqual(self.dict["key"], "value")

        self.dict["key"] = "new_value"
        self.assertEqual(self.dict["key"], "new_value")

    def test_clear(self):
        self.dict.clear()
        self.dict["key1"] = "value1"
        self.dict["key2"] = "value2"
        self.assertEqual(len(self.dict), 2)

        self.dict.clear()
        self.assertEqual(len(self.dict), 0)

    def test_del(self):
        self.dict["key"] = "value"
        del self.dict["key"]

        with self.assertRaises(KeyError):
            self.dict["key"]


class KeyTypeTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gc = gspread.service_account_from_dict(credentials)
        sheet = gc.open("gspreaddict").sheet1
        assert sheet is not None
        self.dict = gspreaddb.GspreadDB(sheet)
        self.dict.clear()

    def test_list_tuple(self):
        self.dict.clear()
        key1 = ["key1.1", "key1.2"]
        key1_copy = key1.copy()
        self.dict[key1] = "value1"

        self.assertEqual(self.dict[key1], "value1")
        self.assertEqual(self.dict[key1_copy], "value1")

        key2 = ("key1.1", "key1.2")
        key2_copy = key1.copy()
        self.dict[key1] = "value1"

        self.assertEqual(self.dict[key1], "value1")
        self.assertEqual(self.dict[key1_copy], "value1")

    def test_int_float(self):
        self.dict.clear()
        self.dict[1] = "value1"
        self.assertEqual(self.dict[1], "value1")

        self.dict[1.0] = "value2"
        self.assertEqual(self.dict[1.0], "value2")


if __name__ == "__main__":
    unittest.main()
