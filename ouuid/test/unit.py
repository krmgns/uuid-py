""" Run:
$ python3.9 test/main.py
$ python3.9 -m unittest test/main.py
"""

import os, sys
# Not working in console.
# sys.path.append(os.path.realpath('..'))
# sys.path.append(os.path.realpath('../..'))
# Constant "__file__" is required for console.
# sys.path.append(os.path.abspath(__file__ + '/../..'))
sys.path.insert(0, os.path.abspath(__file__ + '/../../..'))

from ouuid import Uuid, DateUuid, DateTimeUuid, UuidError
from ouuid.__util import listing, string, dating
from uuid import UUID as PyUuid
import unittest

UUID = '84572c49-f0b6-4286-8008-22026cc6209e'
DATE_UUID = '0134d703-6a41-4bf8-b4b1-49f126d4f932'
DATE_TIME_UUID = '126885d2-0f33-4d31-8373-7b4cd61bb661'

class UuidTest(unittest.TestCase):
    def testConstructor(self):
        uuid = Uuid()

        self.assertIsInstance(uuid.value, str)
        self.assertEqual(uuid.value, Uuid(uuid.value))
        self.assertEqual(uuid.value, Uuid(uuid).value)

        uuid = Uuid(UUID)

        # All valid.
        self.assertEqual(uuid, str(PyUuid(UUID)))
        self.assertEqual(uuid, Uuid(Uuid(UUID)))
        self.assertEqual(uuid, Uuid(DateUuid(UUID, strict=False)))
        self.assertEqual(uuid, Uuid(DateTimeUuid(UUID, strict=False)))

        with self.assertRaises(UuidError) as ctx: Uuid(None)
        self.assertEqual("Argument value type must be str|ouuid.Uuid|uuid.UUID, None given",
            str(ctx.exception))

        with self.assertRaises(UuidError) as ctx: Uuid('invalid')
        self.assertEqual("Invalid UUID value: 'invalid'", str(ctx.exception))

    def testMagicMethods(self):
        uuid = Uuid(UUID)

        # __eq__
        self.assertTrue(uuid == UUID)
        # __str__
        self.assertEqual(str(uuid), uuid.value)
        # __int__
        self.assertEqual(int(uuid), hash(uuid.value))
        # __hash_
        self.assertEqual(hash(uuid), hash(uuid.value))
        # __repr__
        self.assertEqual(repr(uuid), "%s('%s')" % (uuid.type.replace('ouuid.', ''), uuid.value))

        # __setattr__
        with self.assertRaises(UuidError): uuid.type = 'x'
        with self.assertRaises(UuidError): uuid.value = 'x'
        with self.assertRaises(UuidError): uuid.NULL = 'x'
        with self.assertRaises(UuidError): uuid.NULL_HASH = 'x'

    def testGetterMethods(self):
        uuid = Uuid(UUID)

        self.assertEqual(uuid.toString(), UUID)
        self.assertEqual(uuid.toHashString(), UUID.replace('-', ''))

    def testCheckerMethods(self):
        uuid = Uuid(UUID)

        self.assertFalse(uuid.isNull())
        self.assertFalse(uuid.isNullHash())
        self.assertTrue(uuid.isEqual(UUID))
        self.assertTrue(uuid.isValid())

        uuid = Uuid(Uuid.NULL, strict=False)

        self.assertTrue(uuid.isNull())
        self.assertFalse(uuid.isNullHash())
        self.assertTrue(uuid.isEqual(Uuid.NULL))
        self.assertFalse(uuid.isValid())
        self.assertTrue(uuid.isValid(strict=False))

        uuid = Uuid(Uuid.NULL_HASH, strict=False)

        self.assertTrue(uuid.isNullHash())
        self.assertTrue(uuid.isEqual(Uuid.NULL_HASH))
        self.assertFalse(uuid.isValid())
        self.assertTrue(uuid.isValid(strict=False))

    def testPropertyMethods(self):
        uuid = Uuid(UUID)

        self.assertEqual('ouuid.Uuid', uuid.type)
        self.assertEqual(UUID, uuid.value)

    def testGenerate(self):
        uuid = Uuid.generate()
        hash = string(uuid.replace('-', ''))

        self.assertEqual(36, len(uuid))
        self.assertEqual(32, len(hash))
        self.assertTrue(hash.isHex())

        version, variant = hash[12], hash[16]

        self.assertEqual(version, '4')
        self.assertIn(variant, ['8','9','a','b'])

    def testValidate(self):
        uuid1 = Uuid()
        uuid2 = Uuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertTrue(Uuid.validate(uuid1.value))
        self.assertTrue(Uuid.validate(uuid2.value, strict=False))
        self.assertFalse(Uuid.validate('invalid'))
        self.assertFalse(Uuid.validate('invalid', strict=False))

    def testEquals(self):
        uuid1 = Uuid()
        uuid2 = Uuid(uuid1)

        self.assertTrue(Uuid.equals(uuid1.value, uuid2.value))
        self.assertFalse(Uuid.equals(uuid1.value, 'invalid'))

    def testModify(self):
        bins = Uuid.modify(os.urandom(16))

        self.assertIsInstance(bins, bytearray)
        self.assertEqual(16, len(bins))

        with self.assertRaises(UuidError) as ctx: Uuid.modify(b'invalid')
        self.assertEqual('Modify for only 16-length bins', str(ctx.exception))

    def testFormat(self):
        hash = Uuid.format(os.urandom(16).hex())

        self.assertIsInstance(hash, str)
        self.assertEqual(36, len(hash))

        with self.assertRaises(UuidError) as ctx: Uuid.format('invalid')
        self.assertEqual('Format for only 32-length hashes', str(ctx.exception))

