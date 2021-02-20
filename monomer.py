import re
from numpy import cos, sin, pi
from numpy.random import choice

class polymer():
    def __init__(self, monomer_list, probabilities, nb_monomer, director):
        self.monomer_list = monomer_list
        self.probabilities = probabilities
        self.nb_monomer = nb_monomer
        self.director = director
        self.create_polymer()

    def create_polymer(self):
        self.monomers = []
        position = 0
        inversion_counter = 1
        for i in range(self.nb_monomer):
            current_monomer = choice(self.monomer_list, replace=False, p=self.probabilities)
            current_monomer = monomer(current_monomer.settings, current_monomer.director, inversion_counter)
            current_monomer.translate([0, 0, position])
            self.monomers.append(current_monomer)
            position += current_monomer.length
            inversion_counter = inversion_counter * current_monomer.get_inversion_counter()

    def translate(self, coords):
        for i in self.monomers:
            i.translate(coords)

    def get_length(self):
        return sum([i.length for i in self.monomers])

    def add_system_id(self, system_id):
        self.s_id = system_id

class monomer_settings():
    def __init__(self, monomer_id):
        self.id = monomer_id

    def check_settings(self):
        """[summary]

        Returns:
            [type]: [description]
        TODO: correct error types
              is used ?
        """
        flag = True
        try:
            self.composition
        except:
            flag = False
            print("Monomer", self.id, "composition missing")
        try:
            self.length
        except:
            flag = False
            print("Monomer", self.id, "has no specified length")
        try:
            self.probability
        except:
            flag = False
            print("Monomer", self.id, "probability missing")
        return flag

    def add_composition(self, composition):
        self.composition = composition

    def add_length(self, length):
        self.length = length

    def add_probability(self, probability):
        self.probability = probability

    def add_particle_sizes(self, sizes):
        self.particles_sizes = sizes

    def add_particle_angles(self, angles):
        self.particles_angles = angles

class monomer():
    def __init__(self, settings, director, inversion_counter):
        self.settings = settings
        self.director = director
        self.evaluate_composition()
        self.create_atom_list(inversion_counter)
        self.evaluate_length()
        self.evaluate_probability()
        self.create_lammps_ids()

    def evaluate_composition(self):
        composition = [i.strip() for i in self.settings.composition.split("+")]
        self.composition = []
        for i in composition:
            unit = i
            repeat = 1
            if '[' in i and ']' in i:
                result = re.search(r"(.*)\[(.*)\]", i)
                try:
                    unit = result[1]
                    repeat = int(result[2])
                except:
                    raise ValueError("repeat value is not an int")
            self.composition.extend([unit]*repeat)

        types = self.settings.particles_sizes.keys()
        for i in self.composition:
            if i not in types:
                raise Exception("Type", i, "does not have a specified length")

    def create_atom_list(self, inversion_counter):
        DEG_TO_RAD = 2 * pi / 360
        self.atoms = []
        last_length = self.settings.particles_sizes[self.composition[0]]*sin(self.settings.particles_angles[self.composition[0]]*DEG_TO_RAD/2)
        position = -last_length
        for i, atom_type in enumerate(self.composition):
            if self.settings.particles_angles[atom_type]:
                position += (self.settings.particles_sizes[atom_type]*sin(self.settings.particles_angles[atom_type]*DEG_TO_RAD/2) + last_length)/2
                direction_1 = ( self.settings.particles_sizes[atom_type]*cos(self.settings.particles_angles[atom_type]*DEG_TO_RAD/2) ) / 2 * inversion_counter
                self.atoms.append( atom(i, atom_type, [direction_1,0,position], self.settings.particles_sizes[atom_type]) )
                last_length = self.settings.particles_sizes[atom_type]*sin(self.settings.particles_angles[atom_type]*DEG_TO_RAD/2)
                inversion_counter *= -1
            else:
                position += (self.settings.particles_sizes[atom_type] + last_length)/2
                self.atoms.append( atom(i, atom_type, [0,0,position], self.settings.particles_sizes[atom_type]) )
                last_length = self.settings.particles_sizes[atom_type]
        self.last_length = last_length

    def get_inversion_counter(self):
        if len(self.composition) % 2: # if even number of atoms
            inv_cnt = -1
        else:
            inv_cnt = 1
        return inv_cnt

    def evaluate_length(self):
        if self.settings.length == "auto":
            # self.length = sum([i.size for i in self.atoms])
            self.length = self.atoms[-1].z - self.atoms[0].z + self.last_length
        else:
            try:
                self.length = float(self.settings.length)
            except:
                raise ValueError("monomer length is neither auto nor a number")

    def evaluate_probability(self):
        try:
            prob = float(self.settings.probability)
            if prob > 1:
                raise ValueError("Value too high")
            self.probability = prob
        except:
            print("probability is not a number")

    def translate(self, coords):
        for i in self.atoms:
            i.translate(coords)

    def create_lammps_ids(self):
        for i in self.atoms:
            i.add_lammps_type(self.settings.particles_sizes.keys())

    def add_system_id(self, system_id):
        self.s_id = system_id
class atom():
    def __init__(self, monomer_id, atom_type, xyz, size):
        self.monomer_id = monomer_id
        self.type = atom_type
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
        self.size = size

    def translate(self, coords):
        self.x += coords[0]
        self.y += coords[1]
        self.z += coords[2]

    def rotate(self, radius, angle, director):
        """[summary]

        Args:
            radius ([type]): [description]
            angle ([type]): [description]
        """
        DEG_TO_RAD = 2 * pi() / 360
        if director == "x":
            self.y = radius * cos(angle*DEG_TO_RAD)
            self.z = radius * cos(angle*DEG_TO_RAD)
        elif director == "y":
            self.x = radius * cos(angle*DEG_TO_RAD)
            self.z = radius * cos(angle*DEG_TO_RAD)
        elif director == "z":
            self.x = radius * cos(angle*DEG_TO_RAD)
            self.y = radius * cos(angle*DEG_TO_RAD)

    def add_system_id(self, system_id):
        self.system_id = system_id

    def add_lammps_type(self, particles_type):
        for i,typing in enumerate(particles_type):
            if self.type == typing:
                self.lammps_type = i+1