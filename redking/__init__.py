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


def generate_random_str(length=32):
    return "".join(
        random.choices(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length
        )
    )


class RedKingBot:
    def __init__(self, port, seed=0):
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
        self.seed = seed
        random.seed(self.seed)
        self.test_msg = generate_random_str().encode("utf-8")
        print_info(f"Initialized with virtual address {self.virtual_address}")

    def is_initialized(self):
        return self.key is not None

    async def run_server(self):
        print_info(f"Running server on port {self.port}")
        server = await asyncio.start_server(self.handle_client, "localhost", self.port)
        async with server:
            await server.serve_forever()
        server.close()
        await server.wait_closed()

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
                    print_error(f"3 bad requests, closing connection to {c_host}")
                    break
                continue
            print_info(f"Received request: {request} from {c_host}")
            bad_requests = 0
            await self.handle_request(request, reader, writer)
        writer.close()
        await writer.wait_closed()

    async def handle_request(self, request, reader, writer):
        if not writer:
            print_error("No writer received")
            return
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
        await self.handle_command(command_parts, writer)

    async def handle_command(self, cmd_parts, writer):
        cmd = cmd_parts[0]
        print_info(f"Received command: {cmd}")
        # first of all, only the master can receive 'raw' commands
        if len(cmd) == 0:
            print_error("Empty command")
        elif cmd == "pushkey":
            await self.pushkey_to_bot(cmd_parts)
        elif cmd == "pullkey":
            await self.pullkey_from_master(cmd_parts, writer)
        elif cmd == "vaddr":
            await self.get_vaddr(writer)
        elif cmd == "get_vaddr":
            await self.get_vaddr_from(cmd_parts, writer)
        elif cmd == "add_neighbor":
            await self.handle_add_neighbor(cmd_parts, writer)
        else:
            print_error("Unrecognized command")

    async def handle_add_neighbor(self, cmd_parts, writer):
        if len(cmd_parts) < 3:
            print_error("add_neighbor command requires host and port")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])
        self.add_neighbor(host, port)
        writer.write("Neighbor added".encode("utf8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def get_vaddr(self, writer):
        print_info(f"Received vaddr request")
        print_info(f"My virtual address: {self.virtual_address}")
        # convert the virtual address to hex
        hex_va = self.virtual_address.hex()
        print_info(f"Hex virtual address: {hex_va}")
        await self.send_msg(writer, hex_va)

    async def get_vaddr_from(self, cmd_parts, writer):
        if len(cmd_parts) < 2:
            print_error("get_vaddr command requires host")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])

        reader2 = None
        writer2 = None
        try:
            reader2, writer2 = await asyncio.open_connection(host, port)
        except Exception as e:
            print_error(f"Error connecting to neighbor: {e}")
            return

        # send the virtual address request to the neighbor
        msg = "vaddr"
        await self.send_msg(writer2, msg)
        response = await self.receive_msg(reader2)
        print_info(f"Received: {response}")
        # convert the hex virtual address to float
        va = float.fromhex(response)
        print_info(f"Received virtual address: {va}")
        # save the virtual address
        # check if the neighbor exists
        neighbor = self.neighbors.get(host)
        if not neighbor:
            print_error(f"No neighbor found for host {host}")
            return
        neighbor["virtual_address"] = va
        print_info(f"Neighbor virtual address saved: {neighbor}")

        # neighbor = self.neighbors.get(host)
        # if not neighbor:
        #    print_error(f"No neighbor found for host {host}")
        #    return
        # send the virtual address to the client bot
        # va = neighbor.get("virtual_address")
        # if not va:
        #    print_error(f"No virtual address found for host {host}")
        #    return
        # print_info(f"Sending virtual address to {host}")
        # await self.send_msg(writer, va)

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
            f = Fernet(self.key)
            encrypted_msg = f.encrypt(self.test_msg)
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
        reader = None
        writer = None
        try:
            reader, writer = await asyncio.open_connection(host, port)
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")
            return
        # send the encrypted key to the bot
        msg = f"pullkey {self.crypto}"
        await self.send_msg(writer, msg)
        # default_read_size = 1024
        # response = await reader.read(default_read_size)
        # decoded_response = response.decode("utf8")
        response = await self.receive_msg(reader)
        # print_info(f"Received: {decoded_response}")
        f = Fernet(self.key)
        decrypted_response = f.decrypt(response)
        print_info(f"Decrypted response: {decrypted_response}")
        if decrypted_response == self.test_msg:
            print_success("Message acknowledged!")
            # lets start by saving the host and port
            self.add_neighbor(host, port)
            # now we can just ask the neighbor for their virtual address
            print_info("Requesting virtual address from neighbor")
            # at this point, we can probably exchange virtual address information
            # lets just mess around and send a new exchange of messages
            # because the virtual address is a float, we need to convert it to hex
            # hex_va = self.virtual_address.hex()
            # print_info(f"Hex virtual address: {hex_va}")
            # test reconstructing the virtual address
            # this will be proof of readiness for exchange
            # va = float.fromhex(hex_va)
            # print_info(f"Reconstructed virtual address: {va}")
            # we are ready to send to the client bot
            # msg = f"exchange {hex_va}"
            # encrypted_msg = f.encrypt(msg.encode("utf-8"))
            # print_info(f"Messaged to send: {msg}")
            # print_info(f"Sending encrypted message: {encrypted_msg}")
            # self.send_msg(writer, "testing")
        else:
            print_error("Message rejected")
        writer.close()
        await writer.wait_closed()

    def add_neighbor(self, host, port):
        neighbor = self.neighbors.get(host)
        if neighbor:
            print_info(f"Neighbor already exists: {neighbor}")
            return
        self.neighbors[host] = {"host": host, "port": port, "virtual_address": None}
        print_info(f"Neighbor added: {self.neighbors[host]}")

    async def send_msg(self, writer, msg):
        if not writer:
            print_error("No writer received")
            return
        writer.write(msg.encode("utf8"))
        await writer.drain()
        # writer.close()
        # await writer.wait_closed()

    async def receive_msg(self, reader):
        # if not reader:
        #    print_error("No reader received")
        #    return
        default_read_size = 1024
        response = await reader.read(default_read_size)
        decoded_response = response.decode("utf8")
        print_info(f"Received: {decoded_response}")
        return decoded_response


class RedKingBotMaster(RedKingBot):
    def __init__(self, port, seed=0):
        super().__init__(port, seed)
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
