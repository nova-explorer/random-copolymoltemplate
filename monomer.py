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
        for i in range(self.nb_monomer):
            current_monomer = choice(self.monomer_list, replace=False, p=self.probabilities)
            current_monomer.translate(0, 0, position)
            self.monomers.append(current_monomer)
            position += current_monomer.length

    def translate(self, coords):
        for i in self.monomers:
            i.translate(coords)

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

    def add_particle_lengths(self, lengths):
        self.particles_lengths = lengths

class monomer():
    def __init__(self, settings, director):
        self.settings = settings
        self.director = director
        self.evaluate_composition()
        self.create_atom_list()
        self.evaluate_length()
        self.evaluate_probability()

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

        types = self.settings.particles_lengths.keys()
        for i in self.composition:
            if i not in types:
                raise Exception("Type", i, "does not have a specified length")

    def create_atom_list(self):
        self.atoms = []
        for i, atom_type in enumerate(self.composition):
            self.atoms.append( atom(i, atom_type, [0,0,0], self.settings.length[atom_type]) )

        for i in self.atoms[1::]:
            if self.director == "x":
                i.translate([ self.atoms[i.id-1].length, 0, 0 ])
            elif self.director == "y":
                i.translate([ 0, self.atoms[i.id-1].length, 0 ])
            elif self.director == "z":
                i.translate([ 0, 0, self.atoms[i.id-1].length ])

    def evaluate_length(self):
        if self.settings.length == "auto":
            self.length = sum([i.length for i in self.atoms])
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
            self.prob = prob
        except:
            print("probability is not a number")

    def translate(self, coords):
        for i in self.atoms:
            i.translate(coords)

class atom():
    def __init__(self, monomer_id, atom_type, xyz, length):
        self.monomer_id = monomer_id
        self.atom_type = atom_type
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
        self.length = length

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