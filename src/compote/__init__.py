import os


class Compote:
    """
    - uniform access for environment variables
    - supply defaults where applicable
    - raise exception if required values are missing
    - optionally transform environment values, default values or result value
    """

    @staticmethod
    def identity(x):
        return x

    @staticmethod
    def fetch_from_env_or_default(
        key,
        default,
        transform_default=identity,
        transform_env=identity,
        transform_value=identity,
    ):
        """
        Fetch value from ENV or return provided default/None
        Apply provided transformation functions or no-op using identity
        function
        """

        if value := os.environ.get(key):
            value = transform_env(value)
        else:
            value = transform_default(default)

        return transform_value(value)

    @staticmethod
    def fetch_from_env_or_fail(key):
        value = os.environ.get(key)
        if value:
            return value
        else:
            raise KeyError('"%s" must be present in host environment.' % key)
