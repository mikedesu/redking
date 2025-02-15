import random
import asyncio
from cryptography.fernet import Fernet
import rsa
import base64
import rich


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
        self.priv = rsa.PrivateKey.load_pkcs1(self.private_key_bytes)
        rich.print(f"Initialized with virtual address {self.virtual_address}")

    def is_initialized(self):
        return self.key is not None

    async def run_server(self):
        rich.print(f"running server on port {self.port}")
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
            default_read_size = 128
            request = (await reader.read(default_read_size)).decode("utf8")
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
            await self.handle_request(request, writer)
            # writer.write(response.encode("utf8"))
            # await writer.drain()
        writer.close()

    async def handle_request(self, request, writer):
        if not writer:
            rich.print("No writer received")
            return
        is_init = self.is_initialized()
        if not request:
            rich.print("No request received")
            return
        if request == "init":
            if not is_init:
                self.init_aes_key()
                print(f"Initialized key: {self.key}")
            else:
                print("Key already initialized")
            print(f"{self.crypto}")
            return
        # elif is_init:
        # print("unhandled request type")
        command_parts = request.split(" ")
        cmd = command_parts[0]

        rich.print(f"Received command: {cmd}")

        if cmd == "pushkey":
            host = command_parts[1]
            port = int(command_parts[2])
            await self.pushkey_to_bot(host, port)
        elif cmd == "key":
            encoded_encrypted_key = command_parts[1]
            rich.print(f"Received key: {encoded_encrypted_key}")
            encrypted_key = base64.b64decode(encoded_encrypted_key)
            # rich.print(f"Decoding key: {encrypted_key}")

            try:
                decrypted_key = rsa.decrypt(encrypted_key, self.priv)
                # rich.print(f"Decrypted key: {decrypted_key}")
                self.key = decrypted_key
                rich.print(f"Decrypted key: {self.key}")
                # lets test encrypting something
                test_msg = "welcome to evildojo"
                test_msg_bytes = test_msg.encode("utf-8")

                f = Fernet(self.key)

                encrypted_msg = f.encrypt(test_msg_bytes)

                rich.print(f"Encrypted message: {encrypted_msg}")
                rich.print("Sending encrypted message to client")
                # write the encrypted message to the writer
                await writer.write(encrypted_msg)

                # rich.print(f"Encrypted message: {encrypted_msg}")
                # rich.print(f"Encrypted message length: {len(encrypted_msg)}")

            except Exception as e:
                rich.print(f"Error decrypting key: {e}")
        else:
            rich.print("Unrecognized command")
        return

    async def pushkey_to_bot(self, host, port):
        # global known_bots
        try:
            reader, writer = await asyncio.open_connection(host, port)

            # instead of writing ping, perhaps we want to write the key
            msg = f"key {self.crypto}"
            # msg = "ping"
            writer.write(msg.encode("utf8"))

            await writer.drain()
            default_read_size = 1024
            response = await reader.read(default_read_size)
            decoded_response = response.decode("utf8")
            print(f"Received: {decoded_response}")
            # its base64 encoded
            # and encrypted with the aes key
            # lets decrypt it
            f = Fernet(self.key)
            decrypted_response = f.decrypt(response)
            print(f"Decrypted response: {decrypted_response}")

            # known_bots.append((host, port))
            # await writer.close()
            # await reader.close()
        except Exception as e:
            print(f"Error connecting to bot: {e}")
        await writer.close()
        return await reader.close()
        # have to return an awaitable


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
