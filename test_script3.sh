

# 6666 = A
# 6667 = B
# 6668 = C

# A <-> B <-> C

# first we have to build the network... 
echo "add_neighbor localhost 6667" | nc localhost 6666; # A <-> B
echo "add_neighbor localhost 6666" | nc localhost 6667; # B <-> A
echo "add_neighbor localhost 6668" | nc localhost 6667; # B <-> C
echo "add_neighbor localhost 6667" | nc localhost 6668; # C <-> B

# then we have to tell each node to get each others vaddr
echo "get_vaddr localhost 6667" | nc localhost 6666; # A <-> B
echo "get_vaddr localhost 6666" | nc localhost 6667; # B <-> A
echo "get_vaddr localhost 6668" | nc localhost 6667; # B <-> C
echo "get_vaddr localhost 6667" | nc localhost 6668; # C <-> B


# then we have to tell each node to get the list of neighbors
echo "get_list_neighbors localhost 6667" | nc localhost 6666; # A <-> B
echo "get_list_neighbors localhost 6666" | nc localhost 6667; # B <-> A
echo "get_list_neighbors localhost 6668" | nc localhost 6667; # B <-> C
echo "get_list_neighbors localhost 6667" | nc localhost 6668; # C <-> B

# now that we have all the neighbors advertises >:)

while true; do 
    echo "check_for_swap" | nc localhost 6666;
    #sleep 1;
    echo "check_for_swap" | nc localhost 6667;
    #sleep 1;
    echo "check_for_swap" | nc localhost 6668;
    #sleep 1;
    sleep 1;
    echo "get_list_neighbors localhost 6667" | nc localhost 6666; # A <-> B
    echo "get_list_neighbors localhost 6666" | nc localhost 6667; # B <-> A
    echo "get_list_neighbors localhost 6668" | nc localhost 6667; # B <-> C
    echo "get_list_neighbors localhost 6667" | nc localhost 6668; # C <-> B
done






