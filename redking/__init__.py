import random
import asyncio
from cryptography.fernet import Fernet
import rsa
import base64


class RedKingBot:
    def __init__(self, port):
        self.server = None
        self.virtual_address = random.uniform(0.0, 1.0)
        self.key = None
        self.private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
        # self.private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
        self.pub = None
        self.crypto = None
        self.port = port

    def is_initialized(self):
        return self.key is not None

    async def run_server(self):
        self.server = await asyncio.start_server(
            self.handle_client, "localhost", self.port
        )
        async with self.server:
            await self.server.serve_forever()
            await self.server.close()
            await self.server.wait_closed()
        self.server = None

    async def handle_client(self, reader, writer):
        request = None
        bad_requests = 0
        exit_commands = ["quit", "exit"]
        # c_host = writer.get_extra_info("peername")
        # c_port = c_host[1]
        # print(f"Connected to {c_host} on port {c_port}")
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
            await self.handle_request(request)
            # writer.write(response.encode("utf8"))
            # await writer.drain()
        writer.close()

    async def handle_request(self, request):
        is_init = self.is_initialized()
        if request == "init":
            if not is_init:
                self.init_aes_key()
                print(f"Initialized key: {self.key}")
            else:
                print("Key already initialized")
            print(f"{self.crypto}")
        elif is_init:
            print("unhandled request type")
            # if request:
            #    print("Connecting to bot...")
            #    host, port = request.split(" ")[1:]
            #    await handle_connect_to_bot(host, port)
            # elif request == "ping":
            #    pass
        else:
            print("Key not initialized")
        return


class RedKingBotMaster(RedKingBot):
    def __init__(self, port):
        super().__init__(port)
        self.crypto = None
        self.pub = None
        self.pubkey = b"-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCNVXuPwxPKJiT+fIOJdbZpSKMeovOuiN68Ckx+9VMGM3UfsDv/553ccqQB\nZP/M+CgNyTdCXXgWeM15bktLvsgdAgMBAAE=\n-----END RSA PUBLIC KEY-----"

    def init_aes_key(self):
        if not self.is_initialized():
            print("Initializing...")
            self.key = Fernet.generate_key()
            self.pub = rsa.PublicKey.load_pkcs1(self.pubkey)
            self.crypto = rsa.encrypt(self.key, self.pub)
            self.crypto = base64.b64encode(self.crypto).decode("utf-8")
