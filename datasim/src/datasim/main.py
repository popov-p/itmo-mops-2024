from proto import messages_pb2
import asyncio
import random

class DataSimulator:
    def __init__(self, num_devices: int, frequency: float):
        self.num_devices = num_devices
        self.frequency = frequency

    async def generate_message(self, device_id: int):
        while True:
            message = f"{device_id} привет"
            print(message)
            await asyncio.sleep(1 / self.frequency)

    async def start(self):
        tasks = []
        for device_id in range(1, self.num_devices + 1):
            tasks.append(self.generate_message(device_id))

        await asyncio.gather(*tasks)


def main():
    num_devices = 5
    frequency = 2
    generator = DataSimulator(num_devices, frequency)
    asyncio.run(generator.start())

if __name__ == "__main__":
    main()

