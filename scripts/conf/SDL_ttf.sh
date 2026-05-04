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
	-DBUILD_SHARED_LIBS=0 \
	\
	-DSDLTTF_INSTALL=0 \
	-DSDLTTF_VENDORED=0 \
	-DSDLTTF_STRICT=1 \
	\
	-DSDLTTF_FREETYPE=1 \
	-DSDLTTF_HARFBUZZ=0 \
	-DSDLTTF_PLUTOSVG=0 \
	\
	-DSDL3_DIR="../SDL/build/" \
	\
	-DFREETYPE_LIBRARY="../../freetype/objs/.libs/libfreetype.a" \
	-DFREETYPE_INCLUDE_DIRS="$PWD/../../freetype/include/" \

make clean
