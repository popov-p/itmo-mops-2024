import argparse
from .data_simulator import DataSimulator
from iot_proto_message import Batch
import time

def main():
    
    batch = Batch(
    device_id=123,
    value=45.67,
    timestamp = str(time.time())
    )

    ds = DataSimulator()
    print(batch.timestamp)

if __name__ == "__main__":
    main()
