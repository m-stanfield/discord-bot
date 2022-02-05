import logging

class testClass:
    def __init__(self,logger = None):
        self._logger = logger or logging.getLogger(__name__)
        self._logger.info("Logger in class")
