#!/usr/bin/python
"""
"""
from read_system import system_settings
from generate_system import system
from export import export_to_dump, export_to_lt, export_to_xyz

settings = system_settings("input.txt")
system = system(settings)
export_to_dump(system, "test.dump")
