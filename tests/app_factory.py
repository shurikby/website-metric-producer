from app import producer, database
from app.producer import Producer
from app.database import MyPostgresDB


def build_production_app() -> Producer:
    app = producer.create_producer()
    return app


def build_postgres_db(test_mode=True) -> MyPostgresDB:
    db = database.create_producer(test_mode)
    return db
