# pylint: disable=unnecessary-dunder-call, invalid-name, line-too-long, trailing-whitespace, missing-final-newline
'''Tests subtract command'''
from decimal import Decimal

from app.plugins.subtract import SubtractCommand

def test_subtract_command_with_two_decimals():
    ''' Tests for 2-number args '''
    subtract_command = SubtractCommand()
    result = subtract_command.execute('10.5', '20.3')
    assert result == Decimal('-9.8'), "Should return the difference of two Decimals"

def test_subtract_command_with_incorrect_args():
    ''' Tests for incorrect args '''
    subtract_command = SubtractCommand()
    result = subtract_command.execute('10.5')
    assert result == "Please use 'subtract' command with two Decimal numbers as parameters."

def test_subtract_command_with_non_decimal_input():
    ''' Tests for wrong type args '''
    subtract_command = SubtractCommand()
    result = subtract_command.execute('abc', 'xyz')
    assert result == "Invalid input. Please enter two Decimal numbers."
