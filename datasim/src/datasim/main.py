from proto.messages_pb2 import Batch
from .prometheus import REQUESTS_TOTAL, REQUESTS_FAILED, REQUEST_DURATION, DEVICE_FREQ, DEVICE_COUNT
from prometheus_client import start_http_server
import asyncio
import aiohttp
import random
import signal
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

url = "http://controller:8000/incoming-data"

class DataSimulator:
    def __init__(self, num_devices: int, frequency: float):
        self.num_devices = num_devices
        self.frequency = frequency
        self.tasks = []
        self.stop_event = asyncio.Event()

    async def generate_message(self, device_id:int):
        try:
            async with aiohttp.ClientSession() as session:
                while not self.stop_event.is_set():
                    batch = Batch(device_id=device_id,
                                  alpha=random.randint(1, 100),
                                  beta=random.randint(1, 100),
                                  timestamp=str(time.time()))
                    logging.info(f"Отправляем данные. ID: {batch.device_id}, "
                                 f"alpha: {batch.alpha}, beta: {batch.beta}, timestamp: {batch.timestamp}")
                    start_time = time.time()
                    try:
                        async with session.post(url, data=batch.SerializeToString()) as response:
                            duration = time.time() - start_time
                            REQUEST_DURATION.labels(device_id=device_id).set(duration)
                            if response.status == 200:
                                logging.info(f"Ответ от IOT контроллера: {await response.text()}")
                                REQUESTS_TOTAL.labels(status="success").inc()
                            else:
                                error_text = await response.text()
                                logging.error(f"Ошибка при отправке. Статус: {response.status}, тело ошибки: {error_text}.")
                    except Exception as ex:
                        logging.error(f"Ошибка при отправке данных. {ex}")
                        REQUESTS_FAILED.labels(device_id=device_id).inc()
                    await asyncio.sleep(1 / self.frequency) 
        except Exception as ex:
            logging.error(f"An error occurred in task for device {device_id}: {ex}")
        finally:
            logging.info(f"Task stopped for device {device_id}.")

    def stop(self):
        self.stop_event.set()

    async def start(self):
        DEVICE_COUNT.set(self.num_devices)
        DEVICE_FREQ.set(self.frequency)
        for device_id in range(1, self.num_devices + 1):
            self.tasks.append(self.generate_message(device_id))

        await asyncio.gather(*self.tasks)


def main():
    num_devices = 1
    frequency = 2
    generator = DataSimulator(num_devices, frequency)

    start_http_server(8070)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, generator.stop)
    loop.add_signal_handler(signal.SIGINT, generator.stop)

    try:
        loop.run_until_complete(generator.start())
    finally:
        loop.close()

if __name__ == "__main__":
    main()

