# Compote

## Rationale
Compote is a library which provides structure and utility for use when bootstrapping an application's common configuration class.

This is a pattern which consolidates application configuration in a single source of truth and prevents application components from having to reach out into the environment to read values at runtime, handle missing values, handle type casting of read values, etc. There are two core functions which read values from the environment: `fetch_from_env_or_default` and `fetch_from_env_or_fail`. These functions will be documented below but hopefully their names reveal their intentions.

This library also provides hooks for transformation functions (`transform_env`, `transform_default` and `transform_value`) to apply after reading value from the environment or setting defaults. These are useful for operations like casting value types and doing data validation.

A nice side effect of this consolidation is that it makes stubbing values into test environments simple. Instead of having to monkeypatch the environment, you can just provide a different `Compote` instance in your test setup.

Compote is a piece of code I've been carrying around and iterating on since around 2018. It was originally inspired by the `Config` class in Miguel Grinberg's infamous Flask tutorial.

## Features
### Reading from environment
#### Pull from env and fall back to default
```
class Config(Compote):
    GREETING = Compote.fetch_from_env_or_default("GREETING", "Hiya!")
```

#### Attempt to pull from env and raise a `KeyError` if not found
```
class Config(Compote):
    SOME_API_KEY = Compote.fetch_from_env_or_fail("SOME_API_KEY")
```

### Value Transformation

#### transform_env
This function runs after the field has been set using an environment variable.

```
class Config(Compote):
    SOME_VALUE = Compote.fetch_from_env_or_default(
        "SOME_VALUE",
        111,
        transform_env=lambda x: int(x)
    )
```

#### transform_value
This function runs after the field has been set, regardless of whether the value came from the environment or the default.
```
def some_value_transformer(value):
    value_ = int(value)
    if value_ < 100:
        raise Exception(f"{value_} must be greater than 100!")

class Config(Compote):
    SOME_VALUE = Compote.fetch_from_env_or_default(
        "SOME_VALUE",
        111,
        transform_value=some_value_transformer
    )
```
#### transform_default
This function runs after the field has been set using a default variable. This may seem contrived but it can be useful if `SOME_VALUE` is computed using other `Config` fields and has proved useful in practice.

```
class Config(Compote):
    SOME_OTHER_VALUE = 111
    SOME_VALUE = Compote.fetch_from_env_or_default(
        "SOME_VALUE",
        "111",
        transform_default=lambda x: int(x) + Config.SOME_OTHER_VALUE
    )
```

## Examples

### Flask

See: examples/flask_app.py which can be run using:
```
GREETING=hola uv run --with-editable . examples/flask_app.py
```

## Future Work
### Logging
I find it helpful to know when default values are used and have historically used loguru to log a warning message when this happens. I don't want to add a dependency for anyone wishing to use this library, though, so I plan to add pluggable logging in a future release.
### Types
I personally don't care for Python type hints (because they lie!) but I'll be a good steward and add them at some point.
