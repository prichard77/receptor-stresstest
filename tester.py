from queue import Queue, Empty
import json
import threading
import time
from receptor_stresstest import worker


class FakeInnerEnvelope:
    raw_payload = None


def monitor_queue(queue, event):
    while not event.is_set():
        try:
            qsize = queue.qsize()
            item = queue.get(False)
        except Empty:
            time.sleep(0.1)
        else:
            print(f"Got item from {item['ts']} Blob length: {len(item['blob'])}. Queue size: {qsize}")


if __name__ == '__main__':
    queue = Queue()
    message = FakeInnerEnvelope()
    message.raw_payload = json.dumps(dict(rate=50, length=10, size=512))
    all_done = threading.Event()
    monitor_thread = threading.Thread(target=monitor_queue, args=(queue, all_done))
    monitor_thread.start()
    worker.blunderbuss(message, {}, queue)
    all_done.set()
