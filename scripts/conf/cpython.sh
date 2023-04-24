#!/bin/bash
set -e

export CC="gcc"

./configure \
	--disable-shared \
	\
	--enable-optimizations \
	--with-lto

make clean
