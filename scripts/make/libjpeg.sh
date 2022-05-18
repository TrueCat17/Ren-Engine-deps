#!/bin/bash
set -e

cd ./build/
make -j4
cp ./libjpeg.a ../../000res
cp ./*.h ..
