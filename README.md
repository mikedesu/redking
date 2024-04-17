# redking hivemind

## Motivation

- vxunderground black mass volume 1

## Goals

- a client/server framework capable of implementing the RedKing protocol 
- ability to use the network for arbitrary file storage
- ability to use the network for arbitrary file retrieval
- ability to attach custom functionality and distribute it through the network
- ability to encrypt and sign messages distributed through the network
- ability to verify received messages in order to protect against bad actors
- small-world network properties (or N=6 variant)

## Current Work / TODO

- [x] Simple example showing how to map an integer IP address and port combination to a single float64 value
- [ ] Beginning of a node that can act as both the starting server as well as a subsequent connecting node
    - [ ] on node connect to server, both nodes should store the virtual address of its neighbor
    - [ ] threaded so that we can accept new connections while doing other work

## Related Blog Posts

- [The Dream of a Red King — A Connection Protocol for Small-World P2P Botnets](https://medium.com/@moorejacob2017/the-dream-of-a-red-king-a-connection-protocol-for-small-world-p2p-botnets-b64f2eed63f8)

## Social Media

- [Twitter](https://twitter.com/evildojo666)
- [YouTube](https://www.youtube.com/@evildojo666)
- [Twitch](https://www.twitch.tv/evildojo666)
- [Website](https://www.evildojo.com)
