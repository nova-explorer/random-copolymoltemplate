#!/usr/bin/python
"""
main

Usage:

Requires modules:

Requires scripts: read_system.py
                  generate_system.py
                  monomer.py
                  export.py

TODO: *Current structure has a high propensity to create copy by reference issues.
      *initialize_monomers is useless
      *Increase verbosity and better error messages
"""
from read_system import system_settings
from generate_system import system
from export import export_to_dump, export_to_lt, export_to_xyz

settings = system_settings("input.txt")
system = system(settings)
export_to_xyz(system, "mol_files/system.xyz")
export_to_lt(system, "mol_files/template.lt", "mol_files/system.lt")