#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'
SECONDS=0

if [ -f input.txt ]; then
    python3 src/create_system.py
    if [ $? != 0 ]; then
        echo -e "${RED}Error: Python encountered an error."
        exit 1
    fi
else
    echo -e "${RED}Error: input.txt cannot be found in ./${NC}"
    exit 1
fi

if [ -f mol_files/system.lt ] && [ -f mol_files/system.xyz ]; then
    cd mol_files/
        moltemplate.sh -xyz system.xyz -atomstyle "atomid atomtype x y z molid ellipsoidflag density" system.lt
        if [ $? != 0 ]; then
            echo -e "${RED}Error: Moltemplate encountered an error."
            exit 1
        fi

        NB_ELL=$(grep -E 'new longi \[[0-9\.]+\]' system.lt | grep -Eo '[0-9\.]+')
        sed "s/.*ellipsoids/     $NB_ELL  ellipsoids/" system.data > temp &&
            mv temp system.data
    cd ../
    mv mol_files/system.in.init lammps/
    mv mol_files/system.in.settings lammps/
    mv mol_files/system.data lammps/
else
    echo -e "${RED}Error: system.lt and system.xyz cannot be found in mol_files/${NC}"
    exit 1
fi

echo -e "${GREEN}Finished script in $SECONDS s${NC}"
echo -e "${BLUE}"
shuf -n 1 src/post.txt
echo -e "${NC}"