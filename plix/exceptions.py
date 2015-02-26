"""
Exceptions classes.
"""


class UnknownKeys(RuntimeError):
    """
    Unknown keys where specified.
    """

    def __init__(self, keys):
        keys = frozenset(keys)

        super(UnknownKeys, self).__init__(
            ', '.join(keys),
        )

        self.keys = keys
