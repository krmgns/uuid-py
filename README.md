While preserving version & variant fields of generated values, Uuid library provides three types of UUIDs with a simple and fast approach, and can be used where sortable UUIDs are needed.

The `generate()` method of;

- `Uuid` class uses 16-length random bytes (UUID/v4).
- `DateUuid` class uses 12-length random bytes and 4-length bytes of UTC date as prefix, and generated values are sortable up to 8th hex character.
- `DateTimeUuid` class uses 10-length random bytes and 6-length bytes of UTC date/time as prefix, and generated values are sortable up to 12th hex character.

Besides these UUIDs are sortable, they can be used for some sort of jobs like folder exploration (say, where we are working with an image cropping service).

So, as a quick example, let's see it in action;

```py
from ouuid import DateUuid, UuidError
from fastapi import FastAPI
import os

app = FastAPI()

# Eg: cdn.foo.com/image/crop/0134b3ce-ce20-4917-a020-f0514e110834.jpg
# @route /image/crop/:image
@app.get('/image/crop/{image}')
def cropAction(image):
    # Eg: 0134b3ce-ce20-4917-a020-f0514e110834.jpg
    name, extension = image.split('.')

    try:
        # Since we've created an image file name with DateUuid,
        # here we're expecting the incoming image to be valid.
        uuid = DateUuid(name)

        # Eg: 2023/11/12
        path = uuid.getDate('/')
    except UuidError:
        # Invalid DateUuid.
        raise BadRequestError()
    except:
        # Internal error.
        raise InternalServerError()

    # Eg: /images/2023/11/12/0134b3ce-ce20-4917-a020-f0514e110834.jpg
    image = '/images/%s/%s.%s' % (path, name, extension)

    # No such file.
    if not os.path.exists(image):
        raise NotFoundError()

    # Else crop image & serve cropped image here...
```

### Installing
```
pip install ouuid
```

### Notes / Reminding

· Besides all classes can take `value` argument (#1) as type of `str` and built-in `uuid.UUID`, `Uuid` class can also take type of `Uuid`, `DateUuid` class can also take type of `DateUuid`, `DateTimeUuid` class can also take type of `DateTimeUuid`, but it also can be skipped for auto-generation at the same time.

· Besides `Uuid` is able to be cast to string, `DateUuid` and `DateTimeUuid` are subclasses of `Uuid` class. So, while inheriting some useful methods (`toString()`, `toHashString()`, etc.), they also overrides some methods (`isValid()`, `generate()`, `validate()` etc.) alongside `__init__()` methods.

· Since `DateTimeUuid` uses an instant date/time stamp up to seconds (format: `%Y%m%d%H%I%S`), the best sortable UUIDs can only be generated with this class.

### The `Uuid` Class

Like the inheriting classes, when no `value` (UUID value) given, `Uuid` class will generate and assign its value by itself. Otherwise, given value will be assigned after it's checked in strict mode (modifier argument is `strict` as `True`) whether it's a valid UUID value or not.

```py
from ouuid import Uuid, UuidError

# Auto-generate.
uuid = Uuid()

assert uuid.value == uuid.toString()
assert uuid.value == str(uuid)
assert uuid.value == uuid # Equable

assert True == uuid.isEqual(uuid)
assert True == uuid.isEqual(uuid.value)

uuid = Uuid('26708ec6-ad78-4291-a449-9ee08cf50cfc')
assert True == uuid.isValid()

uuid = Uuid('invalid', strict=False)
assert False == uuid.isValid()

try: Uuid(null)
except UuidError as e:
    assert "Argument value type must be str|ouuid.Uuid|uuid.UUID, None given" == e.message

try: Uuid('invalid')
except UuidError as e:
    assert "Invalid UUID value: 'invalid'" == e.message

# Given value.
value = '26708ec6-ad78-4291-a449-9ee08cf50cfc'
uuid = Uuid(value)

assert True == uuid.isEqual(uuid)
assert True == uuid.isEqual(uuid.value)
assert True == uuid.isEqual(value)

assert '26708ec6-ad78-4291-a449-9ee08cf50cfc' == uuid.toString()
assert '26708ec6ad784291a4499ee08cf50cfc' == uuid.toHashString()

# Null values.
uuid1 = Uuid('00000000-0000-0000-0000-000000000000', strict=False)
uuid2 = Uuid('00000000000000000000000000000000', strict=False)

assert False == uuid1.isValid()
assert False == uuid2.isValid()

assert True == uuid1.isNull()
assert True == uuid2.isNullHash()

assert Uuid.NULL == uuid1.value
assert Uuid.NULL_HASH == uuid2.value
```

#### Statics

```py
# Generating.
uuid = Uuid.generate() # Eg: fec3cfe2-d378-4181-8ba1-99c54bcfa63e

# Validating.
valid = Uuid.validate(uuid)
assert True == valid

assert False == Uuid.validate('invalid')
assert False == Uuid.validate('invalid', strict=False)

assert False == Uuid.validate(Uuid.NULL)
assert False == Uuid.validate(Uuid.NULL_HASH)

assert True == Uuid.validate(Uuid.NULL, strict=False)
assert True == Uuid.validate(Uuid.NULL_HASH, strict=False)

# Equal checking.
assert True == Uuid.equals(uuid, 'fec3cfe2-d378-4181-8ba1-99c54bcfa63e')
assert False == Uuid.equals(uuid, 'invalid-uuid-input-value')

# DIY tools.
bins = random.randbytes(16)

# Add version/variant.
bins = Uuid.modify(bins)

# Format as UUID format.
uuid = Uuid.format(bins.hex())
```

See [test/main.py](test/main.py) for more examples. <br><br>
