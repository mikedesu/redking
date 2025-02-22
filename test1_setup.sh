# 3-node setup, 
#
#   A
#  / \
# B - C

echo "add_neighbor localhost 6662" | nc localhost 6661;
echo "add_neighbor localhost 6663" | nc localhost 6661;

echo "add_neighbor localhost 6661" | nc localhost 6662;
echo "add_neighbor localhost 6663" | nc localhost 6662;

echo "add_neighbor localhost 6661" | nc localhost 6663;
echo "add_neighbor localhost 6662" | nc localhost 6663;

#####

echo "get_vaddr localhost 6662" | nc localhost 6661;
echo "get_vaddr localhost 6663" | nc localhost 6661;

echo "get_vaddr localhost 6661" | nc localhost 6662;
echo "get_vaddr localhost 6663" | nc localhost 6662;

echo "get_vaddr localhost 6661" | nc localhost 6663;
echo "get_vaddr localhost 6662" | nc localhost 6663;

#####

echo "get_list_neighbors localhost 6662" | nc localhost 6661;
echo "get_list_neighbors localhost 6663" | nc localhost 6661;

echo "get_list_neighbors localhost 6661" | nc localhost 6662;
echo "get_list_neighbors localhost 6663" | nc localhost 6662;

echo "get_list_neighbors localhost 6661" | nc localhost 6663;
echo "get_list_neighbors localhost 6662" | nc localhost 6663;

# now that we have all the neighbors advertises >:)
# its time...
# to do the sandberg swap!
# but first
# we must build the primitives

# with all the neighbor-neighbors, we can calculate the values we need

#while true; do
#    echo "check_for_swap" | nc localhost 6661;
#    echo "check_for_swap" | nc localhost 6662;
#    sleep 1;
#done


#echo "exit" | nc localhost 6661;
#echo "exit" | nc localhost 6662;
#echo "exit" | nc localhost 6663;



