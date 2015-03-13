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
from io import open

from .executors import ShellExecutor


def load_from_stream(stream):
    """
    Load a configuration from a YAML stream.

    :param stream: The stream to load the configuration from.
    :returns: The normalized configuration.
    """
    return normalize(yaml.safe_load(stream))


def load_from_file(filename, encoding='utf-8'):
    """
    Load a configuration from a file.

    :param filename: The name of the file to load the configuration from.
    :returns: The normalized configuration.
    """
    with open(filename, encoding=encoding) as stream:
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
        Required('global', default={}): {Extra: object},
        Required('matrix', default={}): {Extra: object},
        Required('exclusion_matrix', default=[]): {Extra: object},
        Required(
            'before_install',
            default=[],
        ): Coerce(command_or_command_list),
        Required('install', default=[]): Coerce(command_or_command_list),
        Required('before_script', default=[]): Coerce(command_or_command_list),
        Required('script', default=[]): Coerce(command_or_command_list),
        Required('after_success', default=[]): Coerce(command_or_command_list),
        Required('after_failure', default=[]): Coerce(command_or_command_list),
        Required('after_script', default=[]): Coerce(command_or_command_list),
    })

    return schema(configuration)
