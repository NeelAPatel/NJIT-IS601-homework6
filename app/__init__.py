import importlib
import pkgutil
import multiprocessing
from multiprocessing import Process
from app.commands import CommandHandler, Command
#logging and env imports
import os
import sys
from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True) #if exists, then its fine
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        
        #program
        self.command_handler = CommandHandler()
        # Creating exit event to use exit command
        self.exit_event = multiprocessing.Event()
        
    def configure_logging(self):
        # use logging.conf to configure 
        logging_conf_path = 'logging.conf'

        #checks if path to logging file exists
        if os.path.exists(logging_conf_path): 
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)
    

    def execute_command_in_process(self, command_input):
        """Method to execute a command in a separate process."""
        if command_input == "exit":
            self.exit_event.set()
        else:
            self.command_handler.execute_command(command_input)

    def pluginLoad(self):
        # Dynamically load all plugins in the plugins directory
        pluginPath = 'app.plugins'
        
        # #Path check
        # if not os.path.exists(pluginPath):
        #     #unsure why this is triggered when app.plugins does exist. 
        #     logging.warning(f"Plugins directory at '{pluginPath}' not found.") 
        #     return
    
        #For each item, item's name, and pkgFlag in path's list...
        for _, plugin_name, is_pkg in pkgutil.iter_modules([pluginPath.replace('.', '/')]):

            if is_pkg:  # Ensure it's a package
                try:
                    #Grabs module aka the plugin package folder
                    plugin_module = importlib.import_module(f'{pluginPath}.{plugin_name}')
                    logging.info(f"Plugin Registering: {plugin_name}")
                    self.registerPlugin(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error while importing plugin {plugin_name}: {e}")
            else:
                continue
                

    def registerPlugin(self, plugin_module, plugin_name) :
        # for each item in folder, check if theres a subclass and register it as a command
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            try:
                if issubclass(item, (Command)):
                    self.command_handler.register_command(plugin_name, item())
                    logging.info(f"Plugin Loaded: {plugin_name}")
            except TypeError:
                continue  # Ignore if not class

    def start(self):
        # Register plugins as usual
        self.pluginLoad()
        logging.info("Plugins Loaded. Application started. Type 'exit' to exit.")

        #Staring repel process
        #print("Type 'exit' to exit.")
        try: 
            while not self.exit_event.is_set():  # Check the exit event
                command_input = input(">>> ").strip()
                command_process = Process(target=self.execute_command_in_process, args=(command_input,))
                command_process.start()
                command_process.join()
        except KeyboardInterrupt: 
            logging.info("App interrupted via keyboard. Exiting gracefully")
            sys.exit(0)
        finally: 
            logging.info("App terminated.")