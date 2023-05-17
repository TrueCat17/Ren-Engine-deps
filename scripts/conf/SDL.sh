#!/bin/bash
set -e

export CC="gcc"
export CFLAGS="-O2 -flto"
export LDFLAGS="-lm -flto"


shared_static="--disable-shared --enable-static"
if [[ `echo $(uname -a) | tr '[A-Z]' '[a-z]'` =~ "cygwin" ]]; then
	CC="i686-w64-mingw32-gcc" # cygwin-SDL crashes on using opengl, use mingw
	shared_static="--enable-shared --disable-static" # mingw static lib is unsupported by cygwin => make shared
	LDFLAGS="$LDFLAGS -Wl,-s"
fi


./configure \
	--enable-sse2 \
	--disable-sse3 \
	\
	$shared_static \
	\
	--disable-joystick \
	--disable-haptic \
	--disable-sensor \
	--disable-power \
	\
	--disable-oss --disable-jack --disable-sndio --disable-esd \
	--disable-alsatest --disable-esdtest \
	--disable-arts --disable-nas --disable-fusionsound --disable-diskaudio \
	--disable-libsamplerate \
	\
	--disable-video-wayland \
	--disable-video-rpi \
	--disable-video-x11-scrnsaver \
	--disable-video-vivante \
	--disable-video-cocoa \
	--disable-render-metal \
	--disable-video-vulkan \
	--disable-video-directfb \
	--disable-directx \
	--disable-wasapi \
	--disable-video-opengles \
	--disable-video-opengles1 \
	--disable-video-opengles2 \
	\
	--disable-video-x11-xdbe \
	\
	--disable-rpath \
	--disable-render-d3d

make clean
