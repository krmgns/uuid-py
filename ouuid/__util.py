from __future__ import annotations
from datetime import datetime
import re, typing, textwrap

# None holder.
Null = object()

# Get type name, eg: <class 'int'> => int
def typeOf(x, check: bool = False) -> str:
    name = x if check and isTypeOf(x, type) else type(x)
    name = str(name)[8:-2]
    # Drop mid part.
    if 'ouuid.' in name:
        name = re.sub(r'ouuid\.\w+\.(\w+)', r'ouuid.\1', name)
    return name

# Check types, eg: (int, str, ...)
def isTypeOf(x, *types: object) -> bool:
    return isinstance(x, types)


HEXES = '0123456789abcdef'

class listing(list):
    def cut(self, length: int) -> listing:
        if length > 0:
            return listing(self[:length])
        return listing(self[length:])

    def sub(self, start: int, end: int = None) -> listing:
        return listing(self[start:end])

    def pad(self, length: int, value: typing.Any = None) -> listing:
        length, padding = length - len(self), []
        if length > 0:
            padding = [value] * length
        return listing(self + padding)

    def filter(self, func: typing.Callable = None) -> listing:
        return listing(filter(func, self))

    def map(self, func: typing.Callable) -> listing:
        return listing(map(func, self))

    def join(self, glue: str) -> string:
        return string(glue.join(self))

class string(str):
    def cut(self, length: int) -> string:
        if length > 0:
            return string(self[:length])
        return string(self[length:])

    def sub(self, start: int, length: int = None) -> string:
        if length is None:
            return string(self[start:])
        return string(self[start:][:length])

    def drop(self, search: str) -> string:
        return string(self.replace(search, ''))

    def slit(self, num: int, tup: bool = True) -> tuple|listing:
        ret = textwrap.wrap(self, num)
        return tuple(ret) if tup else listing(ret)

    def isHex(self) -> bool:
        for s in self.lower():
            if not s in HEXES:
                return False
        # Prevent empty.
        return len(self) > 0

class dating:
    def utcDate(fmt = None) -> str:
        fmt = fmt or '%Y%m%d'
        return datetime.utcnow().strftime(fmt)

    def utcDateTime(fmt = None) -> str:
        fmt = fmt or '%Y%m%d%H%M%S'
        return datetime.utcnow().strftime(fmt)

    def isValidDate(*args) -> bool:
        y, m, d = map(int, args)
        return (
                y >= 0
            and m >= 1 and m <= 12
            and d >= 1 and d <= 31
        )

    def isValidTime(*args) -> bool:
        h, i, s = map(int, args)
        return (
                h >= 0 and h <= 23
            and i >= 0 and i <= 59
            and s >= 0 and s <= 59
        )
