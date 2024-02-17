# gspreaddict ![Python version >= 3.6](https://img.shields.io/badge/python-%E2%89%A53.6-blue) [![GitHub Actions tests badge](https://github.com/Ycmelon/gspreadDB/actions/workflows/tests.yml/badge.svg)](https://github.com/Ycmelon/gspreadDB/actions/workflows/tests.yml) [![Coverage Status](https://coveralls.io/repos/github/Ycmelon/gspreadDB/badge.svg?branch=main)](https://coveralls.io/github/Ycmelon/gspreadDB?branch=main)

A persistent `dict` wrapper around Google Sheets using gspread

```python
import gspread
from gspreaddict import GspreadDict

gc = gspread.service_account()  # https://docs.gspread.org/en/latest/oauth2.html
db = GspreadDict(gc.open("My spreadsheet").sheet1)

# Keys can be str, and values can be str | None
db["colour"] = "blue"
db["shape"] = "triangle"
db["size"] = "large"
print(db["shape"])  # -> triangle

for key, value in db.items():
    print(key, value)  # colour blue, shape triangle, size large

print(len(db))  # 3
```

## Credits

- Inspiration from [sqlitedict](https://github.com/RaRe-Technologies/sqlitedict)

## License

[GNU General Public License v3.0](LICENSE)
