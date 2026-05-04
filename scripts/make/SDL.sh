#!/bin/bash
set -e

cd ./build/
make -j4

cp ./libSDL3.a ../../000res/
