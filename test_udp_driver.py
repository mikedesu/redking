from redking import EchoUDPProtocol
import asyncio


async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoUDPProtocol(), local_addr=("127.0.0.1", 8888)
    )
    try:
        # await asyncio.sleep(3600)  # Keep the server running for an hour
        await asyncio.Event().wait()
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
