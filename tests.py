import os
import sys
import json
import pytest
import time

import gspread
import gspreaddict


min_python38 = pytest.mark.skipif(
    sys.version_info < (3, 8), reason="requires Python 3.8"
)
min_python39 = pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires Python 3.9"
)


@pytest.fixture(autouse=True)
def clear(db: gspreaddict.GspreadDict):
    db.clear()
    time.sleep(5)  # prevent rate-limit


@pytest.fixture(scope="session")
def db():
    try:
        gc = gspread.service_account()  # dev
    except FileNotFoundError:
        SERVICE_ACCOUNT_CREDENTIALS = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")
        if SERVICE_ACCOUNT_CREDENTIALS == None:
            raise RuntimeError("Missing service account credentials")

        credentials = json.loads(SERVICE_ACCOUNT_CREDENTIALS)
        gc = gspread.service_account_from_dict(credentials)

    sheet = gc.open("gspreaddict").sheet1
    if sheet == None:
        raise RuntimeError("Missing sheet")
    db = gspreaddict.GspreadDict(sheet)

    return db


class TestMethods:
    def test_clear(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"
        db["key2"] = "value2"
        assert len(db) == 2

        db.clear()
        assert len(db) == 0

    def test_copy(self, db: gspreaddict.GspreadDict):
        db_copy = db.copy()
        assert db == db_copy
        assert not db is db_copy

    def test_popitem(self, db: gspreaddict.GspreadDict):
        with pytest.raises(KeyError):
            db.popitem()

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert db.popitem() == ("key2", "value2")

    def test_setdefault(self, db: gspreaddict.GspreadDict):
        assert db.setdefault("key", "default") == "default"
        assert db.setdefault("key", "new_value") == "default"

    def test_update(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"

        dict1 = {"key1": "new_value1", "key2": "value2"}
        db.update(dict1)
        assert db["key1"] == "new_value1"
        assert db["key2"] == "value2"

        iter1 = [("key2", "new_value2"), ("key3", "value3")]
        db.update(iter1)
        assert db["key2"] == "new_value2"
        assert db["key3"] == "value3"

        db.update(key3="new_value3", key4="value4")
        assert db["key3"] == "new_value3"
        assert db["key4"] == "value4"

    def test_keys(self, db: gspreaddict.GspreadDict):
        assert list(db.keys()) == []

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert list(db.keys()) == ["key1", "key2"]

    def test_values(self, db: gspreaddict.GspreadDict):
        assert list(db.values()) == []

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert list(db.values()) == ["value1", "value2"]

    def test_items(self, db: gspreaddict.GspreadDict):
        assert list(db.items()) == []

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert list(db.items()) == [("key1", "value1"), ("key2", "value2")]

    def test_len(self, db: gspreaddict.GspreadDict):
        assert len(db) == 0

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert len(db) == 2

        db["key3"] = "value3"
        assert len(db) == 3

    def test_get_set(self, db: gspreaddict.GspreadDict):
        with pytest.raises(KeyError):
            db["key"]

        assert db.get("key", "default") == "default"

        db["key"] = "value"
        assert db["key"] == "value"

        db["key"] = "new_value"
        assert db["key"] == "new_value"

    def test_delete(self, db: gspreaddict.GspreadDict):
        db["key"] = "value"
        del db["key"]

        with pytest.raises(KeyError):
            del db["key"]

    def test_iter(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"
        db["key2"] = "value2"

        keys = []
        for key in db:
            keys.append(key)

        assert keys == ["key1", "key2"]

    @min_python38
    def test_reversed(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"
        db["key2"] = "value2"

        assert list(reversed(db)) == ["key2", "key1"]

    def test_str_repr(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"
        db["key2"] = "value2"
        assert str(db) == str({"key1": "value1", "key2": "value2"})
        assert repr(db) == str({"key1": "value1", "key2": "value2"})

    @min_python39
    def test_class_getmethod(self):
        assert gspreaddict.GspreadDict[int] == "GspreadDict[int]"

    @min_python39
    def test_or(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"
        db["key2"] = "value2"
        dict1 = {"key2": "new_value2", "key3": "value3"}

        assert db | dict1 == {
            "key1": "value1",
            "key2": "new_value2",
            "key3": "value3",
        }

    @min_python39
    def test_ior(self, db: gspreaddict.GspreadDict):
        db["key1"] = "value1"
        db["key2"] = "value2"
        dict1 = {"key2": "new_value2", "key3": "value3"}

        db |= dict1

        assert db == {
            "key1": "value1",
            "key2": "new_value2",
            "key3": "value3",
        }

    def test_contains(self, db: gspreaddict.GspreadDict):
        assert not "key" in db

        db["key"] = "value"
        assert "key" in db

    def test_bool(self, db: gspreaddict.GspreadDict):
        assert not bool(db)

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert bool(db)

        db.clear()
        assert not bool(db)


class TestTypes:
    def test_none(self, db: gspreaddict.GspreadDict):
        db["key1"] = None
        assert db["key1"] == None

        db["key1"] = "value1"
        assert db["key1"] != None
