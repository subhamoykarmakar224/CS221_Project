import logging
import multiprocessing
import queue
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, ProcessPoolExecutor

from app_stream.jobpool.JobBuffer import JobBuffer


class JobStreamer():
    def __init__(self):
        self.level = logging.DEBUG
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.handler.setLevel(self.level)
        self.log = logging.getLogger(__name__)
        self.log.addHandler(self.handler)
        self.log.setLevel(self.level)
        self.WAIT_SLEEP = 1  # second, adjust this based on the timescale of your tasks
        self.shutting_down = queue.Queue()  # Use a queue to signal shutdown.

    def shutdown(self, signum, frame):
        self.log.warning('Caught signal %d, shutting down...' % signum)
        # Put an item in the shutting down queue to signal shutdown.
        self.shutting_down.put(None)

    def is_shutting_down(self):
        return not self.shutting_down.empty()

    def stop(self):
        self.shutting_down.put(None)

    def stream_processor_mprocessor(self, input_stream, task, num_workers=multiprocessing.cpu_count()):
        # Register the signal handler
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

        futures = dict()
        buffer = JobBuffer(input_stream)
        with ProcessPoolExecutor(num_workers) as executor:
            num_success = 0
            num_failure = 0
            while True:
                idle_workers = num_workers - len(futures)

                if not self.is_shutting_down():
                    items, is_finished = buffer.nextN(idle_workers)
                    if is_finished:
                        self.stop()

                    for data in items:
                        futures[executor.submit(task, data)] = data

                done, _ = wait(futures, timeout=self.WAIT_SLEEP, return_when=ALL_COMPLETED)
                for f in done:
                    data = futures[f]
                    try:
                        f.result(timeout=0)
                    except Exception as exc:
                        self.log.error('future encountered an exception: %r, %s' % (data, exc))
                        num_failure += 1
                    else:
                        self.log.info('future finished successfully: %r' % data)
                        num_success += 1

                    del futures[f]

                if self.is_shutting_down() and len(futures) == 0:
                    break

            self.log.info("num_success=%d, num_failure=%d" % (num_success, num_failure))

    def stream_processor_mthreads(self, input_stream, task, num_workers):
        # Register the signal handler
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

        futures = dict()
        buffer = JobBuffer(input_stream)
        with ThreadPoolExecutor(num_workers) as executor:
            num_success = 0
            num_failure = 0
            while True:
                idle_workers = num_workers - len(futures)

                if not self.is_shutting_down():
                    items = buffer.nextN(idle_workers)
                    for data in items:
                        futures[executor.submit(task, data)] = data

                done, _ = wait(futures, timeout=self.WAIT_SLEEP, return_when=ALL_COMPLETED)
                for f in done:
                    data = futures[f]
                    try:
                        f.result(timeout=0)
                    except Exception as exc:
                        self.log.error('future encountered an exception: %r, %s' % (data, exc))
                        num_failure += 1
                    else:
                        self.log.info('future finished successfully: %r' % data)
                        num_success += 1

                    del futures[f]

                if self.is_shutting_down() and len(futures) == 0:
                    break

            self.log.info("num_success=%d, num_failure=%d" % (num_success, num_failure))

