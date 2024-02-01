from __future__ import annotations
from .Uuid import Uuid, UuidError
from .__util import Null, string, dating, isTypeOf
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from uuid import UUID
import struct, random

class DateTimeUuid(Uuid):
    threshold: str|int = None

    def __init__(self, value: str|DateTimeUuid|UUID = Null, strict: bool = True, threshold: str|int = None):
        if value is Null:
            value = None
        else:
            types = [str,Uuid,DateTimeUuid,UUID]
            if isTypeOf(value, *types) is False:
                raise UuidError.forInvalidValueType(value, types)
            if strict is True and self.validate(value, threshold) is False:
                raise UuidError.forInvalidDateTimeValue(value)

        value = value or self.generate()

        super().__init__(value, False)

    def getDate(self, separator: str = None) -> list[str]|None:
        date, _ = self.parse(self.value, self.threshold) or [None, None]

        if date and separator:
            date = f'%s{separator}%s{separator}%s' % (*date,)
            # date = f'{{0}}{separator}{{1}}{separator}{{2}}'.format(*date) # alt

        return date

    def getTime(self, separator: str = None) -> list[str]|None:
        _, time = self.parse(self.value, self.threshold) or [None, None]

        if time and separator:
            time = f'%s{separator}%s{separator}%s' % (*time,)
            # time = f'{{0}}{separator}{{1}}{separator}{{2}}'.format(*time) # alt

        return time

    def getDateTime(self, zone: str = None) -> datetime|None:
        date, time = self.parse(self.value, self.threshold) or [None, None]

        if date and time:
            y, m, d, h, i, s = map(int, date + time)
            ret = datetime(y, m, d, h, i, s, tzinfo=ZoneInfo('UTC'))

            # Convert to zone.
            if zone is not None:
                ret = ret.astimezone(ZoneInfo(zone))

            return ret

        return None

    def isValid(self, strict: bool = True, threshold: str|int = None) -> bool:
        return self.validate(self.value, strict, threshold or self.threshold)

    @staticmethod
    def generate() -> str:
        date = DateTimeUuid.datetime()
        bins = struct.pack('Q', int(date))

        # Drop NULL pads, reverse, add random bytes.
        bins = bins[:-2][::-1] + random.randbytes(10)

        # Add version/variant.
        bins = Uuid.modify(bins)

        return Uuid.format(bins.hex())

    @staticmethod
    def validate(uuid: str, strict: bool = True, threshold: str|int = None) -> bool:
        if not Uuid.validate(uuid, strict):
            return False
        if not DateTimeUuid.parse(uuid, threshold):
            return False

        return True

    @staticmethod
    def parse(uuid: str, threshold: str|int = None) -> list[list[str]]|None:
        ret, sub = None, string(uuid).cut(13).drop('-')

        # Extract usable part from value.
        if len(sub) == 12 and sub.isHex():
            dec = int(sub, 16)
            tmp = string(dec).slit(2, tup=False).pad(7).cut(7)
            y, m, d, h, i, s = [''.join(tmp[:2])] + tmp[2:]

            # Validate.
            if dating.isValidDate(y, m, d) and dating.isValidTime(h, i, s):
                ret = [[y, m, d], [h, i, s]]

        # Validate.
        if ret:
            if threshold and dec < int(threshold):
                return None
            if dec > int(DateTimeUuid.datetime()):
                return None

        return ret

    @staticmethod
    def datetime() -> str:
        return dating.utcDateTime()
