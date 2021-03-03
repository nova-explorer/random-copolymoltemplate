#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -f input.txt ]; then
    python3 src/test_system.py
else
    echo -e "${RED}Error: input.txt cannot be found in ./${NC}"
    exit 1
fi

if [ -f test.dump ]; then
    ovito test.dump
    rm test.dump
else
    echo -e "${RED}Error: test.dump cannot be found in mol ./${NC}"
    exit 1
fi

echo -e "${BLUE}"
shuf -n 1 src/post.txt