echo "add_neighbor localhost 6667" | nc localhost 6666;
echo "add_neighbor localhost 6666" | nc localhost 6667;
echo "add_neighbor localhost 6668" | nc localhost 6667;
echo "add_neighbor localhost 6667" | nc localhost 6668;

echo "get_vaddr localhost 6667" | nc localhost 6666;
echo "get_vaddr localhost 6666" | nc localhost 6667;
echo "get_vaddr localhost 6668" | nc localhost 6667;
echo "get_vaddr localhost 6667" | nc localhost 6668;

echo "get_list_neighbors localhost 6667" | nc localhost 6666;
echo "get_list_neighbors localhost 6666" | nc localhost 6667;
echo "get_list_neighbors localhost 6668" | nc localhost 6667;
echo "get_list_neighbors localhost 6667" | nc localhost 6668;

# now that we have all the neighbors advertises >:)
# its time...
# to do the sandberg swap!
# but first
# we must build the primitives

# with all the neighbor-neighbors, we can calculate the values we need

#while true; do
#    echo "check_for_swap" | nc localhost 6666;
#    echo "check_for_swap" | nc localhost 6667;
#    echo "check_for_swap" | nc localhost 6668;
#    sleep 1;
#done


#echo "exit" | nc localhost 6666;
#echo "exit" | nc localhost 6667;
#echo "exit" | nc localhost 6668;



