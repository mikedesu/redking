from redking import RedKingBot
from redking import RedKingBotMaster
from sys import argv
from sys import exit
import asyncio


def usage():
    print("Usage: python botmaster.py <port> <seed>")
    exit(1)


if __name__ == "__main__":
    if len(argv) < 3:
        usage()
    port = int(argv[1])
    seed = int(argv[2])
    # bot = RedKingBot(port)
    botmaster = RedKingBotMaster(port, seed)
    botmaster.init_aes_key()
    try:
        asyncio.run(botmaster.run_server())
    except KeyboardInterrupt:
        print("KeyboardInterrupt Exiting...")
    except asyncio.exceptions.CancelledError:
        print("CancelledError Exiting...")
    except Exception as e:
        print(f"Exception: {e}")
        print("Exiting...")
