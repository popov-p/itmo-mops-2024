import asyncio
from .rabbitmq import connect_to_rabbitmq

async def main():
    connection, channel = await connect_to_rabbitmq()
    try:
        await asyncio.Future()
    finally:
        await channel.close()
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())