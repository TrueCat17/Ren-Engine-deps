#!/bin/bash
set -e

export CC="gcc"
export CFLAGS="-O2 -flto"
export LDFLAGS="-lm -flto"

rm -rf ./build/
mkdir ./build/
cd ./build/

cmake .. -G "Unix Makefiles" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=./installed \
	-DBUILD_SHARED_LIBS=0 \
	-DBROTLI_DISABLE_TESTS=1 \

make clean
