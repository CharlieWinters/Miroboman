import loguru
import sys

# Cutom Logger
logger = loguru.logger
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD - HH:mm:ss!UTC} - {level} - {file}:{line} - ({extra[request_id]}) {message} ", level="INFO")