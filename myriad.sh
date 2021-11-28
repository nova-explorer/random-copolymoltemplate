#!/bin/bash

nb_configs=$1

for ((i=0; i<$nb_configs; i++))
do
	mkdir lammps/$i
	./setup_moltemplate.sh
	cp lammps/run.in.nvt lammps/system.in.init lammps/system.in.settings lammps/system.data lammps/$i

done
exit 0
