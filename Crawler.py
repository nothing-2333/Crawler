from Encrypt import Encrypt

class Crawler:
    def __init__(self, requests, logger) -> None:
        self.logger = logger
        self.debug = logger.debug
        self.error = logger.error
        
        self.requests = requests
        self.get = requests.get
        self.post = requests.post
        
        self.encrypt = Encrypt(logger)
        self.encrypt.test()

        
        
if __name__ == "__main__":
    pass