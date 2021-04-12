from app import producer
from app.producer import Producer


def build_production_app() -> Producer:
    app = producer.create_producer()
    return app
