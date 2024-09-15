from lib.logger import Logger


class App:
    def __init__(self):
        self.logger= Logger('APP')

    def run(self):
        self.logger.info('App is running...')