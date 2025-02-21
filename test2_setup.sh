# 6-node setup, 
# all linked to each other
#
# A B C D E F

for bot in `seq 6666 6671`; do
    for i in `seq 6666 6671`; do
        if [ $i -ne $bot ]; then
            echo "add_neighbor localhost $i" | nc localhost $bot;
            echo "get_vaddr localhost $i" | nc localhost $bot;
        fi
    done
done

for bot in `seq 6666 6671`; do
    for i in `seq 6666 6671`; do
        echo "get_list_neighbors localhost $i" | nc localhost $bot;
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



