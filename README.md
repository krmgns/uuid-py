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

· Besides all classes can take `value` argument (#1) as type of `str`, `Uuid` class can also take type of `Uuid`, `DateUuid` class can also take type of `DateUuid`, `DateTimeUuid` class can also take type of `DateTimeUuid`, but it also can be skipped for auto-generation at the same time.

· Besides `Uuid` is able to be cast to string, `DateUuid` and `DateTimeUuid` are subclasses of `Uuid` class. So, while inheriting some useful methods (`toString()`, `toHashString()`, etc.), they also overrides some methods (`isValid()`, `generate()`, `validate()` etc.) alongside `__init__()` methods.

· Since `DateTimeUuid` uses an instant date/time stamp up to seconds (format: `%Y%m%d%H%I%S`), the best sortable UUIDs can only be generated with this class.
