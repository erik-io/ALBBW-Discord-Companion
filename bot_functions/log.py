from logging.handlers import RotatingFileHandler
import configparser
import logging


# Initialize logging
def setup_logging():
    """
    This function sets up the logging for the application. It reads the logging level from a configuration file,
    sets up a rotating file handler for the log file and a console handler for console output. Both handlers use
    the same formatter for their log messages. The function also sets the logging level for the root logger.
    """

    # Create a config parser
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Get the logging level from the configuration file, defaulting to 'INFO' if not found
    log_level = config.get('LOGGING', 'log_level', fallback='INFO')

    # Create a formatter for the log messages
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a rotating file handler for the log file
    # The log file will be 'bot.log', with a maximum size of 5MB, and a maximum of 1 backup files
    log_file_handler = RotatingFileHandler('../bot.log', maxBytes=5 * 1024 * 1024, backupCount=1)

    # Set the formatter for the file handler
    log_file_handler.setFormatter(log_formatter)

    # Set the logging level for the file handler
    log_file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Create a console handler for console output
    console_handler = logging.StreamHandler()

    # Set the logging level for the console handler
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Set the formatter for the console handler
    console_handler.setFormatter(log_formatter)

    # Set the logging configuration for the root logger
    # The root logger will have two handlers: the file handler and the console handler
    logging.basicConfig(handlers=[log_file_handler, console_handler], level=logging.DEBUG)

    # Log a message indicating that logging has been set up successfully
    logging.info("Logging set up successfully")
