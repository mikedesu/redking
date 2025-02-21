# redking python

This readme needs heavy updating.

## usage:

```
python3 botmaster.py <port> <seed>
python3 botmain.py <port> <seed>

echo "command" | nc localhost <port>
```

See `test1_setup.sh`, `test1.sh`, etc. for examples of interaction at the moment.
The intent is to automate a lot of what is being done there right now.

-----

[![asciicast](https://asciinema.org/a/EhsynoKYncB47vZ678fL5pAo2.svg)](https://asciinema.org/a/EhsynoKYncB47vZ678fL5pAo2)

-----

## Example quick start

In 3 separate terminal sessions:

```
python3 botmaster.py 6661 0
python3 botmain.py 6662 0
python3 botmain.py 6663 0
```

In a 4th terminal session:

```
./test1_setup.sh
./test1.sh
```

-----

## COMMANDS

```
Coming soon...

pushkey
pullkey
vaddr
get_vaddr
list_neighbors
get_list_neighbors
add_neighbor
check_for_swap
swap

...more to come
```

-----

## TODO

- [ ] Only the botmaster should receive raw commands and even then...
  - [ ] Commands sent between botmaster and bot should be optionally encrypted
  - [ ] Commands and info sent between bot and bot should be encrypted
- [ ] Different modes of operation:
    - [ ] "Normal" mode, where certain things can be overridden
    - [ ] "Lockdown" mode, where botmaster becomes a regular bot, all comms are encrypted using irrecoverable keys, and everything runs on full autopilot
    - [ ] etc.
- [ ] We should be able to re-initialize keys, seeds, and other values, and distribute them across the network
- [ ] We should be able to load bots in a way that is "hot reloadable" especially during development
    - [ ] As code is changed, we want to re-load the bot functionality while still sitting on the network or without having to re-attach
- [ ] We should be able to arbitrarily prune nodes off the network and everything update/play together nicely
- [ ] We should seek to perform network initialization especially during testing entirely in Python3 instead of zsh
- [ ] The existing zsh testing scripts and the correlated functionality in the bots should be updated such that construction of networks is easier and allows for adding of arbitrary nodes to arbitrary locations and if the maximum number of neighbors is reached on that node then the connection is passed off to an available neighbor or if yet unavailable continues to search for available neighbors. The adding of new nodes is such that the network can never be "full" unless we introduce that constraint.
    - [ ] 1. At the moment, we have to manually specify both forward and backward links between peers
    - [ ] 2. At the moment, we have to additionally request in both directions:
        - [ ] The vaddr of the peer
        - [ ] The list of neighbors of the peer
    - [ ] Ideally, we can group steps 1 and 2 together into one request
    - [ ] We can save the exchange of neighbor information until after the network is constructed (static network), or we can seek to do it on each node add and then propagate update requests to all nodes: requires updates for the whole network for each new node added (dynamic network)
- [x] Swap calc should select one random neighbor to do the check on instead of manual selection
- [ ] vaddrs should transmit using the base64-hex representation and decode as such
- [ ] Verify nodes have unique addresses
    - [ ] There is a bug here where sometimes it appears a vaddr is shared by one or more nodes on the network
    - [ ] Verify nodes are properly managing their list of neighbors and neighbor-neighbors
- [ ] Be able to distribute code and function updates/additions across the network
- [ ] Remove dependencies on external `rich` library
- [ ] Many other things that I can't think of right now

-----

## contact

- [twitter/x](https://x.com/evildojo666)
- [github](https://github.com/mikedesu)
- [youtube](https://youtube.com/@evildojo666)
