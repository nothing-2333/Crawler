

class Crawler:
    def __init__(self, requests, logger) -> None:
        self.logger = logger
        self.debug = logger.debug
        self.error = logger.error
        
        self.requests = requests
        self.get = requests.get
        self.post = requests.post

        
        
if __name__ == "__main__":
    pass