echo "add_neighbor localhost 6667" | nc localhost 6666;
echo "add_neighbor localhost 6668" | nc localhost 6666;
echo "add_neighbor localhost 6669" | nc localhost 6666;
echo "add_neighbor localhost 6670" | nc localhost 6666;
echo "add_neighbor localhost 6671" | nc localhost 6666;


echo "add_neighbor localhost 6666" | nc localhost 6667;
echo "add_neighbor localhost 6668" | nc localhost 6667;
echo "add_neighbor localhost 6669" | nc localhost 6667;
echo "add_neighbor localhost 6670" | nc localhost 6667;
echo "add_neighbor localhost 6671" | nc localhost 6667;

echo "add_neighbor localhost 6666" | nc localhost 6668;
echo "add_neighbor localhost 6667" | nc localhost 6668;
echo "add_neighbor localhost 6669" | nc localhost 6668;
echo "add_neighbor localhost 6670" | nc localhost 6668;
echo "add_neighbor localhost 6671" | nc localhost 6668;

echo "add_neighbor localhost 6666" | nc localhost 6669;
echo "add_neighbor localhost 6667" | nc localhost 6669;
echo "add_neighbor localhost 6668" | nc localhost 6669;
echo "add_neighbor localhost 6670" | nc localhost 6669;
echo "add_neighbor localhost 6671" | nc localhost 6669;

echo "add_neighbor localhost 6666" | nc localhost 6670;
echo "add_neighbor localhost 6667" | nc localhost 6670;
echo "add_neighbor localhost 6668" | nc localhost 6670;
echo "add_neighbor localhost 6669" | nc localhost 6670;
echo "add_neighbor localhost 6671" | nc localhost 6670;

echo "add_neighbor localhost 6666" | nc localhost 6671;
echo "add_neighbor localhost 6667" | nc localhost 6671;
echo "add_neighbor localhost 6668" | nc localhost 6671;
echo "add_neighbor localhost 6669" | nc localhost 6671;
echo "add_neighbor localhost 6670" | nc localhost 6671;

echo "get_vaddr localhost 6667" | nc localhost 6666;
echo "get_vaddr localhost 6668" | nc localhost 6666;
echo "get_vaddr localhost 6669" | nc localhost 6666;
echo "get_vaddr localhost 6670" | nc localhost 6666;
echo "get_vaddr localhost 6671" | nc localhost 6666;

echo "get_vaddr localhost 6666" | nc localhost 6667;
echo "get_vaddr localhost 6668" | nc localhost 6667;
echo "get_vaddr localhost 6669" | nc localhost 6667;
echo "get_vaddr localhost 6670" | nc localhost 6667;
echo "get_vaddr localhost 6671" | nc localhost 6667;

echo "get_vaddr localhost 6666" | nc localhost 6668;
echo "get_vaddr localhost 6667" | nc localhost 6668;
echo "get_vaddr localhost 6669" | nc localhost 6668;
echo "get_vaddr localhost 6670" | nc localhost 6668;
echo "get_vaddr localhost 6671" | nc localhost 6668;

echo "get_vaddr localhost 6666" | nc localhost 6669;
echo "get_vaddr localhost 6667" | nc localhost 6669;
echo "get_vaddr localhost 6668" | nc localhost 6669;
echo "get_vaddr localhost 6670" | nc localhost 6669;
echo "get_vaddr localhost 6671" | nc localhost 6669;

echo "get_vaddr localhost 6666" | nc localhost 6670;
echo "get_vaddr localhost 6667" | nc localhost 6670;
echo "get_vaddr localhost 6668" | nc localhost 6670;
echo "get_vaddr localhost 6669" | nc localhost 6670;
echo "get_vaddr localhost 6671" | nc localhost 6670;

echo "get_vaddr localhost 6666" | nc localhost 6671;
echo "get_vaddr localhost 6667" | nc localhost 6671;
echo "get_vaddr localhost 6668" | nc localhost 6671;
echo "get_vaddr localhost 6669" | nc localhost 6671;
echo "get_vaddr localhost 6670" | nc localhost 6671;

#echo "list_neighbors" | nc localhost 6666;
#echo "list_neighbors" | nc localhost 6667;
#echo "list_neighbors" | nc localhost 6668;
echo "get_list_neighbors localhost 6667" | nc localhost 6666;
echo "get_list_neighbors localhost 6668" | nc localhost 6666;
echo "get_list_neighbors localhost 6669" | nc localhost 6666;
echo "get_list_neighbors localhost 6670" | nc localhost 6666;
echo "get_list_neighbors localhost 6671" | nc localhost 6666;

