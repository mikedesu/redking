while true; do
    for i in `seq 6666 6671`; do
        echo "check_for_swap" | nc localhost $i;
        sleep 0.25;
    done
done


