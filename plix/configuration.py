"""
Configuration parser.
"""

from __future__ import unicode_literals

import yaml

from six import string_types
from voluptuous import (
    Schema,
    Required,
    Coerce,
    Extra,
)

from .executors import ShellExecutor


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
    """
    if isinstance(value, string_types):
        return [value]
    elif isinstance(value, (list, tuple)):
        return value
    else:
        raise ValueError("Value must be either a string or a list")


def parse_executor(value):
    """
    Parse an executor string or dict and turns it into an executor instance.

    :param value: The value to parse.
    :returns: An executor instance.
    """
    if isinstance(value, string_types):
        value = {'name': value}

    executor_schema = Schema({
        Required('name'): str,
        Required('options', default={}): {Extra: object},
    })
    value = executor_schema(value)

    module, klass = value['name'].rsplit('.', 1)
    executor_klass = getattr(__import__(module, fromlist=[klass]), klass)

    return executor_klass(options=value['options'])


def normalize(configuration):
    """
    Normalize and validate a configuration.

    :param configuration: The configuration to normalize.
    :returns: The normalized configuration.
    """
    schema = Schema({
        Required(
            'executor',
            default=ShellExecutor(),
        ): Coerce(parse_executor),
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
