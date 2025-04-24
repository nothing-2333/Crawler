from loguru import logger 

from .encrypt import Encrypt
from .request import Request
from .env import Env

debug = logger.debug

class Crawler:
    def __init__(self, env: Env = None, encrypt: Encrypt = None, request: Request = None) -> None:    
        self.env = env
        self.encrypt = encrypt
        self.request = request
        
        
        self.tmp_args = {}
