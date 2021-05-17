# :pencil: gspreadDB 
![Python version >= 3.6](https://img.shields.io/badge/python-%E2%89%A53.6-blue) [![GitHub Actions tests badge](https://github.com/Ycmelon/gspreadDB/actions/workflows/tests.yml/badge.svg)](https://github.com/Ycmelon/gspreadDB/actions/workflows/tests.yml) [![Coverage Status](https://coveralls.io/repos/github/Ycmelon/gspreadDB/badge.svg?branch=main)](https://coveralls.io/github/Ycmelon/gspreadDB?branch=main) [![GitHub license](https://img.shields.io/github/license/Ycmelon/gspreaddb)](https://github.com/Ycmelon/gspreadDB/blob/main/LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple key-value store built on Google Sheets (gspread) with a `dict`-like interface

## :warning: Warning

See: [The `pickle` module is not secure. (from Python docs)](https://docs.python.org/3/library/pickle.html)

This module is a proof of concept and very slow & inefficient, I do not recommend using it!

## :book: Example

```python
import gspread
from gspreaddb import GspreadDB

gc = gspread.service_account()  # https://docs.gspread.org/en/latest/oauth2.html
db = GspreadDB(gc.open("Untitled spreadsheet").sheet1)

db["any_picklable_object"] = "any_picklable_object"
print(db["any_picklable_object"])  # any_picklable_object

for key, value in db.items():
    print(key, value)  # any_picklable_object any_picklable_object

print(len(db))  # 1
```

## :trophy: Credits

- Inspiration from [sqlitedict](https://github.com/RaRe-Technologies/sqlitedict)

## :page_with_curl: License

[GNU General Public License v3.0](https://github.com/Ycmelon/gspreadDB/blob/main/LICENSE)
