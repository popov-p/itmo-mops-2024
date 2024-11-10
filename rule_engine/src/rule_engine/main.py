import asyncio
from prometheus_client import start_http_server
from .rabbitmq import connect_to_rabbitmq

async def main():
    start_http_server(8080)
    connection, channel = await connect_to_rabbitmq()
    try:
        await asyncio.Future()
    finally:
        await channel.close()
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())