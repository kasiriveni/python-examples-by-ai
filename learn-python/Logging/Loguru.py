# Loguru: Simplified Logging

from loguru import logger

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Add a file sink
logger.add("file.log", rotation="1 MB", retention="10 days", level="INFO")
logger.info("This message will also be written to the file")
