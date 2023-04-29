#!/bin/bash
set -e

export CC="gcc"
export CFLAGS="-O2 -flto"
export LDFLAGS="-lm -flto"

# <out> instead <build>, because <BUILD> is file in brotli repo
mkdir -p ./out
rm -rf ./out/*
cd ./out
cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=./installed -DBROTLI_DISABLE_TESTS=ON
