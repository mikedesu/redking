# 4-node setup, 
# all in a chain
# A B C D

# link A to B
echo "add_neighbor localhost 6662" | nc localhost 6661;
echo "get_vaddr localhost 6662" | nc localhost 6661;
echo "add_neighbor localhost 6661" | nc localhost 6662;
echo "get_vaddr localhost 6661" | nc localhost 6662;

# link B to C
echo "add_neighbor localhost 6663" | nc localhost 6662;
echo "get_vaddr localhost 6663" | nc localhost 6662;
echo "add_neighbor localhost 6662" | nc localhost 6663;
echo "get_vaddr localhost 6662" | nc localhost 6663;

# link C to D
echo "add_neighbor localhost 6664" | nc localhost 6663;
echo "get_vaddr localhost 6664" | nc localhost 6663;
echo "add_neighbor localhost 6663" | nc localhost 6664;
echo "get_vaddr localhost 6663" | nc localhost 6664;

# link D to C
echo "add_neighbor localhost 6663" | nc localhost 6664;
echo "get_vaddr localhost 6663" | nc localhost 6664;
echo "add_neighbor localhost 6664" | nc localhost 6663;
echo "get_vaddr localhost 6664" | nc localhost 6663;

for i in `seq 6661 6664`; do
    for j in `seq 6661 6664`; do
        echo "get_list_neighbors localhost $j" | nc localhost $i;
    done
done

# now that we have all the neighbors advertises >:)
# its time...
# to do the sandberg swap!
# but first
# we must build the primitives

# with all the neighbor-neighbors, we can calculate the values we need

#while true; do
#    echo "check_for_swap" | nc localhost 6666;
#    echo "check_for_swap" | nc localhost 6667;
#    sleep 1;
#done


#echo "exit" | nc localhost 6666;
#echo "exit" | nc localhost 6667;
#echo "exit" | nc localhost 6668;



