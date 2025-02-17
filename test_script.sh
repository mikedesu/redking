echo "add_neighbor localhost 6667" | nc localhost 6666;
sleep 1;
echo "add_neighbor localhost 6668" | nc localhost 6666;
sleep 1;

echo "add_neighbor localhost 6666" | nc localhost 6667;
sleep 1;
echo "add_neighbor localhost 6668" | nc localhost 6667;
sleep 1;

echo "add_neighbor localhost 6666" | nc localhost 6668;
sleep 1;
echo "add_neighbor localhost 6667" | nc localhost 6668;
sleep 1;

echo "get_vaddr localhost 6667" | nc localhost 6666;
sleep 1;
echo "get_vaddr localhost 6668" | nc localhost 6666;
sleep 1;

echo "get_vaddr localhost 6666" | nc localhost 6667;
sleep 1;
echo "get_vaddr localhost 6668" | nc localhost 6667;
sleep 1;

echo "get_vaddr localhost 6666" | nc localhost 6668;
sleep 1;
echo "get_vaddr localhost 6667" | nc localhost 6668;
sleep 1;


echo "list_neighbors" | nc localhost 6666;
sleep 1;
echo "list_neighbors" | nc localhost 6667;
sleep 1;
echo "list_neighbors" | nc localhost 6668;
sleep 1;

echo "exit" | nc localhost 6666;
echo "exit" | nc localhost 6667;
echo "exit" | nc localhost 6668;



