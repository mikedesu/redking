from redking import RedKingBot

# from redking import RedKingBotMaster
from sys import argv
from sys import exit
import asyncio


def usage():
    print("Usage: python botmain.py <port> <seed>")
    exit(1)


if __name__ == "__main__":
    if len(argv) < 3:
        usage()
    port = int(argv[1])
    seed = int(argv[2])
    bot = RedKingBot(port, seed)
    try:
        asyncio.run(bot.run_server())
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
