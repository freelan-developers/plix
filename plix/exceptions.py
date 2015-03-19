"""
Exceptions classes.
"""


class UnknownKeys(RuntimeError):
    """
    Unknown keys were specified.
    """

    def __init__(self, keys):
        keys = frozenset(keys)

        super(UnknownKeys, self).__init__(
            ', '.join(keys),
        )

        self.keys = keys


class DuplicateKeys(RuntimeError):
    """
    Duplicate keys were specified.
    """

    def __init__(self, keys):
        keys = frozenset(keys)

        super(DuplicateKeys, self).__init__(
            ', '.join(keys),
        )

        self.keys = keys
