#!/bin/bash
set -e

make -j4

cp ./sharpyuv/.libs/libsharpyuv.a   ../000res/
cp ./src/.libs/libwebp.a            ../000res/
cp ./src/demux/.libs/libwebpdemux.a ../000res/
cp ./src/mux/.libs/libwebpmux.a     ../000res/
