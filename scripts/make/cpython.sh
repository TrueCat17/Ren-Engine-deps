#!/bin/bash
set -e

tmp="x-flto"
if [[ "$tmp" == "x" ]]; then
	threads="-j4" # usual, enable multi-threading
else
	threads="-j1" # hard optimizations, needs a lot of memory, disable multi-threading
fi

make "$threads" LDFLAGS="-lm"
cp ./libpython3.11.a ../000res
