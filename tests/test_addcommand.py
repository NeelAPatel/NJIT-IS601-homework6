'''Tests add command'''
from decimal import Decimal

from app.plugins.add import AddCommand

def test_add_command_with_two_decimals():
    ''' Tests for 2-number args '''
    add_command = AddCommand()
    result = add_command.execute('10.5', '20.3')
    assert result == Decimal('30.8'), "Should return the sum of two Decimal numbers"

def test_add_command_with_incorrect_args():
    ''' Tests for incorrect args '''
    add_command = AddCommand()
    result = add_command.execute('10.5')
    assert result == "Please use 'add' command with two Decimal numbers as parameters."

def test_add_command_with_non_decimal_input():
    ''' Tests for wrong type args '''
    add_command = AddCommand()
    result = add_command.execute('abc', 'xyz')
    assert result == "Invalid input. Please enter two Decimal numbers."
