from loguru import logger 

from .encrypt import Encrypt

debug = logger.debug

class Crawler:
    def __init__(self, requests) -> None:

        self.requests = requests
        self.get = requests.get
        self.post = requests.post
        
        self.encrypt = Encrypt()