class DateUuidTest(unittest.TestCase):
    def testConstructor(self):
        uuid = DateUuid()

        self.assertIsInstance(uuid.value, str)
        self.assertEqual(uuid.value, DateUuid(uuid.value))
        self.assertEqual(uuid.value, DateUuid(uuid).value)

        uuid = DateUuid(DATE_UUID)

        # All valid.
        self.assertEqual(uuid, str(DateUuid(DATE_UUID)))
        self.assertEqual(uuid, DateUuid(DateUuid(DATE_UUID)))
        self.assertEqual(uuid, DateUuid(DateUuid(DATE_UUID, strict=False)))
        self.assertEqual(uuid, DateUuid(DateUuid(DATE_UUID, strict=False)))

        with self.assertRaises(UuidError) as ctx: DateUuid(None)
        self.assertEqual("Argument value type must be str|ouuid.Uuid|ouuid.DateUuid|uuid.UUID, None given",
            str(ctx.exception))

        with self.assertRaises(UuidError) as ctx: DateUuid('invalid')
        self.assertEqual("Invalid date UUID value: 'invalid'", str(ctx.exception))

    def testGetDate(self):
        uuid = DateUuid()
        date = dating.utcDate('%Y.%m.%d').split('.')

        self.assertEqual(date, uuid.getDate())
        self.assertEqual('-'.join(date), uuid.getDate(separator='-'))

        uuid = DateUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNone(uuid.getDate())

    def testGetDateTime(self):
        uuid = DateUuid()
        date = dating.utcDate('%Y.%m.%d').split('.')
        time = '00.00.00'.split('.')

        self.assertEqual('-'.join(date), uuid.getDateTime().strftime('%Y-%m-%d'))
        self.assertEqual(':'.join(time), uuid.getDateTime().strftime('%H:%M:%S'))

        uuid = DateUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNone(uuid.getDateTime())

    def testIsValid(self):
        uuid = DateUuid()
        threshold = self.threshold()

        self.assertTrue(uuid.isValid())
        self.assertFalse(uuid.isValid(threshold=threshold))

    def testGenerate(self):
        uuid = DateUuid.generate()
        hash = string(uuid.replace('-', ''))

        self.assertEqual(36, len(uuid))
        self.assertEqual(32, len(hash))
        self.assertTrue(hash.isHex())

        version, variant = hash[12], hash[16]

        self.assertEqual(version, '4')
        self.assertIn(variant, ['8','9','a','b'])

    def testValidate(self):
        uuid1 = DateUuid()
        uuid2 = DateUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertTrue(DateUuid.validate(uuid1.value))
        self.assertFalse(DateUuid.validate(uuid2.value, strict=False))
        self.assertFalse(DateUuid.validate('invalid'))
        self.assertFalse(DateUuid.validate('invalid', strict=False))

        threshold = self.threshold()

        self.assertFalse(DateUuid.validate(uuid1.value, threshold=threshold))
        self.assertFalse(DateUuid.validate(uuid2.value, threshold=threshold, strict=False))

    def testParse(self):
        uuid1 = DateUuid()
        uuid2 = DateUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNotNone(DateUuid.parse(uuid1.value))
        self.assertIsNone(DateUuid.parse(uuid2.value))

        threshold = self.threshold()

        self.assertIsNone(DateUuid.parse(uuid1.value, threshold=threshold))

    @staticmethod
    def threshold(diff = 1):
        # Next year to falsify (eg: 20241212).
        return str(int(dating.utcDate('%Y')) + diff) + '1212'

