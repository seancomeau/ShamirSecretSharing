#!/usr/bin/env sh

set -ev

rm -rf build
mkdir build
cd build
cmake ..
scan-build cmake --build . --target all
ctest -T Test -T memcheck