echo "get_list_neighbors localhost 6666" | nc localhost 6667;
echo "get_list_neighbors localhost 6668" | nc localhost 6667;
echo "get_list_neighbors localhost 6669" | nc localhost 6667;
echo "get_list_neighbors localhost 6670" | nc localhost 6667;
echo "get_list_neighbors localhost 6671" | nc localhost 6667;

echo "get_list_neighbors localhost 6666" | nc localhost 6668;
echo "get_list_neighbors localhost 6667" | nc localhost 6668;
echo "get_list_neighbors localhost 6669" | nc localhost 6668;
echo "get_list_neighbors localhost 6670" | nc localhost 6668;
echo "get_list_neighbors localhost 6671" | nc localhost 6668;

echo "get_list_neighbors localhost 6666" | nc localhost 6669;
echo "get_list_neighbors localhost 6667" | nc localhost 6669;
echo "get_list_neighbors localhost 6668" | nc localhost 6669;
echo "get_list_neighbors localhost 6670" | nc localhost 6669;
echo "get_list_neighbors localhost 6671" | nc localhost 6669;

echo "get_list_neighbors localhost 6666" | nc localhost 6670;
echo "get_list_neighbors localhost 6667" | nc localhost 6670;
echo "get_list_neighbors localhost 6668" | nc localhost 6670;
echo "get_list_neighbors localhost 6669" | nc localhost 6670;    
echo "get_list_neighbors localhost 6671" | nc localhost 6670;

echo "get_list_neighbors localhost 6666" | nc localhost 6671;
echo "get_list_neighbors localhost 6667" | nc localhost 6671;
echo "get_list_neighbors localhost 6668" | nc localhost 6671;
echo "get_list_neighbors localhost 6669" | nc localhost 6671;
echo "get_list_neighbors localhost 6670" | nc localhost 6671;

#sleep 3;

# now that we have all the neighbors advertises >:)
# its time...
# to do the sandberg swap!
# but first
# we must build the primitives

# with all the neighbor-neighbors, we can calculate the values we need

while true; do
    echo "check_for_swap localhost 6667" | nc localhost 6666;
    sleep 1;
    echo "check_for_swap localhost 6668" | nc localhost 6666;
    sleep 1;
    echo "check_for_swap localhost 6669" | nc localhost 6666;
    sleep 1;
    echo "check_for_swap localhost 6670" | nc localhost 6666;
    sleep 1;
    echo "check_for_swap localhost 6671" | nc localhost 6666;
    sleep 1;

    echo "check_for_swap localhost 6666" | nc localhost 6667;
    sleep 1;
    echo "check_for_swap localhost 6668" | nc localhost 6667;
    sleep 1;
    echo "check_for_swap localhost 6669" | nc localhost 6667;
    sleep 1;
    echo "check_for_swap localhost 6670" | nc localhost 6667;
    sleep 1;
    echo "check_for_swap localhost 6671" | nc localhost 6667;
    sleep 1;

    echo "check_for_swap localhost 6666" | nc localhost 6668;
    sleep 1;
    echo "check_for_swap localhost 6667" | nc localhost 6668;
    sleep 1;
    echo "check_for_swap localhost 6669" | nc localhost 6668;
    sleep 1;
    echo "check_for_swap localhost 6670" | nc localhost 6668;
    sleep 1;
    echo "check_for_swap localhost 6671" | nc localhost 6668;
    sleep 1;

    echo "check_for_swap localhost 6666" | nc localhost 6669;
    sleep 1;
    echo "check_for_swap localhost 6667" | nc localhost 6669;
    sleep 1;
    echo "check_for_swap localhost 6668" | nc localhost 6669;
    sleep 1;
    echo "check_for_swap localhost 6670" | nc localhost 6669;
    sleep 1;
    echo "check_for_swap localhost 6671" | nc localhost 6669;
    sleep 1;

    echo "check_for_swap localhost 6666" | nc localhost 6670;
    sleep 1;
    echo "check_for_swap localhost 6667" | nc localhost 6670;
    sleep 1;
    echo "check_for_swap localhost 6668" | nc localhost 6670;
    sleep 1;
    echo "check_for_swap localhost 6669" | nc localhost 6670;
    sleep 1;
    echo "check_for_swap localhost 6671" | nc localhost 6670;
    sleep 1;

    echo "check_for_swap localhost 6666" | nc localhost 6671;
    sleep 1;
    echo "check_for_swap localhost 6667" | nc localhost 6671;
    sleep 1;
    echo "check_for_swap localhost 6668" | nc localhost 6671;
    sleep 1;
    echo "check_for_swap localhost 6669" | nc localhost 6671;
    sleep 1;
    echo "check_for_swap localhost 6670" | nc localhost 6671;
    sleep 1;
done


#echo "exit" | nc localhost 6666;
#echo "exit" | nc localhost 6667;
#echo "exit" | nc localhost 6668;



