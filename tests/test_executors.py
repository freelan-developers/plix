"""
Test executors logic.
"""

import yaml

from unittest import TestCase
from voluptuous import Schema
from six import StringIO

from mock import (
    patch,
    call,
    MagicMock,
)

from plix.executors import (
    BaseExecutor,
    ShellExecutor,
)

from .common import MockDisplay


class ExecutorsTests(TestCase):
    def test_executors_are_yaml_representable(self):
        class MyExecutor(BaseExecutor):
            options_schema = Schema({'foo': str})
            __module__ = 'my_module'

        executor = MyExecutor(options={'foo': 'bar'})

        self.assertEqual(
            yaml.dump({
                'name': 'my_module.MyExecutor',
                'options': {
                    'foo': 'bar',
                }
            }),
            yaml.dump(executor),
        )

    def test_executors_are_yaml_representable_without_options(self):
        class MyExecutor(BaseExecutor):
            options_schema = Schema({'foo': str})
            __module__ = 'my_module'

        executor = MyExecutor(options={})

        self.assertEqual(
            yaml.dump('my_module.MyExecutor'),
            yaml.dump(executor),
        )

    def test_base_executors_requires_a_returncode(self):
        class MyExecutor(BaseExecutor):
            def execute_one(self, environment, command, output):
                pass

        display = MockDisplay()
        executor = MyExecutor()

        with self.assertRaises(RuntimeError):
            executor.execute(
                environment={},
                commands=['a'],
                display=display,
            )

    def test_shell_executor_execute(self):
        environment = {"FOO": "BAR"}
        commands = ["alpha", "beta"]

        display = MockDisplay()
        executor = ShellExecutor()

        def Popen(command, env=None, *args, **kwargs):
            process = MagicMock()
            process.stdout = StringIO(command)
            process.returncode = 0

            self.assertEqual(environment, env)

            return process

        with patch('subprocess.Popen', side_effect=Popen):
            executor.execute(
                environment=environment,
                commands=commands,
                display=display,
            )

        self.assertEqual(
            display.start_command.mock_calls,
            [
                call(index=0, total=2, command="alpha"),
                call(index=1, total=2, command="beta"),
            ],
        )
        self.assertEqual(
            display.stop_command.mock_calls,
            [
                call(index=0, total=2, command="alpha", returncode=0),
                call(index=1, total=2, command="beta", returncode=0),
            ],
        )
        self.assertEqual(
            display.command_output.mock_calls,
            [
                call(0, "alpha"),
                call(1, "beta"),
            ],
        )
