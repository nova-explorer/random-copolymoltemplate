def export_to_lt(system, template, filename):

def export_to_xyz(system, filename):

def export_to_dump(system, filename):
    output = open(filename+".dump", "w")

    output.write("ITEM: TIMESTEP\n0\n")
    output.write("ITEM: NUMBER OF ATOMS\n")
    output.write(print_bounds(system))
    output.write("ITEM: ATOMS id type xu yu zu c_orient[1] c_orient[2] c_orient[3] c_orient[4] c_shape[1] c_shape[2] c_shape[3]")

    bead = "{id} {type} {x} {y} {z} 0 0 0  0 0 0 0"
    ellipsoid = "{id} {type} {x} {y} {z} 0 0 0 1 4.69 4.69 17.51"
    for row in system.polymers:
        for column in row:
            for poly in column:
                for mono in poly.monomers:
                    for atom in mono.atoms:
                        positions += bead.format(id=,
                                                 atom_type=,
                                                 x=,
                                                 y=,
                                                 z=,)

def print_bounds(system):