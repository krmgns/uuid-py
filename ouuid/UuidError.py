from __future__ import annotations
from .__util import typeOf
import typing

class UuidError(Exception):
    def getMessage(self):
        return str(self)

    @property
    def message(self):
        return str(self)

    @staticmethod
    def forInvalidValueType(value: typing.Any, types: list[type]) -> UuidError:
        given = typeOf(value)
        if given == 'NoneType':
            given = 'None'

        # Map all real type names.
        types = map(lambda t: typeOf(t, True), types)

        return UuidError('Argument value type must be %s, %s given' % (
            '|'.join(types), given
        ))

    @staticmethod
    def forInvalidValue(value: typing.Any) -> UuidError:
        return UuidError("Invalid UUID value: '%s'" % value)

    @staticmethod
    def forInvalidDateValue(value: typing.Any) -> UuidError:
        return UuidError("Invalid date UUID value: '%s'" % value)

    @staticmethod
    def forInvalidDateTimeValue(value: typing.Any) -> UuidError:
        return UuidError("Invalid date/time UUID value: '%s'" % value)

    @staticmethod
    def forInvalidBins() -> UuidError:
        return UuidError('Modify for only 16-length bins')

    @staticmethod
    def forInvalidHash() -> UuidError:
        return UuidError('Format for only 32-length hashes')
