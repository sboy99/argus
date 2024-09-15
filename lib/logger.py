import logging
import os

class Logger:
    def __init__(self, name, log_level=logging.INFO):
        # Create a custom logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Define log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create console handler (logging to standard output)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Define default log directory
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # File handlers for each log level
        self._add_file_handler(log_dir, "info.log", logging.INFO, formatter)
        self._add_file_handler(log_dir, "warning.log", logging.WARNING, formatter)
        self._add_file_handler(log_dir, "error.log", logging.ERROR, formatter)
        self._add_file_handler(log_dir, "critical.log", logging.CRITICAL, formatter)

    def _add_file_handler(self, log_dir, log_file, level, formatter):
        """
        Helper function to add a file handler for a specific log level.
        """
        file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
