import importlib
import pkgutil
import multiprocessing
from multiprocessing import Process
from app.commands import CommandHandler, Command

class App:
    def __init__(self):
        self.command_handler = CommandHandler()
        # Creating exit event to use exit command
        self.exit_event = multiprocessing.Event()

    def execute_command_in_process(self, command_input):
        """Method to execute a command in a separate process."""
        if command_input == "exit":
            self.exit_event.set()
        else:
            self.command_handler.execute_command(command_input)

    def pluginRegistration(self):
        # Dynamically load all plugins in the plugins directory
        pluginPath = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([pluginPath.replace('.', '/')]):
            #For each item, item's name, and pkgFlag in path's list...

            if is_pkg:  # Ensure it's a package

                #Grabs module aka the plugin package folder
                plugin_module = importlib.import_module(f'{pluginPath}.{plugin_name}')

                # for each item in folder, check if theres a subclass and register it as a command
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)):
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue  # Ignore if not class
            else:
                continue

    def start(self):
        # Register plugins as usual
        self.pluginRegistration()

        #Staring repel process
        print("Type 'exit' to exit.")
        while not self.exit_event.is_set():  # Check the exit event
            command_input = input(">>> ").strip()
            command_process = Process(target=self.execute_command_in_process, args=(command_input,))
            command_process.start()
            command_process.join()
