import random
import time

# import math
import asyncio
from cryptography.fernet import Fernet
import rsa
import base64
import rich
from rich.tree import Tree
from datetime import datetime
import json


def print_info(msg):
    # curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rich.print(f":pizza: {msg}")
    # rich.print(f":pizza: {curtime} {msg}")


def print_success(msg):
    # curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rich.print(f":thumbs_up: {msg}")
    # rich.print(f":thumbs_up: {curtime} {msg}")


def print_error(msg):
    # curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rich.print(f":pile_of_poo: {msg}")
    # rich.print(f":pile_of_poo: {curtime} {msg}")


def print_fatal(msg):
    # curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rich.print(f":skull: {msg}")
    # rich.print(f":skull: {curtime} {msg}")


def print_todo(msg):
    # curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rich.print(f":construction: {msg}")
    # rich.print(f":construction: {curtime} {msg}")


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
        self.pub = None
        self.crypto = None
        self.port = port
        self.priv = rsa.PrivateKey.load_pkcs1(self.private_key_bytes)
        self.neighbors = {}
        self.neighbor_neighbors = {}
        self.seed = seed
        random.seed(self.seed)
        # self.test_msg = generate_random_str().encode("utf-8")
        self.test_msg = generate_random_str()
        self.server_coroutine = None
        self.total_swaps = 0
        print_info(f"Initialized with virtual address {self.virtual_address}")
        print_info(f"Initialized with test message: {self.test_msg}")
        self.tree = Tree(str(self.virtual_address))

    def is_initialized(self):
        return self.key is not None

    async def run_server(self):
        print_info(f"Running server on port {self.port}")
        self.server = await asyncio.start_server(
            self.handle_client, "localhost", self.port
        )
        async with self.server:
            try:
                print_info("Server started")
                await self.server.serve_forever()
            except Exception as e:
                print_error(f"Error running server: {e}")
        self.server.close()
        await self.server.wait_closed()

    async def handle_client(self, reader, writer):
        # c_extra_info = writer.get_extra_info("peername")
        # c_host = c_extra_info[0]
        # print_info(f"Connected to {c_host}")
        default_read_size = 1024
        request = await reader.read(default_read_size)
        await self.handle_request(request, writer)
        writer.close()
        await writer.wait_closed()

    def check_if_encrypted_request(self, request):
        if not request:
            print_error("No request received")
            return None
        if len(request) == 0:
            print_error("Empty request")
            return None
        # at this point, we can assume the request is not empty
        # so we can attempt to decode it the same way the test message gets decoded
        decrypted_request = None
        try:
            assert self.key
            f = Fernet(self.key)
            decrypted_request = f.decrypt(request)
        except Exception as e:
            print_error(f"Error decrypting request: {e}")
            return None
        try:
            decrypted_request = decrypted_request.decode("utf-8")
        except Exception as e:
            print_error(f"Error decoding decrypted request: {e}")
            return None
        return decrypted_request

    def check_if_signed_request(self, request):
        if not request:
            print_error("No request received")
            return None
        if len(request) == 0:
            print_error("Empty request")
            return None
        # at this point, we can assume the request is not empty
        # so we can attempt to decode it the same way the AES key gets decoded
        encrypted_request = None
        try:
            encrypted_request = base64.b64decode(request)
        except Exception as e:
            print_error(f"Error decoding request: {e}")
            return None
        decrypted_request = None
        try:
            decrypted_request = rsa.decrypt(encrypted_request, self.priv)
        except Exception as e:
            print_error(f"Error decrypting request: {e}")
            return None
        try:
            decrypted_request = decrypted_request.decode("utf-8")
        except Exception as e:
            print_error(f"Error decoding decrypted request: {e}")
            return None
        return decrypted_request

    async def handle_request(self, request, writer):
        if not writer:
            print_error("No writer received")
            return
        if not request:
            # print_error("No request received")
            return
        print_info(f"Received request: {request}")
        # check if the request is signed
        if not self.is_master:
            # check to see if we are initialized
            if not self.is_initialized():
                print_info("Bot is not initialized")
                # check for signed request anyway in case it is a pushkey from the master
                signed_request = self.check_if_signed_request(request)
                if signed_request and signed_request[:2] == "pk":
                    command_parts = signed_request.split(" ")
                    await self.handle_command(command_parts, writer)
                    return
                # receive the raw request
                request = request.decode("utf-8")
                command_parts = request.split(" ")
                await self.handle_command(command_parts, writer)
                return
            signed_request = self.check_if_signed_request(request)
            decrypted_request = self.check_if_encrypted_request(request)
            if not signed_request and not decrypted_request:
                print_error("Invalid request: isn't RSA signed or AES encrypted")
                return
            if signed_request and signed_request[:2] == "pk":
                # print_todo(f"TODO: Implement pushkey from master")
                command_parts = signed_request.split(" ")
                await self.handle_command(command_parts, writer)
                return
            if decrypted_request:
                print_info(f"Decrypted request: {decrypted_request}")
                command_parts = decrypted_request.split(" ")
                await self.handle_command(command_parts, writer)
                return
            print_error(f"Unhandled signed request received: {signed_request}")
            return
        elif self.is_master:
            # check for decrypted request
            decrypted_request = self.check_if_encrypted_request(request)
            if decrypted_request:
                print_info(f"Decrypted request: {decrypted_request}")
                command_parts = decrypted_request.split(" ")
                await self.handle_command(command_parts, writer)
                return
            request = request.decode("utf-8")
            command_parts = request.split(" ")
            if not command_parts:
                print_error("No command parts")
                return
            await self.handle_command(command_parts, writer)

    async def handle_command(self, cmd_parts, writer):
        cmd = cmd_parts[0].strip()
        # first of all, only the master can receive 'raw' commands
        print_info(f"Received command: {cmd}")
        if len(cmd) == 0:
            print_error("Empty command")
        elif cmd == "send_raw_ping":
            await self.send_raw_ping(cmd_parts, writer)
        elif cmd == "send_aes_ping":
            await self.send_aes_ping(cmd_parts, writer)
        elif cmd == "ping":
            await self.send_aes_pong(writer)
        elif cmd == "pong":
            await self.send_aes_pong(writer)
        elif cmd == "pushkey":
            await self.pushkey_to_bot(cmd_parts)
        elif cmd == "pk":
            await self.pullkey_from_master(cmd_parts, writer)
        elif cmd == "vaddr":
            await self.get_vaddr(writer)
        elif cmd == "get_vaddr":
            await self.get_vaddr_from(cmd_parts, writer)
        elif cmd == "add_neighbor":
            await self.handle_add_neighbor(cmd_parts, writer)
            await self.get_vaddr_from(cmd_parts, writer)
        elif cmd == "send_add_neighbor":
            await self.handle_send_add_neighbor(cmd_parts, writer)
        elif cmd == "list_neighbors":
            await self.list_neighbors(writer)
        elif cmd == "get_list_neighbors":
            await self.get_list_neighbors(cmd_parts, writer)
        elif cmd == "check_for_swap":
            await self.check_for_swap(writer)
        elif cmd == "swap":
            await self.handle_swap(cmd_parts, writer)
        else:
            print_error("Unrecognized command")
        try:
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error closing writer: {e}")

    async def handle_send_add_neighbor(self, cmd_parts, writer):
        if len(cmd_parts) < 5:
            print_error("send_add_neighbor command requires host and port")
            return
        send_host = cmd_parts[1]
        send_port = int(cmd_parts[2])
        add_host = cmd_parts[3]
        add_port = int(cmd_parts[4])
        # send the add_neighbor command to the bot
        # we have to encrypt this message with the AES key
        assert self.key
        f = Fernet(self.key)
        msg = f"add_neighbor {add_host} {add_port}"
        encrypted_msg = f.encrypt(msg.encode("utf-8"))
        # open a connection to the bot
        reader = None
        writer2 = None
        try:
            reader, writer2 = await asyncio.open_connection(send_host, send_port)
            writer2.write(encrypted_msg)
            await writer2.drain()
            DEFAULT_READ_SIZE = 1024
            response = await reader.read(DEFAULT_READ_SIZE)
            print_info(f"Received: {response}")
            writer.write(response)
            # await writer.drain()
            # writer.close()
            # await writer.wait_closed()
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")

    async def send_raw_pong(self, writer):
        print_info("Sending raw pong")
        writer.write("pong\n".encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def send_aes_pong(self, writer):
        print_info("Sending AES-encrypted pong")
        if not self.is_initialized():
            print_error("Bot is not initialized...sending raw pong")
            await self.send_raw_pong(writer)
            return
        assert self.key
        f = Fernet(self.key)
        msg = "pong".encode("utf-8")
        encrypted_msg = f.encrypt(msg)
        writer.write(encrypted_msg)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    # send_aes_ping <host> <port>
    # sends an AES-encrypted ping to the given host and port and waits for a response
    # only works if the bot is initialized with an AES key
    async def send_aes_ping(self, cmd_parts, writer):
        if not self.is_initialized():
            print_error("Bot is not initialized")
            return
        if len(cmd_parts) < 3:
            print_error("send_ping command requires host and port")
            return
        host = cmd_parts[1]
        port = cmd_parts[2]
        reader = None
        writer2 = None
        try:
            port = int(port)
            reader, writer2 = await asyncio.open_connection(host, port)
            assert self.key
            f = Fernet(self.key)
            msg = "ping".encode("utf-8")
            encrypted_msg = f.encrypt(msg)
            writer2.write(encrypted_msg)
            await writer2.drain()
            response = await reader.read(1024)
            print_info(f"Received: {response}")
            # decrypt the response
            decrypted_response = f.decrypt(response)
            print_info(f"Decrypted response: {decrypted_response}")
            writer.write(decrypted_response)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")

    # send_raw_ping <host> <port>
    # sends a ping to the given host and port and waits for a response
    # only works if the bot is not initialized with an AES key
    async def send_raw_ping(self, cmd_parts, writer):
        if len(cmd_parts) < 3:
            print_error("send_ping command requires host and port")
            return
        host = cmd_parts[1]
        port = cmd_parts[2]
        reader = None
        writer2 = None
        try:
            port = int(port)
            reader, writer2 = await asyncio.open_connection(host, port)
            writer2.write("ping".encode("utf-8"))
            await writer2.drain()
            response = await reader.read(1024)
            print_info(f"Received: {response}")
            writer.write(response)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")

    # swap <virtual address>
    # swaps our virtual address with the neighbor's virtual address
    async def handle_swap(self, cmd_parts, writer):
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
        # for some reason, we might hit this even if all nodes are connected to this node, not sure why...
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
        # our old virtual address
        tmp_va = self.virtual_address
        # our virtual address is now the neighbor's virtual address
        self.virtual_address = neighbor_va
        # we update our local map with the new virtual address
        neighbor["virtual_address"] = tmp_va
        # print_info(f"Swapped {tmp_va} with {neighbor_va}")
        self.total_swaps += 1
        rich.console.Console().clear()
        print_info(
            f"Virtual address is now {self.virtual_address:.8f}. Total swaps: {self.total_swaps}"
        )
        # rich.print(self.tree)
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
                    # print_info(
                    #    f"Found a neighbor equal to ourself, updating map from {va} to {self.virtual_address}"
                    # )
                    neighbor_info["virtual_address"] = self.virtual_address
                    their_neighbors[n] = neighbor_info
            # at the very end, we update our local map of the neighbor's own neighbor's list
            self.neighbor_neighbors[hostport] = their_neighbors
            # nice printing
            tree = Tree(str(self.virtual_address))
            for n in self.neighbors:
                neighbor_info = self.neighbors[n]
                va = neighbor_info["virtual_address"]
                tree.add(str(va))
            rich.print(tree)
            return True
        else:
            print_error(f"No their_neighbors found for {hostport}")
        return False

    # check_for_swap
    # checks to see if we should swap with a neighbor and if so, do so
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
        # print_info(f"Checking swap between {a} and {b}")
        # print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        # this should be a more efficient calculation than the previous code
        # but it has yet to be tested...
        # a_ns = [float(self.neighbors[n]["virtual_address"]) for n in self.neighbors]
        # b_ns = [float(their_neighbors[n]["virtual_address"]) for n in their_neighbors]
        # a_ns.remove(a)
        # b_ns.remove(b)
        # d1 = math.prod([abs(a - va) * abs(b - va) for va in a_ns])
        # d2 = math.prod([abs(b - va) * abs(a - va) for va in b_ns])
        for n in self.neighbors:
            va = float(self.neighbors[n]["virtual_address"])
            if a == va:
                continue
            d1 *= abs(a - va)
        # print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in their_neighbors:
            va = float(their_neighbors[n]["virtual_address"])
            if b == va:
                continue
            d1 *= abs(b - va)
        # print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in self.neighbors:
            va = float(self.neighbors[n]["virtual_address"])
            if b == va:
                continue
            d2 *= abs(b - va)
        # print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
        for n in their_neighbors:
            va = float(their_neighbors[n]["virtual_address"])
            if a == va:
                continue
            d2 *= abs(a - va)
        # we have calculated our d1 and d2
        # now we need to check if we should swap
        # print_info(f"d1: {d1:>10.10f} d2: {d2:>10.10f}")
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
            # we are going to want to encrypt this message
            writer.write(msg.encode("utf8"))
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print_error(f"Error connecting to bot: {e}")
            return

    # get_list_neighbors <host> <port>
    # this function actually attempts to open a new connection to the given host and port
    # and return their list of neighbors
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

    # list_neighbors
    # returns a list of neighbors
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

    # add_neighbor <host> <port>
    # adds a neighbor to the list of neighbors
    async def handle_add_neighbor(self, cmd_parts, writer):
        if len(cmd_parts) < 3:
            print_error("add_neighbor command requires host and port")
            return
        host = cmd_parts[1]
        port = int(cmd_parts[2])
        self.add_neighbor(host, port, writer)
        # writer.write("Neighbor added\n".encode("utf-8"))
        # writer.write("OK\n".encode("utf-8"))
        # await writer.drain()
        # writer.close()
        # await writer.wait_closed()

    # vaddr
    # returns the virtual address
    async def get_vaddr(self, writer):
        print_info(f"Received vaddr request")
        print_info(f"My virtual address: {self.virtual_address}")
        # convert the virtual address to hex
        hex_va = self.virtual_address.hex()
        print_info(f"Hex virtual address: {hex_va}")
        # base64
        b64_va = base64.b64encode(hex_va.encode("utf-8")).decode("utf-8")
        print_info(f"Base64 virtual address: {b64_va}")

        # encrypt the virtual address
        assert self.key
        f = Fernet(self.key)
        encrypted_b64_va = f.encrypt(b64_va.encode("utf-8"))
        writer.write(encrypted_b64_va)
        # writer.write(b64_va.encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    # get_vaddr <host> <port>
    # gets the virtual address from the given host and port
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
            # encrypt the 'vaddr' command
            msg = "vaddr".encode("utf-8")
            assert self.key
            f = Fernet(self.key)
            encrypted_msg = f.encrypt(msg)
            writer2.write(encrypted_msg)
            # writer2.write("vaddr".encode("utf-8"))
            await writer2.drain()
            # response = await self.receive_msg(reader2)
            response = await reader2.read(1024)
            print_info(f"Received: {response}")
            # decrypt the response
            try:
                response = f.decrypt(response)
                print_info(f"Decrypted response: {response}")
            except Exception as e:
                print_error(f"Error decrypting response: {e}")
                await writer2.drain()
                writer2.close()
                await writer2.wait_closed()
                return

            response = response.decode("utf-8")
            base64_va = response
            print_info(f"Base64 virtual address: {base64_va}")
            # decode the base64 response
            decoded_response = base64.b64decode(response).decode("utf-8")
            print_info(f"Decoded response: {decoded_response}")
            # convert the hex virtual address to float
            # va = float.fromhex(response)
            # va = float.fromhex(response)
            va = float.fromhex(decoded_response)
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
            # writer.write("Virtual address saved\n".encode("utf-8"))
            writer.write(f"{va}\n".encode("utf-8"))
            # writer.write("OK\n".encode("utf-8"))
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

    # pullkey <encrypted_key>
    # receives the encrypted key from the master
    async def pullkey_from_master(self, cmd_parts, writer):
        if self.is_master:
            print_error("Only bot can receive pullkey command")
            return
        encrypted_key = cmd_parts[1]
        print_info(f"Received key: [{encrypted_key}]")
        aes_key = encrypted_key.encode("utf-8")
        try:
            self.key = aes_key
            f = Fernet(self.key)
            test_msg_bytes = self.test_msg.encode("utf-8")
            encrypted_msg = f.encrypt(test_msg_bytes)
            print_info(f"Encrypted message: {encrypted_msg}")
            print_info("Sending encrypted message to client")
            writer.write(encrypted_msg)
        except Exception as e:
            print_error(f"Error setting key: {e}")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print_info("End of pullkey_from_master")

    # pushkey <host> <port>
    # sends the encrypted key to the bot
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
        if not reader or not writer:
            print_error("No reader or writer")
            return
        # send the key to the bot
        # we will sign this message
        assert self.key
        decoded_key = self.key.decode("utf-8")
        msg = f"pk {decoded_key}"
        print_info(f"Message before base64 encoding: {msg}")
        msg = msg.encode("utf-8")
        # base64 encode the message
        # msg = base64.b64encode(msg.encode("utf-8")).decode("utf-8")
        # msg = f"pullkey {self.crypto}"
        # we can actually sign this message as well
        if self.pub:
            signed_msg = rsa.encrypt(msg, self.pub)
            # base64_signed_msg = base64.b64encode(signed_msg).decode("utf-8")
            base64_signed_msg = base64.b64encode(signed_msg)
            print_info(f"Sending signed message: {base64_signed_msg}")
            writer.write(base64_signed_msg)
            await writer.drain()
            default_read_size = 1024
            response = await reader.read(default_read_size)
            print_info(f"Response: {response}")
            # decoded_response = response.decode("utf8")
            try:
                f = Fernet(self.key)
                decrypted_response = f.decrypt(response)
                print_info(f"Decrypted response: {decrypted_response}")
                decrypted_response = decrypted_response.decode("utf-8")
                if decrypted_response == self.test_msg:
                    print_success("Message acknowledged!")
                else:
                    print_error("Message rejected")
            except Exception as e:
                print_error(f"Error decrypting response: {e}")
                return
            try:
                await writer.drain()
            except Exception as e:
                print_error(f"Error draining writer: {e}")
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print_error(f"Error closing writer: {e}")
            print_info("End of pushkey_to_bot")
        else:
            print_error("No public key found")
        # this is a check to make sure the bot is initialized with the proper seed
        # we can disable this for now
        # decrypted_response = None
        #    # lets start by saving the host and port
        #    self.add_neighbor(host, port)
        # else:
        #    print_error("Message rejected")
        # print_info("End of pushkey_to_bot")

    def add_neighbor(self, host, port, writer):
        # make sure that we do not add ourself
        if host == "localhost" and port == self.port:
            print_error("Cannot add self as neighbor")
            return
        hostport = f"{host}:{port}"
        neighbor = self.neighbors.get(hostport)
        if neighbor:
            print_info(f"Neighbor already exists: {neighbor}")
            error_json = json.dumps(
                {"result": "ERROR", "message": "Neighbor already exists"}
            ).encode("utf-8")
            writer.write(error_json)
            return
        self.neighbors[hostport] = {"host": host, "port": port, "virtual_address": None}
        print_info(f"Neighbor added: {self.neighbors[hostport]}")
        success_json = json.dumps(
            {"result": "SUCCESS", "message": "Neighbor added"}
        ).encode("utf-8")
        writer.write(success_json)


# class RedKingBotMaster(RedKingBot):
#    def __init__(self, port, seed=0):
#        super().__init__(port, seed)
#        self.is_master = True
#        self.crypto = None
#        self.pub = None
#        self.pubkey = b"-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCNVXuPwxPKJiT+fIOJdbZpSKMeovOuiN68Ckx+9VMGM3UfsDv/553ccqQB\nZP/M+CgNyTdCXXgWeM15bktLvsgdAgMBAAE=\n-----END RSA PUBLIC KEY-----"
#
#    def init_aes_key(self):
#        if not self.is_initialized():
#            print_info("Initializing AES key")
#            self.key = Fernet.generate_key()
#            self.pub = rsa.PublicKey.load_pkcs1(self.pubkey)
# self.crypto = rsa.encrypt(self.key, self.pub)
# self.crypto = base64.b64encode(self.crypto).decode("utf-8")
#            print_info(f"Initialized AES key: {self.key}")


class RedkingUDP(asyncio.DatagramProtocol):
    def __init__(self):
        self.start_time = time.time()
        print_info(f"Initializing Redking UDP server")
        self.transport = None
        self.is_master = False
        self.key = None
        # self.server = None
        self.virtual_address = random.uniform(0.0, 1.0)
        self.private_key_bytes = b"-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAI1Ve4/DE8omJP58g4l1tmlIox6i866I3rwKTH71UwYzdR+wO//n\nndxypAFk/8z4KA3JN0JdeBZ4zXluS0u+yB0CAwEAAQJAPAKm42TuWzAVFyVhaJVd\nrZiVAmYoV9xvzqIE1wdtRzbFKVPIXlAfJIoOFb5u+QQ8k96zAC6xbuc9Tl54lLhX\nwQIjAJkluAmy4dW75s63d/rS1hMZ0UI5zXVmHU3pmmBCc83K2fECHwDsQLVSJa7h\nZBcplVu+ld4H2QRS2WJajpfJ667/RO0CIwCUlDGOx0uurtPoLbtrTu1+LogEdkvM\n4DsCAedSCGaNe4YhAh8A1dOrSPJ6Wd1xaV2Zb+HM12WAGExQTI4Kq+L4vGnxAiJ+\n/05NOZ9gfWGFrOHfKI8GIlYPjeDlxud/ZkijKAuO9SjX\n-----END RSA PRIVATE KEY-----"
        self.pub = None
        self.crypto = None
        # self.port = port
        self.priv = rsa.PrivateKey.load_pkcs1(self.private_key_bytes)
        self.neighbors = {}
        self.neighbor_neighbors = {}
        # self.seed = seed
        # random.seed(self.seed)
        # self.test_msg = generate_random_str().encode("utf-8")
        # self.test_msg = generate_random_str()
        # self.server_coroutine = None
        self.total_swaps = 0
        print_info(f"Initialized with virtual address {self.virtual_address}")
        self.name = None
        self.name_locked = False
        # print_info(f"Initialized with test message: {self.test_msg}")
        # self.tree = Tree(str(self.virtual_address))

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        # message = data
        message = data.decode().strip()
        # start_time = time.time()
        signed_message = self.check_if_signed_request(data)
        if signed_message:
            # print_info(f"Received RSA-signed message from {addr}: {signed_message}")
            self.handle_signed_message(signed_message, addr)
        else:
            decrypted_message = self.check_if_encrypted_request(data)
            if decrypted_message:
                # print_info(f"Decrypted message: {decrypted_message}")
                self.handle_encrypted_message(decrypted_message, addr)
            else:
                # print_info(f"Treating as plaintext")
                # print_info(f"Received message from {addr}: {message}")
                # else it is plaintext
                self.handle_plaintext(data, addr)
                # if self.transport:
                #    self.transport.sendto(data, addr)
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print_info(f"Elapsed time: {elapsed_time}")

    def handle_function(self, message, addr):
        # print_info(f"handle_function: {message} {addr}")
        split_msg = message.split(" ")
        cmd = split_msg[0]
        retval = ""
        if cmd == "getname":
            retval = self.handle_getname(addr)
        elif cmd == "setname":
            name = split_msg[1]
            retval = self.handle_setname(name, addr)
        elif cmd == "getkey":
            retval = self.handle_getkey(addr)
        elif cmd == "ping":
            retval = self.handle_ping(addr)
        return retval
        # if self.transport:
        #    self.transport.sendto(return_msg.encode("utf-8"), addr)

    def handle_ping(self, addr):
        return_msg = "pong"
        return return_msg

    def handle_getkey(self, addr):
        return_msg = ""
        if not self.key:
            return_msg = "No key set"
        else:
            return_msg = self.key.decode("utf-8")
        return return_msg
        # if self.transport:
        #    self.transport.sendto(return_msg.encode("utf-8"), addr)

    def handle_setname(self, name, addr):
        return_msg = ""
        if self.name_locked:
            return_msg = "Name locked, cannot change"
        elif not name:
            return_msg = "No name received"
        elif len(name) == 0:
            return_msg = "Empty name"
        else:
            self.name = name
            return_msg = f"Set name to {name}"
        if self.transport:
            self.transport.sendto(return_msg.encode("utf-8"), addr)

    def handle_getname(self, addr):
        name = self.name
        if name is None:
            name = "None"
        name = name.encode("utf-8")
        assert self.transport
        self.transport.sendto(name, addr)

    def handle_encrypted_message(self, message, addr):
        message = message.strip()
        print_info(f"Received encrypted message from {addr}: {message}")
        retval = self.handle_function(message, addr)
        # print_info(f"Return value: {retval}")
        # encrypt the return message
        encrypted_retval = None
        if not self.key:
            print_error("Cannot encrypt, no AES key set")
            return
        try:
            f = Fernet(self.key)
            assert retval
            encrypted_retval = f.encrypt(retval.encode("utf-8"))
        except Exception as e:
            print_error(f"Error encrypting return message: {e}")
            return
        if self.transport:
            self.transport.sendto(encrypted_retval, addr)
        return

    def handle_signed_message(self, message, addr):
        message = message.strip()
        print_info(f"Received signed message from {addr}: {message}")
        retval = self.handle_function(message, addr)
        # sign the return message
        # check to make sure it is less than 53 bytes
        if len(retval) > 53:
            print_error("Return message too long")
            return
        signed_retval = rsa.encrypt(retval.encode("utf-8"), self.priv)
        # print_info(f"signed_retval: {signed_retval}")
        base64_signed_retval = base64.b64encode(signed_retval)
        # print_info(f"base64_signed_retval: {base64_signed_retval}")
        if self.transport:
            self.transport.sendto(base64_signed_retval, addr)
        return

    def handle_plaintext(self, data, addr):
        if not self.is_master:
            print_error("Only master can handle plaintext")
            return

    def error_received(self, exc):
        print_error(f"Error received: {exc}")

    def connection_lost(self, exc):
        print_info("Connection lost")

    def check_if_encrypted_request(self, request):
        # print_info(f"Checking if encrypted request...")
        if not request:
            print_error("No request received")
            return None
        if len(request) == 0:
            print_error("Empty request")
            return None
        # at this point, we can assume the request is not empty
        # so we can attempt to decode it the same way the test message gets decoded
        decrypted_request = None
        if not self.key:
            print_error("Cannot attempt decrypt, no AES key set")
            return None
        try:
            assert self.key
            f = Fernet(self.key)
            decrypted_request = f.decrypt(request)
        except Exception as e:
            # print_error(f"Error decrypting request: {e}")
            return None
        try:
            decrypted_request = decrypted_request.decode("utf-8")
        except Exception as e:
            # print_error(f"Error decoding decrypted request: {e}")
            return None
        return decrypted_request

    def check_if_signed_request(self, request):
        # print_info(f"Checking if signed request...")
        if not request:
            print_error("No request received")
            return None
        if len(request) == 0:
            print_error("Empty request")
            return None
        # at this point, we can assume the request is not empty
        # so we can attempt to decode it the same way the AES key gets decoded
        encrypted_request = None
        try:
            encrypted_request = base64.b64decode(request)
        except Exception as e:
            # print_error(f"Error decoding request: {e}")
            return None
        decrypted_request = None
        try:
            decrypted_request = rsa.decrypt(encrypted_request, self.priv)
        except Exception as e:
            # print_error(f"Error decrypting request: {e}")
            return None
        try:
            decrypted_request = decrypted_request.decode("utf-8")
        except Exception as e:
            # print_error(f"Error decoding decrypted request: {e}")
            return None
        return decrypted_request


class RedkingMasterUDP(RedkingUDP):
    def __init__(self):
        super().__init__()
        self.is_master = True
        self.pubkey = b"-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCNVXuPwxPKJiT+fIOJdbZpSKMeovOuiN68Ckx+9VMGM3UfsDv/553ccqQB\nZP/M+CgNyTdCXXgWeM15bktLvsgdAgMBAAE=\n-----END RSA PUBLIC KEY-----"
        # self.crypto = None
        self.pub = None
        self.init_aes_key()

    def connection_made(self, transport):
        self.transport = transport

    def handle_plaintext(self, data, addr):
        if self.is_master:
            message = data.decode().strip()
            print_info(f"Received plaintext from {addr}: {message}")

    def error_received(self, exc):
        print_error(f"Error received: {exc}")

    def connection_lost(self, exc):
        print_info("Connection lost")

    def init_aes_key(self):
        if not self.key:
            # print_info("Initializing AES key")
            self.key = Fernet.generate_key()
            self.pub = rsa.PublicKey.load_pkcs1(self.pubkey)
            # print_info(f"Initialized AES key: {self.key}")
            print_info(f"Initialized AES key")
