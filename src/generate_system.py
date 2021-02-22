from monomer import monomer, polymer
from numpy.random import choice
from random import uniform

class system():
    def __init__(self, settings):
        self.settings = settings
        self.evaluate_settings()
        self.initialize_monomers()
        self.create_system()
        self.evaluate_bounds()
        self.update_system_ids()
        self.random_translation()

    def evaluate_settings(self):
        """[summary]

        Raises:
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
        TODO: boundaries and sizes should have a common is_nested_list() flag.
        """
        self.check_directions(self.settings.director, self.settings.direction_1, self.settings.direction_2, self.settings.direction_angle)

        if self.is_posint(self.settings.nb_chains_1):
            self.settings.nb_chains_1 = int(self.settings.nb_chains_1)
        else:
            raise ValueError("nb_chains_1 is not an integer")

        if self.is_posint(self.settings.nb_chains_2):
            self.settings.nb_chains_2 = int(self.settings.nb_chains_2)
        else:
            raise ValueError("nb_chains_2 is not an integer")

        if self.is_posint(self.settings.nb_monomers):
            self.settings.nb_monomers = int(self.settings.nb_monomers)
        else:
            raise ValueError("nb_monomers_per_chains is not an integer")

        if self.is_float(self.settings.spacing):
            self.settings.spacing = float(self.settings.spacing)
        else:
            raise ValueError("spacing_between_chains is not a number")

        if self.is_bool(self.settings.translate):
            self.settings.translate = self.to_bool(self.settings.translate)
        else:
            raise ValueError("translate_on_director is not a boolean")

        if self.is_min_max(self.settings.trans_amp):
            self.settings.trans_amp = self.to_min_max(self.settings.trans_amp)
        else:
            raise ValueError("translation_amplitude is not a list")

        if self.is_bool(self.settings.rotate):
            self.settings.rotate = self.to_bool(self.settings.rotate)
        else:
            raise ValueError("rotate_along_director is not a boolean")

        if self.is_min_max(self.settings.rot_amp):
            self.settings.rot_amp = self.to_min_max(self.settings.rot_amp)
        else:
            raise ValueError("rotation_amplitude is not a list")

        if self.is_boundary(self.settings.boundaries):
            if self.settings.boundaries != "auto":
                self.settings.boundaries = self.to_nested_float_list(self.settings.boundaries)
        else:
            raise ValueError("boundaries is not auto or a nested list of floats")

        if self.is_dict_of_float(self.settings.sizes):
            self.settings.sizes = self.to_dict_of_float(self.settings.sizes)
        else:
            raise ValueError("sizes are not dictionnary")

        if self.is_dict_of_float(self.settings.angles):
            self.settings.angles = self.to_dict_of_float(self.settings.angles)
        else:
            raise ValueError("angles are not dictionnary")

    def initialize_monomers(self):
        self.monomers = []
        for i in self.settings.monomers:
            self.monomers.append(monomer(i, self.settings, inv_cnt=1))
        self.probabilities = [i.probability for i in self.monomers]
        if sum(self.probabilities) != 1:
            raise ValueError("Sum of probabilities is not equal to 1")

    def create_system(self):
        position = {'x':0, 'y':0, 'z':0}
        row_list = [] # along direction_1
        for _ in range(self.settings.nb_chains_1):
            column_list = [] # along direction_2
            position[self.settings.direction_2] = 0
            for _ in range(self.settings.nb_chains_2):
                current_polymer = polymer(self.monomers, self.probabilities, self.settings.nb_monomers, self.settings.director)
                current_polymer.translate(position)
                column_list.append(current_polymer)
                position[self.settings.direction_2] += self.settings.spacing
            row_list.append(column_list)
            position[self.settings.direction_1] += self.settings.spacing
        self.polymers = row_list

    def evaluate_bounds(self):
        if self.settings.boundaries == "auto":
            boundaries = {'x':0, 'y':0, 'z':0}
            max_ = 0
            boundaries[self.settings.direction_1] = self.settings.spacing * self.settings.nb_chains_1
            boundaries[self.settings.direction_2] = self.settings.spacing * self.settings.nb_chains_2
            for row in self.polymers:
                for poly in row:
                    current_length = poly.get_length()
                    if current_length > max_:
                        max_ = current_length
            boundaries[self.settings.director] = max_
            self.settings.boundaries = boundaries

    def update_system_ids(self):
        cnt = 1
        for row in self.polymers:
            for poly in row:
                for mono in poly.monomers:
                    for atom in mono.atoms:
                        atom.add_system_id(cnt)
                        cnt += 1

    def random_translation(self):
        position = {'x':0, 'y':0, 'z':0}
        if self.settings.translate:
            for row in self.polymers:
                for poly in row:
                    amplitude = uniform(self.settings.trans_amp[0],
                                        self.settings.trans_amp[1])
                    position[self.settings.director] = amplitude
                    poly.translate(position)

    def check_directions(self, d0, d1, d2, da):
        coords = ["x","y","z"]
        if d0 not in coords:
            raise Exception("director not x, y or z")

        if d1 not in coords:
            raise Exception("direction_1 not x, y or z")
        elif d1 == d0:
            raise Exception("direction_1 needs to be different from director")

        if d2 not in coords:
            raise Exception("direction_2 not x, y or z")
        elif d2 == d0 or d2 == d1:
            raise Exception("direction_2 needs to be different from director or direction_1")

        if da not in coords:
            raise Exception("direction_angle not x, y or z")
        elif da == d0:
            raise Exception("direction_angle needs to be different from director")

    def is_posint(self, value):
        try:
            if int(value) < 0:
                raise Exception
            flag = True
        except:
            flag = False
        return flag

    def is_float(self, value):
        try:
            float(value)
            flag = True
        except:
            flag = False
        return flag

    def is_bool(self, value):
        if value=="true" or value=="True" or value==1 or value=="yes" or value=="Yes":
            flag = True
        elif value=="false" or value=="False" or value==0 or value=="no" or value=="No":
            flag = True
        else:
            flag = False
        return flag

    def to_bool(self, value):
        if value=="true" or value=="True" or value==1 or value=="yes" or value=="Yes":
            value = True
        elif value=="false" or value=="False" or value==0 or value=="no" or value=="No":
            value = False
        else:
            raise Exception("Impossible Error. value is not convertible to boolean")
        return value

    def is_min_max(self, value):
        value = [i.strip() for i in value.split(",")]
        if len(value) == 2 and sum([True for i in value if self.is_float(i)]) == len(value):
            flag = True
        else:
            flag = False
        return flag

    def to_min_max(self, value):
        value = [float(i.strip()) for i in value.split(",")]
        value.sort()
        return value

    def is_boundary(self, value):
        if value == "auto":
            flag = True
        elif self.is_nested_float_list(value):
            flag = True
        else:
            flag = False
        return flag

    def is_nested_float_list(self, value):
        value = [[j.strip() for j in i.strip().split(",")] for i in value.split(":")]
        if len(value) == 3 and sum([len(i)==2 for i in value]) and [self.is_float(j) for i in value for j in i]:
            flag = True
        else:
            flag = False
        return flag

    def to_nested_float_list(self, value):
        value = [[float(j.strip()) for j in i.strip().split(",")] for i in value.split(":")]
        return value

    def is_dict_of_float(self, value):
        value = [[j.strip() for j in i.strip().split(",")] for i in value.split(":")]
        if len(value) == 3 and sum([len(i)==2 for i in value]) and [self.is_float(i[1]) for i in value]:
            flag = True
        else:
            flag = False
        return flag

    def to_dict_of_float(self, value):
        value_dict = {}
        for i in value.split(":"):
            i = [j.strip() for j in i.split(",")]
            value_dict[i[0]] = float(i[1])
        return value_dict