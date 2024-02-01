from __future__ import annotations # @tome For str|Uuid|UUID type.
from .UuidError import UuidError
from .__util import Null, string, typeOf, isTypeOf
from uuid import UUID, uuid4
import re, typing

class Uuid(object):
    # NULL Constants.
    NULL = '00000000-0000-0000-0000-000000000000'
    NULL_HASH = '00000000000000000000000000000000'

    __type: str
    __value: str

    def __init__(self, value: str|Uuid|UUID = Null, strict: bool = True):
        if value is Null:
            value = None
        else:
            types = [str,Uuid,UUID]
            if isTypeOf(value, *types) is False:
                raise UuidError.forInvalidValueType(value, types)
            if strict is True and self.validate(value) is False:
                raise UuidError.forInvalidValue(value)

        self.__type = typeOf(self)
        self.__value = str(value or self.generate())

    def __eq__(self, other: str|Uuid):
        return self.__value == str(other)

    def __str__(self):
        return self.__value

    def __int__(self):
        return self.__hash__()

    def __hash__(self):
        return hash(self.__value)

    def __repr__(self):
        return "%s('%s')" % (self.__type.replace('ouuid.', ''), self.__value)

    def __setattr__(self, aname: str, avalue: typing.Any):
        if aname in ('type', 'value', 'NULL', 'NULL_HASH'):
            raise UuidError('Cannot change type, value, NULL, NULL_HASH')

        return super().__setattr__(aname, avalue)

    ### Getter Methods. ###

    def toString(self) -> str:
        return self.__value

    def toHashString(self) -> str:
        return self.__value.replace('-', '')

    ### Checker Methods. ###

    def isNull(self) -> bool:
        return self.equals(self.NULL, self.__value)

    def isNullHash(self) -> bool:
        return self.equals(self.NULL_HASH, self.__value)

    def isEqual(self, uuid: str|Uuid|UUID) -> bool:
        return self.equals(self.__value, str(uuid))

    def isValid(self, strict: bool = True) -> bool:
        return self.validate(self.__value, strict)

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @staticmethod
    def generate() -> str:
        return str(uuid4())

    @staticmethod
    def validate(uuid: str, strict: bool = True) -> bool:
        uuid = str(uuid)
        if len(uuid) > 36:
            return False

        if strict:
            # With version, variant & dashes.
            res = re.match(
                '^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[ab89][a-f0-9]{3}-[a-f0-9]{12}$',
                uuid, flags=re.IGNORECASE
            )
        else:
            # With/without version, variant & dashes.
            res = re.match(
                '^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$',
                uuid, flags=re.IGNORECASE
            )

        return res is not None

    @staticmethod
    def equals(uuidKnown: str, uuidUnknown: str) -> bool:
        if len(uuidKnown) != len(uuidUnknown):
            return False

        for i in range(len(uuidKnown)):
            if uuidKnown[i] != uuidUnknown[i]:
                return False

        return True

    @staticmethod
    def modify(bins: bytes) -> bytearray:
        bins = bytearray(b'' + bins)

        if len(bins) != 16:
            raise UuidError.forInvalidBins()

        # Add signs: 4 (version) & 8,9,a,b (variant).
        bins[6] = ord(chr(bins[6] & 0x0F | 0x40)) # Version.
        bins[8] = ord(chr(bins[8] & 0x3F | 0x80)) # Variant.

        return bins

    @staticmethod
    def format(hash: str) -> str:
        hash = string(hash)

        if len(hash) != 32 or hash.isHex() is False:
            raise UuidError.forInvalidHash()

        return '%s%s-%s-%s-%s-%s%s%s' % hash.slit(4)
