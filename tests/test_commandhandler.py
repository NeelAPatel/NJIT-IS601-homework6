'''Tests Command Handler'''
from unittest.mock import MagicMock
import pytest
from app.commands import Command, CommandHandler

# Mock command for testing
class TestCommand(Command):
    ''' dummy class for dummy command'''
    def execute(self, *args):
        return "Command executed with args: " + " ".join(args)

@pytest.fixture
def command_handler():
    ''' Fixture for command handler'''
    handler = CommandHandler()
    return handler

# Define the test function for the concrete implementation
def test_command_execute():
    ''' tests the Command Class's instaniation'''
    result = TestCommand().execute()
    assert result == "Command executed with args: ", "The execute method should return 'Command executed with args: '"
    
def test_handler_index_error(capsys):
    ''' tests index error occurance'''
    CommandHandler().execute_command(command_line="")
    captured = capsys.readouterr()

    assert captured.out == "No command entered.\n"

def test_execute_valid_command_with_parameters(capfd, command_handler):
    ''' tests if command can run with parameters'''
    command_handler.register_command('test', TestCommand())
    command_handler.execute_command('test arg1 arg2')
    captured = capfd.readouterr()
    assert "Command executed with args: arg1 arg2" in captured.out

def test_execute_valid_command_without_parameters(capfd, command_handler):
    ''' tests if command can run with no parameters'''
    command_handler.register_command('test', TestCommand())
    command_handler.execute_command('test')
    captured = capfd.readouterr()
    assert "Command executed with args:" in captured.out

def test_execute_unknown_command(capfd, command_handler):
    ''' tests if command can run with nonexistent command'''
    command_handler.execute_command('unknown')
    captured = capfd.readouterr()
    assert "Command 'unknown' not found." in captured.out

def test_execute_no_input(capfd, command_handler):
    ''' tests if command can run with no input'''
    command_handler.execute_command('')
    captured = capfd.readouterr()
    assert "No command entered." in captured.out

def test_execute_command_with_exception(capfd, command_handler):
    ''' tests if command can run with raising exceptions'''
    test_command = TestCommand()
    test_command.execute = MagicMock(side_effect=Exception("Test exception"))
    command_handler.register_command('error', test_command)
    command_handler.execute_command('error')
    captured = capfd.readouterr()
    assert "Error executing command 'error': Test exception" in captured.out
