from __future__ import annotations
from .Uuid import Uuid, UuidError
from .__util import Null, string, dating, isTypeOf
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from uuid import UUID
import struct, random

class DateUuid(Uuid):
    threshold: str|int = None

    def __init__(self, value: str|DateUuid|UUID = Null, strict: bool = True, threshold: str|int = None):
        if value is Null:
            value = None
        else:
            types = [str,Uuid,DateUuid,UUID]
            if isTypeOf(value, *types) is False:
                raise UuidError.forInvalidValueType(value, types)
            if strict is True and self.validate(value, threshold) is False:
                raise UuidError.forInvalidDateValue(value)

        value = value or self.generate()

        super().__init__(value, False)

    def getDate(self, separator: str = None) -> str|None:
        date = self.parseDate(self.value, self.threshold)

        if date and separator:
            s = string(date).slit(2)
            date = f'%s%s{separator}%s{separator}%s' % s

        return date

    def getDateTime(self, zone: str = None) -> datetime|None:
        date = self.parseDate(self.value, self.threshold)

        if date:
            s = string(date).slit(2)
            y, m, d = map(int, [s[0] + s[1], s[2], s[3]])
            ret = datetime(y, m, d, 0, 0, 0, tzinfo=ZoneInfo('UTC'))

            # Convert to zone.
            if zone is not None:
                ret = ret.astimezone(ZoneInfo(zone))

            return ret

        return None

    def isValid(self, strict: bool = True, threshold: str|int = None) -> bool:
        return self.validate(self.value, strict, threshold or self.threshold)

    @staticmethod
    def generate() -> str:
        date = DateUuid.date()
        bins = struct.pack('Q', int(date))

        # Drop NULL pads, reverse, add random bytes.
        bins = bins[:-4][::-1] + random.randbytes(12)

        # Add version/variant.
        bins = Uuid.modify(bins)

        return Uuid.format(bins.hex())

    @staticmethod
    def validate(uuid: str, strict: bool = True, threshold: str|int = None) -> bool:
        if not Uuid.validate(uuid, strict):
            return False
        if not DateUuid.parseDate(uuid, threshold):
            return False

        return True

    @staticmethod
    def parseDate(uuid: str, threshold: str|int = None) -> str|None:
        ret, sub = None, string(str(uuid)[0:8])

        # Extract usable part from value.
        if len(sub) == 8 and sub.isHex():
            dec = int(sub, 16)
            tmp = string(dec).slit(2, tup=False).pad(4).cut(4)
            y, m, d = [''.join(tmp[:2])] + tmp[2:]

            # Validate
            if dating.isValidDate(y, m, d):
                ret = str(dec)

        # Validate.
        if ret:
            if threshold and dec < int(threshold):
                return None
            if dec > int(DateUuid.date()):
                return None

        return ret

    @staticmethod
    def date() -> str:
        return dating.utcDate()
