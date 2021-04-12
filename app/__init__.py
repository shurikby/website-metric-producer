import logging
from app import producer

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

my_app = producer.Producer(logging)


