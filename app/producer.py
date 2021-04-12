import logging
from time import sleep


class Producer:
    log = None

    def __init__(self, log: logging):
        self.log = log

    def run(self, process_mode):
        try:
            while True:
                self.log.info('Producing '+process_mode)
                sleep(1)
        except KeyboardInterrupt:
            self.log.info("Exiting the background task.")
