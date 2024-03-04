'''Tests multiply command'''
from decimal import Decimal

from app.plugins.multiply import MultiplyCommand

def test_multiply_command_with_two_decimals():
    ''' Tests for 2-number args '''
    multiply_command = MultiplyCommand()
    result = multiply_command.execute('5', '4')
    assert result == Decimal('20'), "Should return the sum of two Decimals"

def test_multiply_command_with_incorrect_args():
    ''' Tests for incorrect args '''
    multiply_command = MultiplyCommand()
    result = multiply_command.execute('10.5')
    assert result == "Please use 'multiply' command with two Decimal numbers as parameters."

def test_multiply_command_with_non_decimal_input():
    ''' Tests for wrong type args '''
    multiply_command = MultiplyCommand()
    result = multiply_command.execute('abc', 'xyz')
    assert result == "Invalid input. Please enter two Decimal numbers."
