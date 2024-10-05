import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()

# Set the logging level for the handler
console_handler.setLevel(logging.INFO)

# Create a formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
