#!/bin/bash
set -e

export CC="gcc"
export CFLAGS="-O2 -flto"
export LDFLAGS="-lm -flto"

export BROTLI_CFLAGS="-I$PWD/../brotli/c/include/"
export BROTLI_LIBS="-L$PWD/../000res/"

./autogen.sh

./configure \
	--disable-shared \
	--enable-static \
	--with-bzip2=no \
	--with-brotli=yes \

make clean
