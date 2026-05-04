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
	-DSDLIMAGE_INSTALL=0 \
	-DSDLIMAGE_INSTALL_CPACK=0 \
	-DSDLIMAGE_DEPS_SHARED=0 \
	-DSDLIMAGE_VENDORED=0 \
	-DSDLIMAGE_STRICT=1 \
	-DSDLIMAGE_SAMPLES=0 \
	-DSDLIMAGE_BACKEND_STB=0 \
	-DSDLIMAGE_BACKEND_WIC=0 \
	-DSDLIMAGE_BACKEND_IMAGEIO=0 \
	\
	-DSDLIMAGE_ANI=0 \
	-DSDLIMAGE_AVIF=0 \
	-DSDLIMAGE_BMP=0 \
	-DSDLIMAGE_GIF=0 \
	-DSDLIMAGE_JXL=0 \
	-DSDLIMAGE_LBM=0 \
	-DSDLIMAGE_PCX=0 \
	-DSDLIMAGE_PNM=0 \
	-DSDLIMAGE_QOI=0 \
	-DSDLIMAGE_SVG=0 \
	-DSDLIMAGE_TGA=0 \
	-DSDLIMAGE_TIF=0 \
	-DSDLIMAGE_XCF=0 \
	-DSDLIMAGE_XPM=0 \
	-DSDLIMAGE_XV=0 \
	\
	-DSDLIMAGE_JPG=1 \
	-DSDLIMAGE_PNG=1 \
	-DSDLIMAGE_PNG_LIBPNG=0 \
	-DSDLIMAGE_WEBP=1 \
	\
	-DSDLIMAGE_JPG_SAVE=1 \
	-DSDLIMAGE_PNG_SAVE=1 \
	-DSDLIMAGE_WEBP_SAVE=0 \
	\
	-DSDL3_DIR="../SDL/build/" \
	\
	-DJPEG_LIBRARY="../../libjpeg-turbo/build/libjpeg.a" \
	-DJPEG_INCLUDE_DIR="../../libjpeg-turbo/src/" \
	\
	-Dwebp_LIBRARY="../../libwebp/src/.libs/libwebp.a" \
	-Dwebp_INCLUDE_PATH="../../libwebp/src/" \
	-Dwebpdemux_LIBRARY="/" \
	-Dwebpdemux_INCLUDE_PATH="/" \
	-Dwebpmux_LIBRARY="/" \
	-Dwebpmux_INCLUDE_PATH="/" \

# webp_(de)mux lib paths not used
# webp_(de)mux include paths = webp include path (not need extra definition)
# but all paths must be correct and existing

make clean
