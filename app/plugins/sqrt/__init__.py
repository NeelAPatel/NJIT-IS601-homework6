from decimal import Decimal, InvalidOperation, getcontext
from app.commands import Command
from app.plugins.calc.calculator import sqrt

class SqrtCommand(Command):

    def execute(self, *args):
        getcontext().prec = 10  # Example precision setting
        
        # Check if the correct number of arguments is provided
        if len(args) != 1:
            return "Please use 'sqrt' command with one Decimal number as a parameter."
        
        try:
            return sqrt(Decimal(args[0]))
        except InvalidOperation:
            return "Invalid input. Please enter a valid Decimal number."
