import re
from numpy import cos, sin, pi
from numpy.random import choice
DEG_TO_RAD = 2 * pi / 360

class polymer():
    def __init__(self, monomer_list, probabilities, nb_monomer, director):
        self.monomer_list = monomer_list
        self.probabilities = probabilities
        self.nb_monomer = nb_monomer
        self.director = director
        self.create_polymer()

    def create_polymer(self):
        self.monomers = []
        position = {'x':0, 'y':0, 'z':0}
        inv_cnt = 1

        for _ in range(self.nb_monomer):
            current_monomer = choice(self.monomer_list, replace=False, p=self.probabilities)
            current_monomer = monomer(current_monomer.config, current_monomer.settings, inv_cnt)
            current_monomer.translate(position)
            self.monomers.append(current_monomer)
            position[self.director] += current_monomer.length
            inv_cnt = inv_cnt * current_monomer.get_inv_cnt()

    def translate(self, xyz):
        for i in self.monomers:
            i.translate(xyz)

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

class monomer():
    def __init__(self, config, settings, inv_cnt):
        self.config = config
        self.settings = settings
        self.evaluate_composition()
        self.create_atom_list(inv_cnt)
        self.evaluate_length()
        self.evaluate_probability()
        self.create_lammps_ids()

    def evaluate_composition(self):
        composition = [i.strip() for i in self.config.composition.split("+")]
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

        types = self.settings.sizes.keys()
        for i in self.composition:
            if i not in types:
                raise Exception("Type", i, "does not have a specified length")

    def create_atom_list(self, inv_cnt):
        self.atoms = []
        position = {'x':0, 'y':0, 'z':0}
        last_length = self.sin(self.composition[0])
        position[self.settings.director] -= last_length

        for i, atom_type in enumerate(self.composition):
            position[self.settings.director] += (self.sin(atom_type) + last_length)/2
            position[self.settings.direction_1] = self.cos(atom_type) / 2 * inv_cnt
            self.atoms.append( atom(i, atom_type, position, self.settings.sizes[atom_type]) )
            last_length = self.sin(atom_type)
            inv_cnt *= -1

        self.last_length = last_length

    def sin(self, atom_type):
        return self.settings.sizes[atom_type] * sin(self.settings.angles[atom_type]/2*DEG_TO_RAD)

    def cos(self, atom_type):
        return self.settings.sizes[atom_type] * cos(self.settings.angles[atom_type]/2*DEG_TO_RAD)

    def get_inv_cnt(self):
        if len(self.composition) % 2: # if even number of atoms
            inv_cnt = -1
        else:
            inv_cnt = 1
        return inv_cnt

    def evaluate_length(self):
        if self.config.length == "auto":
            self.length = self.atoms[-1].z - self.atoms[0].z + self.last_length
        else:
            try:
                self.length = float(self.config.length)
            except:
                raise ValueError("monomer length is neither auto nor a number")

    def evaluate_probability(self):
        try:
            prob = float(self.config.probability)
            if prob > 1:
                raise ValueError("Value too high")
            self.probability = prob
        except:
            print("probability is not a number")

    def translate(self, xyz):
        for i in self.atoms:
            i.translate(xyz)

    def create_lammps_ids(self):
        for i in self.atoms:
            i.add_lammps_type(self.settings.sizes.keys())

class atom():
    def __init__(self, monomer_id, atom_type, xyz, size):
        self.monomer_id = monomer_id
        self.type = atom_type
        self.x = xyz['x']
        self.y = xyz['y']
        self.z = xyz['z']
        self.size = size

    def translate(self, xyz):
        self.x += xyz['x']
        self.y += xyz['y']
        self.z += xyz['z']

    def add_system_id(self, system_id):
        self.system_id = system_id

    def add_lammps_type(self, particles_type):
        for i,typing in enumerate(particles_type):
            if self.type == typing:
                self.lammps_type = i+1