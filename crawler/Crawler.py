from loguru import logger 
import json

from .encrypt import Encrypt
from .request import Request
from .env import Env
from .serializer import dumps, loads

debug = logger.debug

class Crawler:
    def __init__(self, env: Env = None, encrypt: Encrypt = None, request: Request = None) -> None:    
        self.env = env
        self.encrypt = encrypt
        self.request = request
        self.tmp = {}
        
        
        
