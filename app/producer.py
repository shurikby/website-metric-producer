import logging
from datetime import datetime, timezone
from app import database, kafka
from threading import Thread, Event, Lock
from requests import get
from re import search
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def get_website_metrics(url='http://localhost', find_str=None):
    sample_start_time = datetime.now(timezone.utc)
    r = get(url, timeout=120)
    isFound = True
    if find_str is not None:
        isFound = search(find_str, r.text) is not None
    return sample_start_time, r.status_code, r.elapsed.total_seconds(), isFound


class Producer:
    log = None
    pg_db = None
    kafka_p = None
    thread_list = []
    global_data_lock = Lock()
    global_event = Event()
    global_sample_results = []

    def __init__(self, pg_db: database.MyPostgresDB, kafka_p:kafka.MyKafkaProducer, log: logging):
        self.log = log
        self.pg_db = pg_db
        self.kafka_p = kafka_p

    def internal_measurement_thread(self, target_params):
        self.log.info("Thread url_id %s: starting", target_params['url_id'])
        while not self.global_event.is_set():
            self.log.info("Thread url_id %s: sampling started", target_params['url_id'])
            response_metrics = get_website_metrics(target_params['url_path'], target_params['regex_pattern'])
            # self.log.info("Thread url_id %s: sampling ended", target_params['url_id'])
            # self.log.info("Thread url_id %s: waiting for with global_data_lock:", target_params['url_id'])
            with self.global_data_lock:
                self.global_sample_results.append((target_params['url_id'],) + response_metrics)
            self.log.info("Thread url_id %s: wait for %s seconds:",
                          target_params['url_id'], target_params['sample_frequency_s'])
            self.global_event.wait(target_params['sample_frequency_s'])
        self.log.info("Thread url_id %s: Ended", target_params['url_id'])

    def auto_save_thread(self):
        self.log.info("Auto save thread: starting")
        while not self.global_event.is_set():
            tmp_samples_list = []
            with self.global_data_lock:
                if self.global_sample_results:
                    tmp_samples_list = self.global_sample_results
                    self.global_sample_results = []
            if tmp_samples_list:
                self.log.info("Auto saving %s samples", len(tmp_samples_list))
                if not self.kafka_p.send_measurements(tmp_samples_list):
                    self.log.warn("Auto saving failed.")
            self.global_event.wait(10)
        logging.info("Auto save thread: Ended")

    def run(self):
        auto_save_thread_handler = None
        try:
            urls = self.pg_db.get_urls()
            for url_id in urls:
                x = Thread(target=self.internal_measurement_thread, args=(urls[url_id],))
                x.start()
                self.thread_list.append(x)
            auto_save_thread_handler = Thread(target=self.auto_save_thread)
            auto_save_thread_handler.start()
            while not self.global_event.is_set():
                self.global_event.wait(1)
        except KeyboardInterrupt:
            self.log.info("Exiting the background task.")
            self.log.info("Sending a global interrupt to all threads to exit their loop.")
            self.global_event.set()
        self.log.info("Waiting for all threads to end.")
        for t in self.thread_list:
            t.join()
        if auto_save_thread_handler:
            auto_save_thread_handler.join()
        tmp_count = len(self.global_sample_results)
        logging.info("Saving any remaining sample %s.", tmp_count)
        self.pg_db.insert_measurements(self.global_sample_results)
        self.log.info("Exiting the producer.")


def create_producer() -> Producer:
    pg_db = database.create_postgres_db()
    kafka_p = kafka.create_kafka_producer()
    return Producer(pg_db, kafka_p, logging)
