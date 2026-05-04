#!/bin/bash
set -e

# 3 of makesetup params without of end '/'
./Modules/makesetup -c ./Modules/config.c.in -s ./Modules ../../scripts/Setup.local
mv config.c ./Modules/


tmp_lto="-flto"
tmp_pgo="--enable-optimizations"
if [ -z "$tmp_lto" ] && [ "$tmp_pgo" == "--disable-optimizations" ]; then
	# usual, enable multi-threading
	threads="-j4"
else
	# hard optimizations, needs a lot of memory, disable multi-threading
	# also, bug in python build system or gcc: race condition on writing profiling (*.gdca) files in multithread mode
	threads="-j1"
fi

make "$threads"
cp ./libpython3.14.a ../000res/

hacl_lib="./Modules/_hacl/libHacl_HMAC.a"
make "$hacl_lib" "$threads"
cp "$hacl_lib" ../000res/
