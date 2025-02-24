# 2-node setup, 
#
#   A-B

# send add_neighbor command to botmaster to add localhost 6662
echo "add_neighbor localhost 6662" | nc localhost 6661;

#
echo "add_neighbor localhost 6661" | nc localhost 6662;

#####

echo "get_vaddr localhost 6662" | nc localhost 6661;
echo "get_vaddr localhost 6661" | nc localhost 6662;

#####

echo "get_list_neighbors localhost 6662" | nc localhost 6661;
echo "get_list_neighbors localhost 6661" | nc localhost 6662;

# with all the neighbor-neighbors, we can calculate the values we need

#while true; do
#    echo "check_for_swap" | nc localhost 6661;
#    echo "check_for_swap" | nc localhost 6662;
#    sleep 1;
#done


#echo "exit" | nc localhost 6661;
#echo "exit" | nc localhost 6662;
#echo "exit" | nc localhost 6663;



