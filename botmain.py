from redking import RedKingBot

# from redking import RedKingBotMaster
from sys import argv
from sys import exit
import asyncio


def usage():
    print("Usage: python botmain.py <port>")
    exit(1)


if __name__ == "__main__":
    if len(argv) < 2:
        usage()
    port = int(argv[1])
    bot = RedKingBot(port)
    asyncio.run(bot.run_server())
