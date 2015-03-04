"""
Common classes for tests.
"""

from plix.executors import BaseExecutor
from plix.displays import BaseDisplay

from six import StringIO
from mock import (
    patch,
    MagicMock,
)


class PythonExecutor(BaseExecutor):
    """
    An executor that executes Python code.
    """
    def __init__(self, options=None, globals=None, locals=None):
        super(PythonExecutor, self).__init__(options=options)
        self.globals = globals
        self.locals = locals

    def execute_one(self, environment, command, output):

        stdout = StringIO()
        stderr = StringIO()

        with patch('sys.stderr', stderr), patch('sys.stdout', stdout):
            try:
                exec(command, self.globals, self.locals)
            except Exception as ex:
                stderr.write(str(ex))

        output(stdout.getvalue())
        output(stderr.getvalue())

        return 0


class MockDisplay(BaseDisplay):
    def __new__(cls):
        self = super(MockDisplay, cls).__new__(cls)
        self.start_command = MagicMock()
        self.stop_command = MagicMock()
        self.command_output = MagicMock()
        return self
