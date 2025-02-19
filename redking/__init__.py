import random
import asyncio
from cryptography.fernet import Fernet
import rsa
import base64
import rich

# import sys


def print_info(msg):
    rich.print(f":pizza: {msg}")
    # print(f"🍕 {msg}")


def print_success(msg):
    rich.print(f":thumbs_up: {msg}")
    # print(f"👍 {msg}")


def print_error(msg):
    rich.print(f":pile_of_poo: {msg}")
    # print(f"💩 {msg}")


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
        self.neighbor_neighbors = {}
        self.seed = seed
        random.seed(self.seed)
        self.test_msg = generate_random_str().encode("utf-8")
        self.server_coroutine = None
        print_info(f"Initialized with virtual address {self.virtual_address}")

    def is_initialized(self):
        return self.key is not None

    async def run_server(self):
        print_info(f"Running server on port {self.port}")
        self.server = await asyncio.start_server(
            self.handle_client, "localhost", self.port
        )
        async with self.server:
            try:
                await self.server.serve_forever()
            except Exception as e:
                print_error(f"Error running server: {e}")
            # await self.server.start_serving() # does this return a coroutine?
        self.server.close()
        await self.server.wait_closed()

    async def handle_client(self, reader, writer):
        # print_info("Handling client")
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
                bad_requests += 1
                if bad_requests > 3:
                    print_error(f"Closing connection to {c_host}")
                    break
                continue
            if request in exit_commands:
                print_info(f"Received exit command from {c_host}")
                writer.close()
                await writer.wait_closed()
                # cancel the server coroutine
                self.server.close()
                await self.server.wait_closed()
            else:
                bad_requests = 0
                # await self.handle_request(request, reader, writer)
                await self.handle_request(request, writer)
        writer.close()
        await writer.wait_closed()

    # async def handle_request(self, request, reader, writer):
    async def handle_request(self, request, writer):
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
        # print_info(f"Received command: {cmd}")
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
        elif cmd == "list_neighbors":
            await self.list_neighbors(writer)
        elif cmd == "get_list_neighbors":
            await self.get_list_neighbors(cmd_parts, writer)
        elif cmd == "check_for_swap":
            await self.check_for_swap(writer)
        elif cmd == "swap":
            await self.handle_swap(cmd_parts, writer)
            # print_info("Received swap command")
            # if len(cmd_parts) < 2:
            #    print_error("swap command requires virtual address")
            #    return
            # va = float(cmd_parts[1])
            # self.perform_swap_by_va(va)
            # writer.write("Virtual address saved\n".encode("utf-8"))
            # await writer.drain()
            # writer.close()
            # await writer.wait_closed()
        else:
            print_error("Unrecognized command")
        # print_info("End of handle_command")
        writer.close()
        await writer.wait_closed()

    async def handle_swap(self, cmd_parts, writer):
        print_info("Received swap command")
        if len(cmd_parts) < 2:
            print_error("swap command requires virtual address")
            return
        va = None
        try:
            va = float(cmd_parts[1])
        except Exception as e:
            print_error(f"Invalid virtual address: {e}")
            return
        self.perform_swap_by_va(va)
        writer.write("Virtual address saved\n".encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    def perform_swap_by_va(self, va):
        # given va, find the neighbor with the matching va
        neighbor = None
        for n in self.neighbors:
            neighbor_info = self.neighbors[n]
            if neighbor_info["virtual_address"] == va:
                neighbor = neighbor_info
                break
        if not neighbor:
            print_error(f"No neighbor found with virtual address: {va}")
            return
        host = neighbor["host"]
        port = neighbor["port"]
        self.perform_local_swap(host, port)

    def perform_local_swap(self, host, port):
        if not host or not port:
            print_error("Invalid host or port")
            return False
        if len(host) == 0:
            print_error("Empty host")
            return False
        if port == 0:
            print_error("Invalid port")
            return False
        hostport = f"{host}:{port}"
        neighbor = self.neighbors.get(hostport)
        if not neighbor:
            print_error(f"No neighbor found for {hostport}")
            return False
        neighbor_va = neighbor.get("virtual_address")
        if not neighbor_va:
            print_error(f"No virtual address found for {hostport}")
            return False
        # swap the virtual addresses
        print_info(f"Swapping virtual addresses with {hostport}...")
        # our old virtual address
        tmp_va = self.virtual_address
        # our virtual address is now the neighbor's virtual address
        self.virtual_address = neighbor_va
        # we update our local map with the new virtual address
        neighbor["virtual_address"] = tmp_va
        self.neighbors[hostport] = neighbor
        # we also need to update our own entry in our local map of the neighbor's own neighbor's list
        their_neighbors = self.neighbor_neighbors.get(hostport)
        # updating
        if their_neighbors:
            their_neighbors_copy = their_neighbors.copy()
            # im not sure this is what we want to do...
            # oh right it is but the swap should def only occur for one of these neighbors
            for n in their_neighbors_copy:
                neighbor_info = their_neighbors_copy[n]
                va = neighbor_info["virtual_address"]
                # if the neighbor of our neighbor is us, we need to update THAT virtual address
                if va == tmp_va:
                    print_info(
                        f"Found a neighbor equal to ourself, updating map from {va} to {self.virtual_address}"
                    )
                    neighbor_info["virtual_address"] = self.virtual_address
                    their_neighbors[n] = neighbor_info
            # at the very end, we update our local map of the neighbor's own neighbor's list
            self.neighbor_neighbors[hostport] = their_neighbors
            return True
            # print_info(f"Virtual address is now {self.virtual_address}")
        else:
            print_error(f"No their_neighbors found for {hostport}")
        return False

    async def check_for_swap(self, writer):
        # this assumes you have all the neighbors
        # and their neighbors
        # and their virtual addresses
        # if len(cmd_parts) < 3:
        #    print_error("check_for_swap command requires host and port")
        #    return
        hostport = random.choice(list(self.neighbors.keys()))
        host, port = hostport.split(":")
        port = int(port)
        # hostport = f"{host}:{port}"
        neighbor = self.neighbors.get(hostport)
        if not neighbor:
            print_error(f"The requested hostport is not a neighbor: {hostport}")
            return
        their_neighbors = self.neighbor_neighbors.get(hostport)
        if not their_neighbors:
            print_error(f"The requested neighbor has no neighbors: {hostport}")
            return
        # print_info(f"{hostport} neighbors: {their_neighbors}")
        # now with our neighbors, and THEIR neighbors...
        d1 = 1.0
        d2 = 1.0
        a = self.virtual_address
        b = neighbor["virtual_address"]
        print_info(f"Checking swap between {a} and {b}")
        print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in self.neighbors:
            va = self.neighbors[n]["virtual_address"]
            d1 *= abs(a - va)
        print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in their_neighbors:
            va = their_neighbors[n]["virtual_address"]
            d1 *= abs(b - va)
        print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in self.neighbors:
            va = self.neighbors[n]["virtual_address"]
            if b == va:
                continue
            d2 *= abs(b - va)
        print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in their_neighbors:
            va = their_neighbors[n]["virtual_address"]
            if a == va:
                continue
            d2 *= abs(a - va)
        # we have calculated our d1 and d2
        # now we need to check if we should swap
        print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        if d2 <= d1:
            # actually implement the swap
            # we have to do more than simply swap the virtual addresses
            # we will also have to update our neighbors list
            swap_result = self.perform_local_swap(host, port)
            # we need to send a command to host:port to swap their virtual address with our old one
            if swap_result:
                await self.perform_remote_swap(host, port, a)
                outstr = f"Swapping {a} with {b}\n"
                # print_info(outstr)
                writer.write(outstr.encode("utf-8"))
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            # swap vaddr's (to-be implemented)
        else:
            swap_probability = d1 / d2
            if swap_probability == 0:
                print_info("No swap required")
                return
            # print_info(f"Swap probability: {swap_probability}")
            random_num = random.random()
            # print_info(f"Random number: {random_num}")
            if random_num < swap_probability:
                swap_result = self.perform_local_swap(host, port)
                if swap_result:
                    await self.perform_remote_swap(host, port, a)
                    outstr = f"Swapping {a} with {b}\n"
                    writer.write(outstr.encode("utf-8"))
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()

    async def perform_remote_swap(self, host, port, va):
        if not host or not port:
            print_error("Invalid host or port")
            return
        if len(host) == 0:
            print_error("Empty host")
            return
        if port == 0:
            print_error("Invalid port")
            return
        # reader = None
        writer = None
        try:
            _, writer = await asyncio.open_connection(host, port)
            # send the swap command
            msg = f"swap {va}"
            writer.write(msg.encode("utf8"))
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")
            return

    async def get_list_neighbors(self, cmd_parts, writer):
        print_info(f"Received get_list_neighbors request")
        if len(cmd_parts) < 3:
            print_error("get_list_neighbors command requires host and port")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])
        print_info(f"Connecting to {host}:{port}")
        reader2 = None
        writer2 = None
        try:
            reader2, writer2 = await asyncio.open_connection(host, port)
            # send the list_neighbors request to the neighbor
            writer2.write("list_neighbors".encode("utf-8"))
            await writer2.drain()
            response = await reader2.read(1024)
            print_info(f"Received: [{response}]")
            neighbor_list = response.decode("utf-8")
            # we should probably ship/receive the neighbors list as a JSON for easier serialization etc
            neighbors = neighbor_list.split("\n")
            for neighbor in neighbors:
                if len(neighbor) == 0:
                    continue
                print_info(f"Neighbor: {neighbor}")
                neighbor_parts = neighbor.split(":")
                if len(neighbor_parts) < 3:
                    print_error(f"Invalid neighbor: {neighbor}")
                    continue
                neighbor_host = neighbor_parts[0]
                print_info(f"Neighbor host: {neighbor_host}")
                if len(neighbor_host) == 0:
                    print_error(f"Invalid neighbor host: {neighbor_host}")
                    continue
                neighbor_port = neighbor_parts[1]
                if len(neighbor_port) == 0:
                    print_error(f"Invalid neighbor port: {neighbor_port}")
                    continue
                neighbor_port = int(neighbor_port)
                print_info(f"Neighbor port: {neighbor_port}")
                neighbor_va = neighbor_parts[2]
                if not neighbor_va:
                    print_error(f"Invalid neighbor virtual address: {neighbor_va}")
                    continue
                neighbor_va = neighbor_va.strip()
                if len(neighbor_va) == 0:
                    print_error(f"Invalid neighbor virtual address: {neighbor_va}")
                    continue
                # print_info(
                #    f"Neighbor virtual address before float conversion: {neighbor_va}"
                # )
                if not neighbor_va:
                    print_error(f"Invalid neighbor virtual address: {neighbor_va}")
                    continue
                neighbor_va = float(neighbor_va)
                print_info(f"Neighbor virtual address: {neighbor_va}")
                # this is a "neighbor of neighbors"
                # check if the neighbor exists
                hostport = f"{neighbor_host}:{neighbor_port}"
                neighbor2 = self.neighbor_neighbors.get(hostport)
                if not neighbor2:
                    new_neighbor = {
                        "host": neighbor_host,
                        "port": neighbor_port,
                        "virtual_address": neighbor_va,
                    }
                    neighbor_neighbors = self.neighbor_neighbors.get(hostport)
                    if not neighbor_neighbors:
                        self.neighbor_neighbors[hostport] = {}
                    new_hostport = f"{neighbor_host}:{neighbor_port}"
                    if new_hostport not in self.neighbor_neighbors[hostport]:
                        print_info(f"Adding neighbor of neighbor: {new_hostport}")
                        self.neighbor_neighbors[hostport][new_hostport] = new_neighbor
                    else:
                        print_info(
                            f"Neighbor of neighbor already exists: {new_hostport}"
                        )
                        # update it anyway
                        print_info(f"Adding neighbor of neighbor: {new_hostport}")
                        self.neighbor_neighbors[hostport][new_hostport] = new_neighbor
                    print_info(
                        f"Neighbor of neighbor added: {self.neighbor_neighbors[hostport]}"
                    )
                else:
                    print_info(f"Neighbor of neighbor already exists: {neighbor2}")
            # writer.write("Neighbor list received\n".encode("utf-8"))
            writer.write(response)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Exception in get_list_neighbors: {e}")
            return

    async def list_neighbors(self, writer):
        print_info(f"Received list_neighbors request")
        # print_info(f"Neighbors: {self.neighbors}")
        neighbors_str = (
            "\n".join(
                [f"{k}:{v['virtual_address']}" for k, v in self.neighbors.items()]
            )
            + "\n"
        )
        writer.write(neighbors_str.encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def handle_add_neighbor(self, cmd_parts, writer):
        if len(cmd_parts) < 3:
            print_error("add_neighbor command requires host and port")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])
        self.add_neighbor(host, port)
        writer.write("Neighbor added\n".encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def get_vaddr(self, writer):
        print_info(f"Received vaddr request")
        print_info(f"My virtual address: {self.virtual_address}")
        # convert the virtual address to hex
        hex_va = self.virtual_address.hex()
        print_info(f"Hex virtual address: {hex_va}")
        # base64
        b64_va = base64.b64encode(hex_va.encode("utf-8")).decode("utf-8")
        print_info(f"Base64 virtual address: {b64_va}")
        writer.write(b64_va.encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def get_vaddr_from(self, cmd_parts, writer):
        print_info(f"get_vaddr_from")
        if len(cmd_parts) < 3:
            print_error("get_vaddr command requires host")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])
        print_info(f"Connecting to {host}:{port}")
        reader2 = None
        writer2 = None
        try:
            reader2, writer2 = await asyncio.open_connection(host, port)
            # send the virtual address request to the neighbor
            # is reader2 being closed early?
            # await self.send_msg(writer2, "vaddr")
            writer2.write("vaddr".encode("utf-8"))
            await writer2.drain()
            # response = await self.receive_msg(reader2)
            response = await reader2.read(1024)
            print_info(f"Received: {response}")
            # decode the base64 response
            response = base64.b64decode(response).decode("utf-8")
            # convert the hex virtual address to float
            va = float.fromhex(response)
            print_info(f"Received virtual address: {va}")
            # save the virtual address
            # check if the neighbor exists
            hostport = f"{host}:{port}"
            neighbor = self.neighbors.get(hostport)
            if not neighbor:
                print_error(f"No neighbor found for host {hostport}")
                return
            neighbor["virtual_address"] = va
            self.neighbors[hostport] = neighbor
            print_info(f"Neighbor virtual address saved: {neighbor}")
            # await self.send_msg(writer, "Virtual address saved\n")
            writer.write("Virtual address saved\n".encode("utf-8"))
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Exception in get_vaddr_from: {e}")
            return
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
        writer.write(msg.encode("utf8"))
        await writer.drain()
        default_read_size = 1024
        response = await reader.read(default_read_size)
        writer.close()
        await writer.wait_closed()
        print_info(f"Response: {response}")
        # decoded_response = response.decode("utf8")
        # response = await self.receive_msg(reader)
        f = Fernet(self.key)
        decrypted_response = None
        try:
            decrypted_response = f.decrypt(response)
        except Exception as e:
            print_error(f"Error decrypting response: {e}")
            return
        print_info(f"Decrypted response: {decrypted_response}")
        if decrypted_response == self.test_msg:
            print_success("Message acknowledged!")
            # lets start by saving the host and port
            self.add_neighbor(host, port)
        else:
            print_error("Message rejected")
        print_info("End of pushkey_to_bot")

    def add_neighbor(self, host, port):
        hostport = f"{host}:{port}"
        neighbor = self.neighbors.get(hostport)
        if neighbor:
            print_info(f"Neighbor already exists: {neighbor}")
            return
        self.neighbors[hostport] = {"host": host, "port": port, "virtual_address": None}
        print_info(f"Neighbor added: {self.neighbors[hostport]}")


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
