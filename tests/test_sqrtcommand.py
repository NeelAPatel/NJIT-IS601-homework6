'''Tests square root command'''
from decimal import Decimal

from app.plugins.sqrt import SqrtCommand

def test_sqrt_command_with_decimal():
    ''' Tests for a single decimal argument '''
    sqrt_command = SqrtCommand()
    result = sqrt_command.execute('16')
    assert result == Decimal('4'), "Should return the square root of the Decimal"

def test_sqrt_command_with_incorrect_args():
    ''' Tests for incorrect number of args '''
    sqrt_command = SqrtCommand()
    result = sqrt_command.execute('10.5', '4')
    assert result == "Please use 'sqrt' command with one Decimal number as a parameter."

def test_sqrt_command_with_non_decimal_input():
    ''' Tests for non-decimal input '''
    sqrt_command = SqrtCommand()
    result = sqrt_command.execute('abc')
    assert result == "Invalid input. Please enter a valid Decimal number."
