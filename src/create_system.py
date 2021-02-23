#!/usr/bin/python

from read_system import system_settings
from generate_system import system
from export import export_to_dump

settings = system_settings("../input.txt")
system = system(settings)
export_to_dump(system, "output")