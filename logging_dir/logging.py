import logging
import sys

# Custom logger
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - module: %(filename)s - line: %(lineno)s - %(message)s', level=logging.INFO)
logger.info('Initialized logging')


#formatter = logga.Formatter("%(asctime)s - %(levelname)s - line: %(lineno)s - %(message)s")

# Handlers
"""
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('logging_dir/file.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.WARNING)

# Formatters and add to handlers

log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

# Add handlers to the logger

logga.addHandler(c_handler)
logga.addHandler(f_handler)

logga.info("This is an info")
#logga.warning("This is a warning")
#logga.error("This is an error")
"""

