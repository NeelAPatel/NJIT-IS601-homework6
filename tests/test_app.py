''' This module tests the functions of launching the application itself '''
from unittest.mock import patch, call
import os
import pytest
from app import App

# Assuming you have a dummy command for testing
from app.plugins.hello import HelloCommand as DummyCommand
from app.commands import CommandHandler

@pytest.fixture
def app_instance():
    '''Fixture for App instance; initializes a mock version of the app with specific libraries'''
    #Loads libraries
    with patch('os.makedirs'), \
        patch('app.App.configure_logging'), \
        patch('dotenv.load_dotenv'), \
        patch('logging.basicConfig'), \
        patch('logging.info'):
        app = App()
    # Assuming CommandHandler has a register_command method
    app.command_handler.register_command("dummy", DummyCommand())
    return app


def test_app_initialization(app_instance):
    '''Test for App initialization'''
    assert isinstance(app_instance.command_handler, CommandHandler) #Is instance created
    assert app_instance.exit_event.is_set() is False
    assert app_instance.settings.get('ENVIRONMENT') == 'PRODUCTION' #Tests environment variable is set to dev

def test_load_environment_variables(app_instance):
    '''Test for environment variable loading'''
    with patch.dict(os.environ, {'TEST_VAR': 'VALUE'}):
        settings = app_instance.load_environment_variables()
    assert settings['TEST_VAR'] == 'VALUE'

def test_configure_logging():
    '''Test for logging configuration'''
    app_instance = App()
    app_instance.configure_logging()

def test_plugin_load(app_instance):
    '''Test if plugins load properly'''
    with patch('pkgutil.iter_modules', return_value=[(None, 'dummy_plugin', True)]), \
        patch('importlib.import_module') as mock_import_module, \
        patch('app.App.registerPlugin') as mock_register_plugin:
        app_instance.pluginLoad()
        mock_import_module.assert_called_once_with('app.plugins.dummy_plugin')
        mock_register_plugin.assert_called()

def test_app_keyboard_interrupt(app_instance):
    '''Test for KeyboardInterrupt handling'''
    with patch('builtins.input', side_effect=KeyboardInterrupt), \
         patch('multiprocessing.Process') as mock_process, \
         patch('logging.info') as mock_log_info, \
         patch('sys.exit') as mock_exit:
        app_instance.start()
        mock_process.assert_not_called()
        mock_log_info.assert_has_calls([
            call("App interrupted via keyboard. Exiting gracefully."),
            call("App terminated.")
        ], any_order=True)

        mock_exit.assert_called_once_with(0)


def test_start_exit_immediately(app_instance):
    ''' test if you run program, load and exit immediately'''
    with patch('builtins.input', return_value='exit'), \
         patch('multiprocessing.Process') as mock_process, \
         patch('app.App.execute_command_in_process') as mock_execute_command, \
         patch('logging.info') as mock_log_info:

        # Set the exit_event to simulate immediate exit
        app_instance.exit_event.set()

        app_instance.start()

        # Assert that input was never called due to the immediate exit condition
        mock_execute_command.assert_not_called()

        # Assert that a new process was never started
        mock_process.assert_not_called()

        # Check for expected log messages
        expected_logs = ["All Plugins Loaded. Application started.", "Type 'exit' to exit.", "App terminated."]
        for expected_log in expected_logs:
            assert any(expected_log in call.args[0] for call in mock_log_info.call_args_list)
