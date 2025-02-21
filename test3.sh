
while true; do
    for i in `seq 6661 6664`; do
        echo "check_for_swap" | nc localhost $i;
    done
done


