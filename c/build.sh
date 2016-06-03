#!/usr/bin/env sh

set -ev

rm -rf build
mkdir build
cd build
cmake ..
cmake --build . --target all
ctest -T Test
