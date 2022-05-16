#!/bin/bash
set -e

SDL_DIR="SDL"
LIBJPEG_DIR="libjpeg-turbo"
LIBPNG_DIR="libpng-1.6.37"
LIBWEBP_DIR="libwebp-1.0.3"

ZLIB_DIR="zlib-1.2.11" # for libpng in pkg-config

export CC="gcc"
export CFLAGS="-O2 -flto"
export CPPFLAGS="-I$PWD/../$SDL_DIR/include -I$PWD/../$LIBJPEG_DIR -I$PWD/../$LIBPNG_DIR -I$PWD/../$LIBWEBP_DIR/src"
export LDFLAGS="-lm -pthread -flto -L$PWD/../000res"

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:$PWD/../$LIBPNG_DIR:$PWD/../$ZLIB_DIR:$PWD/../$LIBWEBP_DIR/src"
export SDL2_CONFIG="$PWD/../$SDL_DIR/sdl2-config"

export LIBPNG_LIBS="-lpng16 -lz"

./autogen.sh

./configure \
	--enable-static \
	--disable-shared \
	--disable-sdltest \
	\
	--disable-imageio \
	--disable-stb-image \
	--disable-avif \
	--disable-bmp \
	--disable-gif \
	--disable-jxl \
	--disable-lbm \
	--disable-pcx \
	--disable-pnm \
	--disable-svg \
	--disable-tga \
	--disable-tif \
	--disable-xcf \
	--disable-xpm \
	--disable-xv \
	--disable-qoi \
	\
	--enable-jpg \
	--enable-png \
	--enable-webp \
	\
	--disable-jpg-shared \
	--disable-png-shared \
	--disable-webp-shared

make clean
