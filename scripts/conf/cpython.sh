#!/bin/bash
set -e

export CC="gcc"

shared="--disable-shared" # for faster building
if [[ `echo $(uname -a) | tr '[A-Z]' '[a-z]'` =~ "cygwin" ]]; then
	shared="--enable-shared" # for no error on cygwin
fi

./configure "$shared" \
	--enable-optimizations \
	--with-lto

make clean
