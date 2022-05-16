#!/bin/bash
set -e

SDL_DIR="SDL2-2.0.10"
FREETYPE_DIR="freetype-2.10.1"

export CC="gcc"
export CFLAGS="-O2 -flto -I$PWD/../$SDL_DIR/include -I$PWD/../$FREETYPE_DIR/include"
export LDFLAGS="-lm -flto"
export LIBS="-L$PWD/../000res/ -lfreetype -lbrotlidec-static -lbrotlicommon-static -lz"

export SDL2_CONFIG="$PWD/../$SDL_DIR/sdl2-config"

./autogen.sh

./configure \
	--enable-static \
	--disable-shared \
	--disable-sdltest \
	--disable-freetypetest \
	--disable-freetype-builtin \
	--disable-harfbuzz \
	--disable-harfbuzz-builtin \
	\
	--with-ft-prefix=$PWD/../000res

make clean
