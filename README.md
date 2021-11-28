# random-copolymoltemplate

## Intro
r-cpm is a wrapper for Moltemplate that was designed to allow the user to create random copolymers easily.
The script works by reading an input file in which the user defines every monomer they want in the system. Then script will create a moltemplate system.lt file specific to this system and an xyz format system.xyz file containing particle locations.

## Version
0.1.1

## Requirements
- Python3 (tested on 3.9.2 64-bit)
- Python modules:
    - re
    - numpy
    - random
- Bash interpreter

## Syntax
The program will interpret the input file as such; commands are written first, then and '=' sign marks the end of the command and the start of its value. Then the value is written. '#' acts as a comment character. For boolean values, True can be written as : True, true, yes, Yes, 1. False can be written as : False, false, no, No, 0.

## List of commands
The commands will be noted as such:
- command : [possible values] Description
Lists are noted as:
    value1, value2
Nested lists are noted as:
    value1, value2 : value3, value4

This is the list and description of commands that can be used in the input file. Most are necessary as of now. In cases where 'monomer1' is in the command name, the '1' can be replaced by any number depending on the number of different monomers needed.
All lengths are in Angstrom and all angles in degrees.

- director : [x,y,z] Direction the polymer chains will be built in
- direction_1 : [x,y,z] Direction orthogonal to the director. The polymer chains will be stacked in this direction.
- direction_2 : [x,y,z] Direction orthogonal to the director. The polymer chains will be stacked in this direction.
- nb_chains_1 : [int] Number of polymer chains that will be placed in direction 1
- nb_chains_2 : [int] Number of polymer chains that will be placed in direction 2
- nb_monomers_per_chain : [int] Number of monomers per polymer chain
- monomer1_composition : Molecular composition of monomer 1. Each particle is separated by a '+' sign. To repeat a particle n times, the user can write [n] after the particle name. The director of this particle can be changed to direction 1 by writing {1} after the particle name. Those are called lateral fragments.
- monomer1_length : [float] Length of monomer 1 in Angstrom in the director axis. If 'auto' is used, the script will calculate the length automatically.
- monomer1_probability : [float] Probability of placing monomer 1 in the system. The sum of all monomer probability should be equal to 1.
- spacing_between_chains : [float] Length of the space between chains in the plane perpendicular to the director (the plane of direction 1 and 2). The spacing is the same in direction 1 and 2.
- translate on director : [bool] If True, the chains will be randomly translated along the director.
- translation_amplitude : [list of float] Minimal and maximal value for translation.
- rotate_along_director : [bool] If True, the lateral fragments will be rotated randomly in the direction 1 and 2 plane.
- rotation_amplitude : [list of floats] Minimal and maximal value for rotation.
- boundaries [nested list of floats] Set boundaries for the system if periodic. If 'auto' the boundaries will be calculated automatically. Otherwise, the items are as such: 1; minimum in x, 2; maximum in x, 3; minimum in y, 4; maximum in y, 5; minimum in z and 6; maximum in z.
- direction_angle : [x,y,z] Direction in which the angle stagger will be placed.
- sizes : [particle name, particle length] Size of each particle in the system.
- angles : [particle name, particle angle] Angle relative to the director of each particle in the system.
- groups : [group name, particle 1, particle 2, ...] Moltemplate molecule of each particle

## Current limitations
- Ellipsoidal shapes are fixed for the dump file but can be customised in their respective moltemplate molecule file.
- The polymer chains are entirely random (no iniator or terminator)
- Bond positionning works by calculating the cosine of the angle of the particle and then "inverting" (multipling by -1) 1/2 particles.
- Number of particles in monomers need to be odd for "inverting" to work

## Upcoming features
- Default values for most options
- Customisation of ellipsoidal shapes
- End of line character allowing commands on multiple lines
- Have negative minimum bounds on auto
- Chain iniator and terminator (and fixed patterns in general)
- Cross-linking (not planned soon)
- More bond positionning options (non-uniform bonds, para/meta/etc.. positionning)
- Rotating whole chains instead of just lateral fragments
- Rotation on other directions than just the plane orthogonal to the director
- Allowing more directions than x, y and z in general
- Heterogenous sizes
- **Read sizes and angles from forcefield**
- Different spacing in direction 1 and 2
- **Create polymers with random number of monomers**
- **Add non-uniform random**
- **A working example (with moltemplate files)**
- **TODOs in the src/ files (these are a bit more technical)**
- Check for parallel computing