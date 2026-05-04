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
	-DENABLE_SHARED=0 \
	-DENABLE_STATIC=1 \
	-DWITH_TURBOJPEG=0 \

make clean
