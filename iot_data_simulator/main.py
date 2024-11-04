import argparse
from .data_simulator import DataSimulator
from data_message import Batch

def main():
    parser = argparse.ArgumentParser(description="IoT Data Simulator")
    parser.add_argument('--num_devices', type=int, default=100, help='Number of devices to simulate')
    parser.add_argument('--frequency', type=int, default=1, help='Frequency of messages from each device (messages/second)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout duration in seconds')

    args = parser.parse_args()
    
    ds = DataSimulator()

if __name__ == "__main__":
    main()
