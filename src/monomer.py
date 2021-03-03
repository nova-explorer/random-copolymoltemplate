import re
from numpy import cos, sin, pi, sqrt
from numpy.random import choice
from random import uniform
DEG_TO_RAD = 2 * pi / 360

class polymer():
    def __init__(self, monomer_list, probabilities, nb_monomer, director, s_id):
        self.monomer_list = monomer_list
        self.probabilities = probabilities
        self.nb_monomer = nb_monomer
        self.director = director
        self.create_polymer(s_id)

    def create_polymer(self, s_id):
        self.monomers = []
        position = {'x':0, 'y':0, 'z':0}
        inv_cnt = 1

        for _ in range(self.nb_monomer):
            current_monomer = choice(self.monomer_list, replace=False, p=self.probabilities)
            current_monomer = monomer(current_monomer.config, current_monomer.settings, inv_cnt, s_id)
            current_monomer.translate(position)
            self.monomers.append(current_monomer)
            position[self.director] += current_monomer.length
            inv_cnt = inv_cnt * current_monomer.get_inv_cnt()
            s_id += current_monomer.get_cnt()

    def translate(self, xyz):
        for i in self.monomers:
            i.translate(xyz)

    def rotate(self, amplitude):
        for i in self.monomers:
            angle = uniform(amplitude[0], amplitude[1])
            i.rotate(angle)

    def get_length(self):
        return sum([i.length for i in self.monomers])

    def get_cnt(self):
        cnt = 0
        for i in self.monomers:
            cnt += i.get_cnt()
        return cnt

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
    def __init__(self, config, settings, inv_cnt, s_id):
        self.config = config
        self.settings = settings
        self.evaluate_composition()
        self.create_atom_list(inv_cnt, s_id)
        self.evaluate_length()
        self.evaluate_probability()
        self.create_lammps_ids()
        self.add_bonds()

    def evaluate_composition(self):
        composition = [i.strip() for i in self.config.composition.split("+")]
        self.composition = []
        for i in composition:
            unit = re.search(r"(.*?)(?:\[|\{|$)", i)[1]
            repeat = 1
            director = self.settings.director

            if unit not in self.settings.sizes.keys():
                raise Exception("Type", i, "does not have a specified length")

            if '[' in i and ']' in i: # do an error case for [ and not ] or inverse
                repeat = re.search(r"\[(.*)\]", i)[1]
                try:
                    repeat = int(repeat)
                except:
                    raise ValueError("Repeat value in not an int")

            if '{' in i and '}' in i:
                director = re.search(r"\{(.*)\}", i)[1]
                try:
                    director = int(director)
                except:
                    raise ValueError("Director value in not an int")

            if director == 1:
                director = self.settings.direction_1
            elif director == 2:
                director = self.settings.direction_2
            elif director != self.settings.director:
                raise ValueError("Director for type", i, "needs to be 1 or 2")

            atom = {'unit':unit, 'd0':director}
            self.composition.extend([atom]*repeat)

    def create_atom_list(self, inv_cnt, s_id):
        self.atoms = []
        position = {'x':0, 'y':0, 'z':0}
        last_length = self.sin(self.composition[0])
        position[self.settings.director] -= last_length
        frag_flag = 0
        for atom_i in self.composition:
            unit = atom_i['unit']
            d0 = atom_i['d0']

            if d0 != self.settings.director:
                if not frag_flag:
                    position[d0] = 0
                    position[self.settings.director] += (self.sin(atom_i) + last_length)/2
                    frag_flag = 1
                else:
                    position[d0] += (self.sin(atom_i) + last_length)/2
            else:
                frag_flag = 0
                position[self.settings.direction_angle] = self.cos(atom_i)/2 * inv_cnt
                position[self.settings.director] += (self.sin(atom_i) + last_length)/2
            self.atoms.append(atom(s_id, unit, position))
            last_length = self.sin(atom_i)
            inv_cnt *= -1
            s_id += 1
        self.last_length = last_length

    def sin(self, atom):
        return self.settings.sizes[atom['unit']] * sin(self.settings.angles[atom['unit']]/2*DEG_TO_RAD)

    def cos(self, atom):
        return self.settings.sizes[atom['unit']] * cos(self.settings.angles[atom['unit']]/2*DEG_TO_RAD)

    def get_inv_cnt(self):
        if len(self.composition) % 2: # if even number of atoms
            inv_cnt = -1
        else:
            inv_cnt = 1
        return inv_cnt

    def evaluate_length(self):
        if self.config.length == "auto":
            self.length = self.atoms[-1].get_position()[self.settings.director] - self.atoms[0].get_position()[self.settings.director] + self.last_length
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

    def rotate(self, angle):
        p0 = self.atoms[0].get_position()
        p0[self.settings.direction_angle] -= self.cos(self.composition[0])/2

        d1 = self.settings.direction_1
        d2 = self.settings.direction_2

        for i in range(len(self.atoms)):
            if self.composition[i]['d0'] != self.settings.director:
                p1 = self.atoms[i].get_position()
                r = sqrt( (p1[d1]-p0[d1])**2 + (p1[d2]-p0[d2])**2 )
                p1[d1] = p0[d1] + r * cos(angle*DEG_TO_RAD)
                p1[d2] = p0[d2] + r * sin(angle*DEG_TO_RAD)
                self.atoms[i].move(p1)

    def create_lammps_ids(self):
        for i in self.atoms:
            i.add_lammps_type(self.settings.sizes.keys())

    def add_bonds(self):
        director = self.settings.director
        for i in range(len(self.atoms)-1):
            current = self.composition[i]['d0']
            previous = self.composition[i-1]['d0']
            after = self.composition[i+1]['d0']

            if current!=director and after!=director and previous==director:
                for j in range(i, len(self.atoms)):
                    if self.composition[j]['d0'] == director:
                        self.atoms[i].add_bonds(self.atoms[j].id)
                        break
            if current!=director and after==director:
                pass
            else:
                self.atoms[i].add_bonds(self.atoms[i+1].id)

    def get_cnt(self):
        return len(self.atoms)

class atom():
    def __init__(self, s_id, atom_type, xyz):
        self.id = s_id
        self.type = atom_type
        self.x = xyz['x']
        self.y = xyz['y']
        self.z = xyz['z']
        self.bonds = []

    def translate(self, xyz):
        self.x += xyz['x']
        self.y += xyz['y']
        self.z += xyz['z']

    def move(self, xyz):
        self.x = xyz['x']
        self.y = xyz['y']
        self.z = xyz['z']

    def add_lammps_type(self, particles_type):
        for i,typing in enumerate(particles_type):
            if self.type == typing:
                self.lammps_type = i+1

    def add_bonds(self, bond):
        self.bonds.append(bond)

    def get_position(self):
        return {'x':self.x, 'y':self.y, 'z':self.z}