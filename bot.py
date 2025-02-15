import asyncio
import rsa
import base64
import sys
import os
from cryptography.fernet import Fernet
import random

key = None
pubkey = b"-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCNVXuPwxPKJiT+fIOJdbZpSKMeovOuiN68Ckx+9VMGM3UfsDv/553ccqQB\nZP/M+CgNyTdCXXgWeM15bktLvsgdAgMBAAE=\n-----END RSA PUBLIC KEY-----"
private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
pub = None
# key = Fernet.generate_key()
crypto = None


virtual_address = random.uniform(0.0, 1.0)

known_bots = []


def is_initialized():
    global key
    return key is not None


def init_aes_key():
    global key
    global crypto
    global pubkey
    global pub
    if not is_initialized():
        print("Initializing...")
        key = Fernet.generate_key()
        pub = rsa.PublicKey.load_pkcs1(pubkey)
        crypto = rsa.encrypt(key, pub)
        crypto = base64.b64encode(crypto).decode("utf-8")


async def handle_connect_to_bot(host, port):
    global known_bots
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write("ping".encode("utf8"))
        await writer.drain()
        response = await reader.read(100)
        print(f"Received: {response.decode('utf8')}")
        known_bots.append((host, port))
        # await writer.close()
        # await reader.close()
    except Exception as e:
        print(f"Error connecting to bot: {e}")
    await writer.close()
    return await reader.close()
    # have to return an awaitable


async def handle_request(request):
    global key
    if request == "init":
        if not is_initialized():
            init_aes_key()
            print(f"Initialized key: {key}")
        else:
            print("Key already initialized")
        print(f"{crypto}")
    elif is_initialized():
        if request:
            print("Connecting to bot...")
            host, port = request.split(" ")[1:]
            await handle_connect_to_bot(host, port)
        # elif request == "ping":
        #    pass
    else:
        print("Key not initialized")
    return


async def handle_client(reader, writer):
    request = None
    bad_requests = 0
    exit_commands = ["quit", "exit"]
    c_host = writer.get_extra_info("peername")
    c_port = c_host[1]
    print(f"Connected to {c_host} on port {c_port}")

    while request not in exit_commands:
        request = (await reader.read(64)).decode("utf8")
        # chop off the newline
        request = request.strip()
        print(f"Received request: {request}")
        # can we get the host and port from the request?

        if len(request) == 0:
            bad_requests += 1
            if bad_requests > 3:
                break
            continue
        bad_requests = 0
        await handle_request(request)
        # writer.write(response.encode("utf8"))
        # await writer.drain()
    writer.close()


def usage():
    print("Usage: python bot.py <port>")
    sys.exit(1)


async def run_server():
    print("run_server")
    print(f"my virtual address is {virtual_address}")
    port = int(sys.argv[1])
    do_init_key = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "1":
            do_init_key = True
        elif sys.argv[2] == "0":
            do_init_key = False
        else:
            usage()
            sys.exit(1)

    server = await asyncio.start_server(handle_client, "localhost", port)

    async with server:
        await server.serve_forever()
        await server.close()
        await server.wait_closed()


if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        usage()
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Shutting down server...")
