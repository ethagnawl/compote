import pytest

from compote import Compote


def test_fetch_from_env_or_default_transforms_default(monkeypatch):
    class Config(Compote):
        TWO_TWENTY_TWO = Compote.fetch_from_env_or_default(
            "TWO_TWENTY_TWO", "222", transform_default=lambda x: int(x)
        )

    expected = 222
    actual = Config.TWO_TWENTY_TWO
    assert expected == actual


def test_fetch_from_env_or_default_transforms_env(monkeypatch):
    monkeypatch.setenv("TWO_TWENTY_TWO", "222")

    class Config(Compote):
        TWO_TWENTY_TWO = Compote.fetch_from_env_or_default(
            "TWO_TWENTY_TWO", "222", transform_env=lambda x: int(x)
        )

    expected = 222
    actual = Config.TWO_TWENTY_TWO
    assert expected == actual


def test_fetch_from_env_or_default_transforms_value(monkeypatch):
    monkeypatch.setenv("FOO", "111")

    class Config(Compote):
        FOO = Compote.fetch_from_env_or_default(
            "FOO", "333", transform_value=lambda x: 222
        )

    expected = 222
    actual = Config.FOO
    assert expected == actual


def test_fetch_from_env_or_default_transforms_env_and_value(monkeypatch):
    monkeypatch.setenv("FOO", "111")

    class Config(Compote):
        FOO = Compote.fetch_from_env_or_default(
            "FOO",
            "333",
            transform_env=lambda x: int(x) * 2,
            transform_value=lambda x: x * 2,
        )

    expected = 444
    actual = Config.FOO
    assert expected == actual


def test_fetch_from_env_or_default_transforms_default_and_value(monkeypatch):
    class Config(Compote):
        FOO = Compote.fetch_from_env_or_default(
            "FOO",
            "111",
            transform_default=lambda x: int(x) * 3,
            transform_value=lambda x: x * 3,
        )

    expected = 999
    actual = Config.FOO
    assert expected == actual


def test_fetch_from_env_or_default_sets_value(monkeypatch):
    monkeypatch.setenv("FOO", "foo")

    class Config(Compote):
        FOO = Compote.fetch_from_env_or_default("FOO", "not-foo")

    foo = "foo"
    expected = foo
    actual = Config.FOO
    assert expected == actual


def test_fetch_from_env_or_default_sets_defaults():
    class Config(Compote):
        FOO = Compote.fetch_from_env_or_default("FOO", "foo")

    foo = "foo"
    expected = foo
    actual = Config.FOO
    assert expected == actual


def test_fetch_from_env_or_fail_raises_when_no_values_found():
    with pytest.raises(KeyError):

        class Config(Compote):
            FOO = Compote.fetch_from_env_or_fail("FOO")


def test_fetch_from_env_or_fail_sets_value(monkeypatch):
    monkeypatch.setenv("FOO", "foo")

    class Config(Compote):
        FOO = Compote.fetch_from_env_or_fail("FOO")

    foo = "foo"
    expected = foo
    actual = Config.FOO
    assert expected == actual
