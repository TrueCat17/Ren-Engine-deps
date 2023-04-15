#!/bin/bash
set -e

export CC="gcc"
#export CFLAGS="-O2 -flto"
#export LDFLAGS="-lm -flto -static"

./configure \
	--disable-shared \
	\
	--enable-optimizations \
	--with-lto

make clean
