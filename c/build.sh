#!/usr/bin/env sh

set -ev

rm -rf build
mkdir build
cd build
cmake ..
cmake --build . --target all
#cmake --build . --target install
ctest -T Test -T memcheck
