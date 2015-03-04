"""
Python 2/3 compatibility helpers.
"""

from __future__ import unicode_literals

import yaml

from six import PY2

unicode = unicode if PY2 else str


def construct_yaml_str(self, node):
    """
    Override the default string handling function to always return unicode
    objects.
    """
    return self.construct_scalar(node)


# Make yaml loading function always return unicode strings.
yaml.Loader.add_constructor('tag:yaml.org,2002:str', construct_yaml_str)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:str', construct_yaml_str)


def unicode_representer(self, value):
    """
    Represents unicode strings as regular strings.
    """
    return yaml.ScalarNode(tag='tag:yaml.org,2002:str', value=value)

# Make unicode representation nice for unicode strings.
yaml.Dumper.add_representer(unicode, unicode_representer)


def yaml_dump(object, **kwargs):
    """
    Give the yaml representation of an object as a unicode string.

    :param object: The object to get the unicode YAML representation from.
    :returns: A unicode string.
    """
    encoding = 'utf-8'
    result = yaml.dump(
        object,
        encoding=encoding,
        allow_unicode=True,
        **kwargs
    )

    return result.decode(encoding)
