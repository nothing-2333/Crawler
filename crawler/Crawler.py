from loguru import logger 

from .encrypt import Encrypt
from .request import Request

debug = logger.debug

class Crawler:
    def __init__(self, base_headers, proxies=None) -> None:    
        self.encrypt = Encrypt()
        self.request = Request(base_headers, proxies)

