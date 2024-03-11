#!/bin/bash
set -e

tmp="x-flto"
if [[ "$tmp" == "x" ]]; then
	threads="-j4" # usual, enable multi-threading
else
	threads="-j1" # hard optimizations, needs a lot of memory, disable multi-threading
fi

./Modules/makesetup -c Modules/config.c.in -s Modules ../../scripts/Setup.local
mv config.c ./Modules/

make "$threads" LDFLAGS="-lm"
cp ./libpython3.11.a ../000res

#cp ./libpython3.12.a ../000res
#cp ./Modules/_hacl/libHacl_Hash_SHA2.a ../000res
