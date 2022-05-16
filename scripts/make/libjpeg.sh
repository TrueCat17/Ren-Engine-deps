#!/bin/bash
set -e

cd ./build/
make -j4
cp ./libjpeg.a ../../../linux-x86_64/000res
cp ./*.h ..
