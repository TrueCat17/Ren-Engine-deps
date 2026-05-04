#!/bin/bash
set -e

cd ./build/
make -j4

cp ./libSDL3_image.a ../../000res/
