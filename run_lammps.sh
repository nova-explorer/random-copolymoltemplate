#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'
SECONDS=0

cd lammps/
    mpirun -np 6 /home/explorer/source_codes/lammps/src/lmp_mpi -in run.in.nvt
cd ..

echo -e "${GREEN}Finished script in $SECONDS s${NC}"