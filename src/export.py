def export_to_lt(system, template, output_name):
    header = get_header(template)
    output = open(output_name, "w")
    output.write(header)

    output.write(get_atoms(system))
    output.write("\n")

    output.write("write('Data Bond List') {\n")
    output.write(get_bonds(system))
    output.write("}\n")

    output.write("\n")

    output.write('write_once("Data Boundary") {\n')
    output.write(get_boundaries(system))
    output.write("}\n")

    output.close()

def get_header(template):
    with open(template, "rt") as file:
        header = file.readlines()
    return "".join(header)

def get_atoms(system):
    section = ""
    base = "{name} = new {type} [{count}]\n"
    for i in system.settings.groups:
        if get_group_count(system,i) != '0':
            section += base.format(name=i+'s',
                                type=i,
                                count=get_group_count(system,i))
    return section

def get_bonds(system):
    section = ""
    base = "\t$bond:b{b_id}  $atom:{name1}[{cnt1}]/{type1} $atom:{name2}[{cnt2}]/{type2}\n"
    bond_id = 0
    atoms = []
    for row in system.polymers:
        for poly in row:
            for mono in poly.monomers:
                for atom in mono.atoms:
                    atoms.append(atom)

    for i in range(len(atoms)-1):
        atom1 = atoms[i]
        for id_2 in atom1.bonds:
            atom2 = system.get_atom(id_2)
            section += base.format(b_id=bond_id,
                                name1=get_group(system, atom1)+'s',
                                name2=get_group(system, atom2)+'s',
                                cnt1=get_group_position(system, atom1),
                                cnt2=get_group_position(system, atom2),
                                type1=atom1.type,
                                type2=atom2.type)
            bond_id+=1
    return section

def get_boundaries(system):
    section = ""
    base = "\t0 {hi} {var}lo {var}hi\n"
    bounds = system.settings.boundaries
    for i in bounds:
        section += base.format(hi=bounds[i],
                               var=i)
    return section

def get_group_count(system, group):
    group_cnt = []
    for atom_type in system.settings.groups[group]:
        cnt = 0
        for row in system.polymers:
            for poly in row:
                for mono in poly.monomers:
                    for i in mono.atoms:
                        if i.type == atom_type:
                            cnt += 1
        group_cnt.append(cnt)
    return str(min(group_cnt))

def get_group(system, atom):
    for group in system.settings.groups:
        for atom_type in system.settings.groups[group]:
            if atom_type == atom.type:
                return group

def get_group_position(system,atom):
    atoms = []
    for row in system.polymers:
        for poly in row:
            for mono in poly.monomers:
                for i in mono.atoms:
                    atoms.append(i)
    group = get_group(system,atom)
    lenght = len(system.settings.groups[group])
    cnt = 0
    group_cnt = 0
    for i in atoms[0:atom.id-1]:
        if get_group(system, i) == group:
            cnt += 1
        if cnt >= lenght:
            group_cnt += 1
            cnt = 0
    return group_cnt

def get_type_count(system, atom):
    cnt = 0
    for row in system.polymers:
        for poly in row:
            for mono in poly.monomers:
                for i in range(len(mono.atoms)):
                    current = mono.atoms[i]
                    if current.id == atom.id:
                        return cnt
                    elif current.type == atom.type:
                        cnt += 1
    return cnt

def export_to_xyz(system, filename):
    output = open(filename, "w")
    output.write(print_nb_atoms(system) + "\n")
    section = ""
    base = "{name}  {x} {y} {z}\n"
    atoms = sort_atom_by_group(system)
    for i in atoms:
        section += base.format(name=i.type,
                               x=i.x,
                               y=i.y,
                               z=i.z)
    output.write(section)

def sort_atoms_by_type(system):
    sorted_atoms = []
    types = system.settings.sizes.keys()
    for curr_type in types:
        for row in system.polymers:
            for poly in row:
                for mono in poly.monomers:
                    for atom in mono.atoms:
                        if atom.type == curr_type:
                            sorted_atoms.append(atom)
    return sorted_atoms

def sort_atom_by_group(system):
    sorted_atoms = []
    for group in system.settings.groups:
        for row in system.polymers:
            for poly in row:
                for mono in poly.monomers:
                    for atom in mono.atoms:
                        if get_group(system, atom) == group:
                            sorted_atoms.append(atom)
    return sorted_atoms

def export_to_dump(system, filename):
    output = open(filename, "w")

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
                for _ in mono.atoms:
                    cnt += 1
    return str(cnt)+"\n"

def print_bounds(system):
    bounds = ""
    line = "0 {max}\n"
    for i in system.settings.boundaries:
        bounds += line.format(max=system.settings.boundaries[i])
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
                        positions += ellipsoid.format(id=atom.id,
                                                type=atom.lammps_type,
                                                x=atom.x,
                                                y=atom.y,
                                                z=atom.z)
                    else:
                        positions += bead.format(id=atom.id,
                                                type=atom.lammps_type,
                                                x=atom.x,
                                                y=atom.y,
                                                z=atom.z)
    return positions