#!/bin/bash
set -e

make -j4
cp ./build/.libs/libSDL2.a ../000res
cp ./build/.libs/libSDL2main.a ../000res
