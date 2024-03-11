#!/bin/bash
set -e

cd ./out
make -j4

cp ./libbrotlicommon.a ../../000res
cp ./libbrotlidec.a ../../000res
