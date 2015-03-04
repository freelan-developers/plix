"""
Executor class.
"""

from __future__ import unicode_literals

import yaml
import subprocess

from voluptuous import Schema
from contextlib import closing
from functools import partial
from six import PY2
from locale import getpreferredencoding


class BaseExecutor(object):
    """
    A generic executor class.
    """
    options_schema = Schema({})

    def __init__(self, options=None):
        self.options = self.options_schema(options or {})

    @property
    def full_name(self):
        """
        Get the full name of the executor.

        :returns: The full dotted-name representation of the current instance
            class, including its definition module.
        """
        return '{module}.{name}'.format(
            module=self.__module__,
            name=self.__class__.__name__,
        )

    def execute(self, environment, commands, display):
        """
        Execute the specified commands.

        :param environment: The environment variables dictionary.
        :param commands: A list of commands to execute.
        :param display: The display to use for command output and report.
        """
        for index, command in enumerate(commands):
            with display.command(
                    index,
                    len(commands),
                    command,
            ) as result:
                result.returncode = self.execute_one(
                    environment=environment,
                    command=command,
                    output=partial(display.command_output, index),
                )

                if result.returncode is None:
                    raise RuntimeError(
                        "No returncode specified for command execution "
                        "({})".format(
                            command,
                        ),
                    )


def executor_representer(dumper, executor):
    if executor.options:
        return dumper.represent_mapping(
            'tag:yaml.org,2002:map',
            {
                'name': executor.full_name,
                'options': executor.options,
            },
        )
    else:
        return dumper.represent_scalar(
            'tag:yaml.org,2002:str',
            executor.full_name,
        )


yaml.add_multi_representer(BaseExecutor, executor_representer)


class ShellExecutor(BaseExecutor):
    """
    An executor that execute commands through the system shell.
    """

    def execute_one(self, environment, command, output):
        # Python 2 subprocess doesn't deal well with unicode commands.
        command = (
            command.encode(getpreferredencoding())
            if PY2
            else command
        )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            env=environment,
        )

        with closing(process.stdout):
            while True:
                data = process.stdout.read(4096)

                if data:
                    output(data)
                else:
                    break

        process.wait()
        return process.returncode
