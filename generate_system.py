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
        TODO: boundaries and lengths should have a common is_nested_list() flag.
        """
        if self.settings.director not in ["x", "y", "z"]:
            raise ValueError("Director not valid. Can be x, y or z.")
        self.define_directions()

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

        if self.is_length(self.settings.lengths):
            self.settings.lengths = self.to_dict(self.settings.lengths)
        else:
            raise ValueError("lengths are not dictionnary")

        for i in self.settings.monomers:
            i.add_particle_lengths(self.settings.lengths)

    def initialize_monomers(self):
        self.monomers = []
        for i in self.settings.monomers:
            self.monomers.append(monomer(i, self.settings.director))
        self.probabilities = [i.probability for i in self.monomers]
        if sum(self.probabilities) != 1:
            raise ValueError("Sum of probabilities is not equal to 1")

    def create_system(self):
        row_list = [] # along direction_1 (x)
        row_position = 0
        for row in range(self.settings.nb_chains_1):

            column_list = [] # along direction_2 (y)
            column_position = 0
            for column in range(self.settings.nb_chains_2):
                current_polymer = None
                current_polymer = polymer(self.monomers, self.probabilities, self.settings.nb_monomers, self.settings.director)
                current_polymer.translate([row_position, column_position, 0])

                column_list.append(current_polymer)
                column_position += self.settings.spacing

            row_list.append(column_list)
            row_position += self.settings.spacing
        self.polymers = row_list

    def evaluate_bounds(self):
        if self.settings.boundaries == "auto":
            min_ = 0
            max_ = 0
            length_dir_1 = self.settings.spacing * self.settings.nb_chains_1
            length_dir_2 = self.settings.spacing * self.settings.nb_chains_2
            for row in self.polymers:
                for poly in row:
                    current_length = poly.get_length()
                    if current_length > max_:
                        max_ = current_length
            self.settings.boundaries = [[0, length_dir_1],
                                        [0, length_dir_2],
                                        [0, max_]]

    def update_system_ids(self):
        cnt = 1
        for row in self.polymers:
            for poly in row:
                for mono in poly.monomers:
                    for atom in mono.atoms:
                        atom.add_system_id(cnt)
                        cnt += 1
        # cnt = 1
        # for row in range(len(self.polymers)):
        #     curr_row = self.polymers[row]
        #     for poly in range(len(curr_row)):
        #         curr_poly = curr_row[poly]
        #         for mono in range(len(curr_poly.monomers)):
        #             curr_mono = curr_poly.monomers[mono]
        #             for atom in range(len(curr_mono.atoms)):
        #                 current_atom = curr_mono.atoms[atom]
        #                 current_atom.add_system_id(cnt)
        #                 self.polymers[row][poly].monomers[mono].atoms[atom] = current_atom
        #                 cnt += 1

    def random_translation(self):
        if self.settings.translate:
            for row in self.polymers:
                for poly in row:
                    amplitude = uniform(self.settings.trans_amp[0],
                                        self.settings.trans_amp[1])
                    poly.translate([0,0,amplitude])

    def define_directions(self):
        direction_1 = ""
        direction_2 = ""

        if self.settings.director == "x":
            direction_1 = "y"
            direction_2 = "z"
        elif self.settings.director == "y":
            direction_1 = "x"
            direction_2 = "z"
        elif self.settings.director == "z":
            direction_1 = "x"
            direction_2 = "y"
        else:
            raise Exception("Impossible Error. Director not x, y or z")

        self.settings.direction_1 = direction_1
        self.settings.direction_2 = direction_2

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

    def is_length(self, value):
        value = [[j.strip() for j in i.strip().split(",")] for i in value.split(":")]
        if len(value) == 3 and sum([len(i)==2 for i in value]) and [self.is_float(i[1]) for i in value]:
            flag = True
        else:
            flag = False
        return flag

    def to_dict(self, value):
        value_dict = {}
        for i in value.split(":"):
            i = [j.strip() for j in i.split(",")]
            value_dict[i[0]] = float(i[1])
        return value_dict