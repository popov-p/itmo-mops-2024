import argparse
from .data_simulator import DataSimulator
from message_lib import Batch
import time

def main():
    parser = argparse.ArgumentParser(description="IoT Data Simulator")
    parser.add_argument('--num_devices', type=int, default=10, help='Number of devices to simulate')
    parser.add_argument('--frequency', type=int, default=1, help='Frequency of messages from each device (messages/second)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout duration in seconds')

    batch = Batch(
    device_id=123,
    value=45.67,
    timestamp = str(time.time())
    )

    args = parser.parse_args()
    
    ds = DataSimulator()
    print(batch.timestamp)
    serialized_data = batch.SerializeToString()
if __name__ == "__main__":
    main()
