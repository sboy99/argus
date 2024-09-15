from decorators import ExceptionHandler
from lib import Logger,OpenCV


class App:
    def __init__(self):
        self.logger= Logger('APP')
        self.open_cv = OpenCV()

    @ExceptionHandler()
    def run(self):
        self.start_capturing()

    def start_capturing(self):
        self.logger.info('Starting recording...')
        self.open_cv.start_capturing()

    def print_open_cv_version(self):
        self.logger.info('Printing OpenCV version')
        self.logger.info(f"Open CV version: {self.open_cv.get_version()}")