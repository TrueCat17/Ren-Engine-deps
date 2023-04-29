#!/bin/bash
set -e

cd ./out
make -j4

cp ./libbrotlicommon-static.a ../../000res
cp ./libbrotlidec-static.a ../../000res
