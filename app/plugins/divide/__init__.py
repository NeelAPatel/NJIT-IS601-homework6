from decimal import Decimal, InvalidOperation

from app.commands import Command
from app.plugins.calc.calculator import divide

class DivideCommand(Command):

    def execute(self, *args):
        # Check if the correct number of arguments is provided
        if len(args) != 2:
            return "Please use 'divide' command with two Decimal numbers as parameters."
    
        # # Attempt to convert arguments to Decimal and divide them
        try:
            return divide(Decimal(args[0]), Decimal(args[1]))
        except InvalidOperation:
            return "Invalid input. Please enter two Decimal numbers."

