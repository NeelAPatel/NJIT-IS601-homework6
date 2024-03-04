from decimal import Decimal, InvalidOperation
from app.commands import Command
from app.plugins.calc.calculator import subtract

class SubtractCommand(Command):

    def execute(self, *args):
        if len(args) != 2:
            return "Please use 'subtract' command with two Decimal numbers as parameters."
    
        try:
            return subtract(Decimal(args[0]), Decimal(args[1]))
        except InvalidOperation:
            return "Invalid input. Please enter two Decimal numbers."
