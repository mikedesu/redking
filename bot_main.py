from redking import RedKingBot
from redking import RedKingBotMaster
from sys import argv
from sys import exit
import asyncio


def usage():
    print("Usage: python bot_main.py <port>")
    exit(1)


if __name__ == "__main__":
    if len(argv) < 2:
        usage()
    port = int(argv[1])
    # bot = RedKingBot(port)
    botmaster = RedKingBotMaster(port)
    botmaster.init_aes_key()
    asyncio.run(botmaster.run_server())
