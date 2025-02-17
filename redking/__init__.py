import random
import asyncio
from cryptography.fernet import Fernet
import rsa
import base64
import rich


def print_info(msg):
    rich.print(f":pizza: {msg}")


def print_success(msg):
    rich.print(f":thumbs_up: {msg}")


def print_error(msg):
    rich.print(f":pile_of_poo: {msg}")


class RedKingBot:
    def __init__(self, port):
        self.is_master = False
        self.server = None
        self.virtual_address = random.uniform(0.0, 1.0)
        self.key = None
        self.private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
        # self.private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
        self.pub = None
        self.crypto = None
        self.port = port
        self.priv = rsa.PrivateKey.load_pkcs1(self.private_key_bytes)
        self.neighbors = {}
        print_info(f"Initialized with virtual address {self.virtual_address}")

    def is_initialized(self):
        return self.key is not None

    async def run_server(self):
        print_info(f"Running server on port {self.port}")
        self.server = await asyncio.start_server(
            self.handle_client, "localhost", self.port
        )
        try:
            async with self.server:
                await self.server.serve_forever()
            self.server.close()
            await self.server.wait_closed()
            self.server = None
        except Exception as e:
            print_error(f"Error running server: {e}")

    async def handle_client(self, reader, writer):
        print_info("Handling client")
        request = None
        bad_requests = 0
        exit_commands = ["quit", "exit"]
        c_extra_info = writer.get_extra_info("peername")
        c_host = c_extra_info[0]
        while request not in exit_commands:
            default_read_size = 1024
            request = (await reader.read(default_read_size)).decode("utf8")
            request = request.strip()
            if len(request) == 0:
                # print_error(f"Empty request from {c_host}")
                bad_requests += 1
                if bad_requests > 3:
                    print_error(
                        f"Too many bad requests, closing connection to {c_host}"
                    )
                    break
                continue
            print_info(f"Received request: {request} from {c_host}")
            bad_requests = 0
            await self.handle_request(request, reader, writer)
            # writer.write(response.encode("utf8"))
            # await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def handle_request(self, request, reader, writer):
        if not writer:
            print_error("No writer received")
            return
        # is_init = self.is_initialized()
        if not request:
            print_error("No request received")
            return
        if request == "init":
            print_info(f"{self.crypto}")
            return
        command_parts = request.split(" ")
        if not command_parts:
            print_error("No command parts")
            return
        await self.handle_command(command_parts, reader, writer)

    async def handle_command(self, cmd_parts, reader, writer):
        cmd = cmd_parts[0]
        print_info(f"Received command: {cmd}")
        # first of all, only the master can receive 'raw' commands
        if len(cmd) == 0:
            print_error("Empty command")
        elif cmd == "pushkey":
            await self.pushkey_to_bot(cmd_parts)
        elif cmd == "pullkey":
            await self.pullkey_from_master(cmd_parts, writer)
        else:
            print_error("Unrecognized command")

    async def pullkey_from_master(self, cmd_parts, writer):
        if self.is_master:
            print_error("Only bot can receive pullkey command")
            return
        encoded_encrypted_key = cmd_parts[1]
        print_info(f"Received key: {encoded_encrypted_key}")
        try:
            encrypted_key = base64.b64decode(encoded_encrypted_key)
            decrypted_key = rsa.decrypt(encrypted_key, self.priv)
            self.key = decrypted_key
            print_info(f"Decrypted key: {self.key}")
            # lets test encrypting something
            test_msg = "welcome to evildojo"
            test_msg_bytes = test_msg.encode("utf-8")
            f = Fernet(self.key)
            encrypted_msg = f.encrypt(test_msg_bytes)
            print_info(f"Encrypted message: {encrypted_msg}")
            print_info("Sending encrypted message to client")
            writer.write(encrypted_msg)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error decrypting key: {e}")

    async def pushkey_to_bot(self, cmd_parts):
        if not self.is_master:
            print_error("Only master can receive pushkey command")
            return
        if len(cmd_parts) < 3:
            print_error("pushkey command requires host and port")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])
        try:
            reader, writer = await asyncio.open_connection(host, port)
            msg = f"pullkey {self.crypto}"
            writer.write(msg.encode("utf8"))
            await writer.drain()
            default_read_size = 1024
            response = await reader.read(default_read_size)
            decoded_response = response.decode("utf8")
            print_info(f"Received: {decoded_response}")
            f = Fernet(self.key)
            decrypted_response = f.decrypt(response)
            print_info(f"Decrypted response: {decrypted_response}")
            if decrypted_response == b"welcome to evildojo":
                print_success("Message acknowledged!")
                # at this point, we can probably exchange virtual address information
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")


class RedKingBotMaster(RedKingBot):
    def __init__(self, port):
        super().__init__(port)
        self.is_master = True
        self.crypto = None
        self.pub = None
        self.pubkey = b"-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCNVXuPwxPKJiT+fIOJdbZpSKMeovOuiN68Ckx+9VMGM3UfsDv/553ccqQB\nZP/M+CgNyTdCXXgWeM15bktLvsgdAgMBAAE=\n-----END RSA PUBLIC KEY-----"

    def init_aes_key(self):
        if not self.is_initialized():
            print_info("Initializing AES key")
            self.key = Fernet.generate_key()
            self.pub = rsa.PublicKey.load_pkcs1(self.pubkey)
            self.crypto = rsa.encrypt(self.key, self.pub)
            self.crypto = base64.b64encode(self.crypto).decode("utf-8")
            print_info(f"Initialized AES key: {self.key}")
