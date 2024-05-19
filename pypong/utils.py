"""
PyPong utils
"""


import logging


class Logger:
    """
    Logger class for PyPong
    """
    
    def __init__(self) -> None:
        
        logging.basicConfig(level=logging.DEBUG)

    def log(self, message: str) -> None:
        """
        Log a message.
        """
        
        logging.debug(message)


logger = Logger()
