import asyncio
import base64
import datetime
import json
import logging


logger = logging.getLogger(__name__)


class Blunderbuss:
    """
    queue - Queue to push responses onto
    rate - Number of responses per second
    length - Number of seconds to generate responses for
    size - Standard response payload size
    """

    def __init__(self, queue, rate=5, length=60, size=512):
        self.queue = queue
        self.rate = rate
        self.length = length
        self.size = size

    async def run(self):
        loop = asyncio.get_event_loop()
        seconds_left = self.length
        while seconds_left:
            for _ in range(self.rate):
                loop.create_task(self.emit())
            await asyncio.sleep(1)
            seconds_left -= 1
        await asyncio.sleep(1)

    async def emit(self):
        self.queue.put(
            dict(
                ts=datetime.datetime.utcnow().isoformat(),
                blob=base64.encodebytes(
                    open("/dev/urandom", "rb").read(self.size // 4 * 3)
                ).decode("utf8"),
            )
        )


def blunderbuss(message, config, queue):
    args = json.loads(message.raw_payload)
    response_generator = Blunderbuss(queue, **args)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(response_generator.run())


blunderbuss.receptor_export = True
