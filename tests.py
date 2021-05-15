import os
import json
import pytest
import time

import gspreaddb
import gspread


@pytest.fixture(autouse=True)
def clear(db: gspreaddb.GspreadDB):
    db.clear()
    time.sleep(5)  # prevent rate-limit


@pytest.fixture()
def db():
    SERVICE_ACCOUNT_CREDENTIALS = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")
    if SERVICE_ACCOUNT_CREDENTIALS == None:
        raise RuntimeError("Missing service account credentials")

    credentials = json.loads(SERVICE_ACCOUNT_CREDENTIALS)
    gc = gspread.service_account_from_dict(credentials)

    sheet = gc.open("gspreaddict").sheet1
    if sheet == None:
        raise RuntimeError("Missing sheet")
    db = gspreaddb.GspreadDB(sheet)

    return db


class TestMethods:
    def test_clear(self, db: gspreaddb.GspreadDB):
        db["key1"] = "value1"
        db["key2"] = "value2"
        assert len(db) == 2

        db.clear()
        assert len(db) == 0

    def test_copy(self, db: gspreaddb.GspreadDB):
        db_copy = db.copy()
        assert db == db_copy
        assert not db is db_copy

    def test_popitem(self, db: gspreaddb.GspreadDB):
        with pytest.raises(KeyError):
            db.popitem()

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert db.popitem() == ("key2", "value2")

    def test_setdefault(self, db: gspreaddb.GspreadDB):
        assert db.setdefault("key", "default") == "default"
        assert db.setdefault("key", "new_value") == "default"

    def test_update(self, db: gspreaddb.GspreadDB):
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

    def test_keys(self, db: gspreaddb.GspreadDB):
        assert list(db.keys()) == []

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert list(db.keys()) == ["key1", "key2"]

    def test_values(self, db: gspreaddb.GspreadDB):
        assert list(db.values()) == []

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert list(db.values()) == ["value1", "value2"]

    def test_items(self, db: gspreaddb.GspreadDB):
        assert list(db.items()) == []

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert list(db.items()) == [("key1", "value1"), ("key2", "value2")]

    def test_len(self, db: gspreaddb.GspreadDB):
        assert len(db) == 0

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert len(db) == 2

        db["key3"] = "value3"
        assert len(db) == 3

    def test_get_set(self, db: gspreaddb.GspreadDB):
        with pytest.raises(KeyError):
            db["key"]

        assert db.get("key", "default") == "default"

        db["key"] = "value"
        assert db["key"] == "value"

        db["key"] = "new_value"
        assert db["key"] == "new_value"

    def test_delete(self, db: gspreaddb.GspreadDB):
        db["key"] = "value"
        del db["key"]

        with pytest.raises(KeyError):
            del db["key"]

    def test_iter(self, db: gspreaddb.GspreadDB):
        db["key1"] = "value1"
        db["key2"] = "value2"

        keys = []
        for key in db:
            keys.append(key)

        assert keys == ["key1", "key2"]

    def test_str_repr(self, db: gspreaddb.GspreadDB):
        db["key1"] = "value1"
        db["key2"] = "value2"
        assert str(db) == str({"key1": "value1", "key2": "value2"})
        assert repr(db) == str({"key1": "value1", "key2": "value2"})

    def test_contains(self, db: gspreaddb.GspreadDB):
        assert not "key" in db

        db["key"] = "value"
        assert "key" in db

    def test_bool(self, db: gspreaddb.GspreadDB):
        assert not bool(db)

        db["key1"] = "value1"
        db["key2"] = "value2"
        assert bool(db)

        db.clear()
        assert not bool(db)


class TestKeyTypes:
    def test_list_tuple(self, db: gspreaddb.GspreadDB):
        key1 = ["key1.1", "key1.2"]
        key1_copy = key1.copy()
        db[key1] = "value1"

        assert db[key1] == "value1"
        assert db[key1_copy] == "value1"

        key2 = ("key1.1", "key1.2")
        key2_copy = key1.copy()
        db[key2] = "value1"

        assert db[key2] == "value1"
        assert db[key2_copy] == "value1"

    def test_int_float(self, db: gspreaddb.GspreadDB):
        db[1] = "value1"
        assert db[1] == "value1"

        db[1.0] = "value2"
        assert db[1.0] == "value2"
