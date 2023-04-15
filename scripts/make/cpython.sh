#!/bin/bash
set -e

make -j4 LDFLAGS="-lm"
cp ./libpython3.11.a ../000res
