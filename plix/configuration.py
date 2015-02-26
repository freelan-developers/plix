"""
Configuration parser.
"""

import yaml

from six import string_types
from voluptuous import (
    Schema,
    Coerce,
    Extra,
)


def load_from_stream(stream):
    """
    Load a configuration from a YAML stream.

    :param stream: The stream to load the configuration from.
    :returns: The normalized configuration.
    """
    return normalize(yaml.safe_load(stream))


def load_from_file(filename):
    """
    Load a configuration from a file.

    :param filename: The name of the file to load the configuration from.
    :returns: The normalized configuration.
    """
    with open(filename) as stream:
        return load_from_stream(stream=stream)


def command_or_command_list(value):
    """
    Validate a value as a command or a command list.

    :param value: The value to validate.
    :returns: A command list.

    >>> command_or_command_list("foo")
    ['foo']

    >>> command_or_command_list(["foo", "bar"])
    ['foo', 'bar']

    >>> command_or_command_list(None)
    Traceback (most recent call last):
    ...
    ValueError: Value must be either a string or a list

    >>> command_or_command_list(42)
    Traceback (most recent call last):
    ...
    ValueError: Value must be either a string or a list
    """
    if isinstance(value, string_types):
        return [value]
    elif isinstance(value, (list, tuple)):
        return value
    else:
        raise ValueError("Value must be either a string or a list")


def normalize(configuration):
    """
    Normalize and validate a configuration.

    :param configuration: The configuration to normalize.
    :returns: The normalized configuration.
    """
    schema = Schema({
        'global': {Extra: object},
        'matrix': {Extra: object},
        'exclusion_matrix': {Extra: object},
        'before_install': Coerce(command_or_command_list),
        'install': Coerce(command_or_command_list),
        'before_script': Coerce(command_or_command_list),
        'script': Coerce(command_or_command_list),
        'after_success': Coerce(command_or_command_list),
        'after_failure': Coerce(command_or_command_list),
        'after_script': Coerce(command_or_command_list),
    })

    return schema(configuration)
