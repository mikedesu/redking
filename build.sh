#!/usr/bin/sh
#
mkdir -p build
cd build
cmake .. -Wno-dev
make
