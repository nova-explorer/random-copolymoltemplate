#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'
SECONDS=0

cd lammps/
    lmp -in run.in.nvt
cd ..

echo -e "${GREEN}Finished script in $SECONDS s${NC}"