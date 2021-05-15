# gspreadDB [![GitHub Actions tests badge](https://github.com/Ycmelon/gspreadDB/actions/workflows/tests.yml/badge.svg)](https://github.com/Ycmelon/gspreadDB/actions/workflows/tests.yml) [![GitHub license](https://img.shields.io/github/license/Ycmelon/gspreaddb)](https://github.com/Ycmelon/gspreadDB/blob/main/LICENSE)

A simple key-value store built on Google Sheets (gspread) with a `dict`-like interface

## :warning: Warning

See: [The `pickle` module is not secure. (from Python docs)](https://docs.python.org/3/library/pickle.html)

This module is a proof of concept and very inefficient, I do not recommend using it!

## :book: Example

```python
import gspread
from gspreaddb import GspreadDB

gc = gspread.service_account()  # https://docs.gspread.org/en/latest/oauth2.html
mydict = GspreadDB(gc.open("Untitled spreadsheet").sheet1)

mydict["any_picklable_object"] = "any_picklable_object"
print(mydict["any_picklable_object"])  # any_picklable_object

for key, value in mydict.items():
    print(key, value)  # any_picklable_object any_picklable_object

print(len(mydict))  # 1
```

## :trophy: Credits

- Inspiration from [sqlitedict](https://github.com/RaRe-Technologies/sqlitedict)

## :page_with_curl: License

[GNU General Public License v3.0](https://github.com/Ycmelon/gspreadDB/blob/main/LICENSE)
