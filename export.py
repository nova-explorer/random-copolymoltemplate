def export_to_lt(system, template, filename):
    return 0
def export_to_xyz(system, filename):
    return 0

def export_to_dump(system, filename):
    output = open(filename+".dump", "w")

    output.write("ITEM: TIMESTEP\n0\n")
    output.write("ITEM: NUMBER OF ATOMS\n")
    output.write(print_nb_atoms(system))
    output.write("ITEM: BOX BOUNDS pp pp pp\n")
    output.write(print_bounds(system))
    output.write("ITEM: ATOMS id type xu yu zu c_orient[1] c_orient[2] c_orient[3] c_orient[4] c_shape[1] c_shape[2] c_shape[3]\n")
    output.write(print_positions(system))

def print_nb_atoms(system):
    cnt = 0
    for row in system.polymers:
        for poly in row:
            for mono in poly.monomers:
                for atom in mono.atoms:
                    cnt += 1
    return str(cnt)+"\n"

def print_bounds(system):
    bounds = ""
    line = "{min} {max}\n"
    for i in system.settings.boundaries:
        bounds += line.format(min=i[0], max=i[1])
    return bounds

def print_positions(system):
    positions = ""
    bead = "{id} {type} {x} {y} {z} 0 0 0 0 0 0 0\n"
    ellipsoid = "{id} {type} {x} {y} {z} 0 0 0 1 2.345 2.345 8.75\n"

    for row in system.polymers:
        for poly in row:
            for mono in poly.monomers:
                for atom in mono.atoms:
                    if atom.type == "ELL":
                        positions += ellipsoid.format(id=atom.system_id,
                                                type=atom.lammps_type,
                                                x=atom.x,
                                                y=atom.y,
                                                z=atom.z)
                    else:
                        positions += bead.format(id=atom.system_id,
                                                type=atom.lammps_type,
                                                x=atom.x,
                                                y=atom.y,
                                                z=atom.z)
    return positions