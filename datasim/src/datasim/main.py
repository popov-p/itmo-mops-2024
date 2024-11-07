from proto import messages_pb2
import asyncio
import random
import signal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataSimulator:
    def __init__(self, num_devices: int, frequency: float):
        self.num_devices = num_devices
        self.frequency = frequency
        self.tasks = []
        self.stop_event = asyncio.Event()

    async def generate_message(self, device_id: int):
        try:
            while not self.stop_event.is_set():
                message = f"Device {device_id} sending message."
                logging.info(message)
                await asyncio.sleep(1 / self.frequency)
        finally:
            logging.info(f"Task stopped for device {device_id}.")

    def stop(self):
        self.stop_event.set()

    async def start(self):
        for device_id in range(1, self.num_devices + 1):
            self.tasks.append(self.generate_message(device_id))

        await asyncio.gather(*self.tasks)


def main():
    num_devices = 5
    frequency = 1
    generator = DataSimulator(num_devices, frequency)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, generator.stop)
    loop.add_signal_handler(signal.SIGINT, generator.stop)

    try:
        loop.run_until_complete(generator.start())
    finally:
        loop.close()

if __name__ == "__main__":
    main()

