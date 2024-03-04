# main.py
from app import App    

#Main.py | used to run the program itself
# launches instance of 'app' 

# You must put this in your main.py because this forces the program to start when you run it from the command line.
if __name__ == "__main__":
    app = App().start()  # Instantiate an instance of App