class DateTimeUuidTest(unittest.TestCase):
    def testConstructor(self):
        uuid = DateTimeUuid()

        self.assertIsInstance(uuid.value, str)
        self.assertEqual(uuid.value, DateTimeUuid(uuid.value))
        self.assertEqual(uuid.value, DateTimeUuid(uuid).value)

        uuid = DateTimeUuid(DATE_TIME_UUID)

        # All valid.
        self.assertEqual(uuid, str(DateTimeUuid(DATE_TIME_UUID)))
        self.assertEqual(uuid, DateTimeUuid(DateTimeUuid(DATE_TIME_UUID)))
        self.assertEqual(uuid, DateTimeUuid(DateTimeUuid(DATE_TIME_UUID, strict=False)))
        self.assertEqual(uuid, DateTimeUuid(DateTimeUuid(DATE_TIME_UUID, strict=False)))

        with self.assertRaises(UuidError) as ctx: DateTimeUuid(None)
        self.assertEqual("Argument value type must be str|ouuid.Uuid|ouuid.DateTimeUuid|uuid.UUID, None given",
            str(ctx.exception))

        with self.assertRaises(UuidError) as ctx: DateTimeUuid('invalid')
        self.assertEqual("Invalid date/time UUID value: 'invalid'", str(ctx.exception))

    def testGetDate(self):
        uuid = DateTimeUuid()
        date = dating.utcDate('%Y.%m.%d').split('.')

        self.assertEqual(date, uuid.getDate())
        self.assertEqual('-'.join(date), uuid.getDate(separator='-'))

        uuid = DateTimeUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNone(uuid.getDate())

    def testGetTime(self):
        uuid = DateTimeUuid()
        time = dating.utcDate('%H.%M.%S').split('.')

        self.assertEqual(time, uuid.getTime())
        self.assertEqual(':'.join(time), uuid.getTime(separator=':'))

        uuid = DateTimeUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNone(uuid.getTime())

    def testGetDateTime(self):
        uuid = DateTimeUuid()
        date = dating.utcDate('%Y.%m.%d').split('.')
        time = dating.utcDate('%H.%M.%S').split('.')

        self.assertEqual('-'.join(date), uuid.getDateTime().strftime('%Y-%m-%d'))
        self.assertEqual(':'.join(time), uuid.getDateTime().strftime('%H:%M:%S'))

        uuid = DateTimeUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNone(uuid.getDateTime())

    def testIsValid(self):
        uuid = DateTimeUuid()
        threshold = self.threshold()

        self.assertTrue(uuid.isValid())
        self.assertFalse(uuid.isValid(threshold=threshold))

    def testGenerate(self):
        uuid = DateTimeUuid.generate()
        hash = string(uuid.replace('-', ''))

        self.assertEqual(36, len(uuid))
        self.assertEqual(32, len(hash))
        self.assertTrue(hash.isHex())

        version, variant = hash[12], hash[16]

        self.assertEqual(version, '4')
        self.assertIn(variant, ['8','9','a','b'])

    def testValidate(self):
        uuid1 = DateTimeUuid()
        uuid2 = DateTimeUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertTrue(DateTimeUuid.validate(uuid1.value))
        self.assertFalse(DateTimeUuid.validate(uuid2.value, strict=False))
        self.assertFalse(DateTimeUuid.validate('invalid'))
        self.assertFalse(DateTimeUuid.validate('invalid', strict=False))

        threshold = self.threshold()

        self.assertFalse(DateTimeUuid.validate(uuid1.value, threshold=threshold))
        self.assertFalse(DateTimeUuid.validate(uuid2.value, threshold=threshold, strict=False))

    def testParse(self):
        uuid1 = DateTimeUuid()
        uuid2 = DateTimeUuid('d41d8cd98f00b204e9800998ecf8427e', strict=False)

        self.assertIsNotNone(DateTimeUuid.parse(uuid1.value))
        self.assertIsNone(DateTimeUuid.parse(uuid2.value))

        threshold = self.threshold()

        self.assertIsNone(DateTimeUuid.parse(uuid1.value, threshold=threshold))

    @staticmethod
    def threshold(diff = 1):
        # Next year to falsify (eg: 20241212191919).
        return str(int(dating.utcDate('%Y')) + diff) + '1212191919'


######## MAIN ############
if __name__ == '__main__':
    unittest.main(exit=False)
