# redking python

This readme needs heavy updating.

## usage:

```
python3 botmaster.py <port> <seed>
python3 botmain.py <port> <seed>

echo "command" | nc localhost <port>
```

See `test1_setup.sh` and `test1.sh` for examples of interaction at the moment.
The intent is to automate a lot of what is being done there right now.

-----

[![asciicast](https://asciinema.org/a/EhsynoKYncB47vZ678fL5pAo2.svg)](https://asciinema.org/a/EhsynoKYncB47vZ678fL5pAo2)

-----

## TODO

- [ ] Only the botmaster should receive raw commands and even then...
  - [ ] Commands sent between botmaster and bot should be encrypted.
  - [ ] Commands sent between bot and bot should be encrypted.
- [x] Swap calc should select one random neighbor to do the check on instead of manual selection
- [ ] Verify nodes have unique addresses and are proeperly managing their list of neighbors and neighbor-neighbors.
- [ ] Many other things that I can't think of right now.

-----

## contact

- [twitter/x](https://x.com/evildojo666)
- [github](https://github.com/mikedesu)
- [youtube](https://youtube.com/@evildojo666)
