from redking import RedkingUDP
import asyncio
from sys import argv

# from redking import RedkingMasterUDP


async def main():
    port = int(argv[1])
    if port < 1024 or port > 65535:
        print("Port number must be between 1024 and 65535")
        return

    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: RedkingUDP(), local_addr=("127.0.0.1", port)
    )
    try:
        await asyncio.Event().wait()
    except Exception as e:
        print(f"Exception: {e}")
    transport.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Killing the bot...")
    except Exception as e:
        print(f"Exception: {e}")
