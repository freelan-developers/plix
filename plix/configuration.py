"""
Configuration parser.
"""

import yaml


class Configuration(object):
    """
    Holds a configuration.
    """

    @staticmethod
    def load_from_stream(stream):
        """
        Load a configuration from a stream.

        :param stream: The stream to load the configuration from.
        :returns: A :class:`plix.configuration.Configuration` instance.
        """
        return Configuration(conf=yaml.safe_load(stream))

    @staticmethod
    def load_from_file(filename):
        """
        Load a configuration from a file.

        :param filename: The name of the file to load the configuration from.
        :returns: A :class:`plix.configuration.Configuration` instance.
        """
        with open(filename) as stream:
            return Configuration.load_from_stream(stream=stream)

    def __init__(self, conf):
        """
        Creates a new configuration from a dictionary of its values.

        :param conf: A dictionary of configuration values.
        """
        self.conf = conf
