"""
Definition of the system_settings class reads the input file and then stores unformatted settings.

Usage: settings = system_settings(input_file="path/to/input_file")

Requires scripts: monomer.py

Raises:
    EOFError: Invalid syntax regarding the use of '=' in the input file
TODO: *settings could be evaluated here
      *invalid syntax should be extended to missing brackets
      *invalid syntax should be extended to not recognized settings
      *direction_angle should also accept 1 and 2
"""
from monomer import monomer_settings

class system_settings():
    """Generates system settings from input file

    Args:
        - input_file (string): path to the input file.

    Attributes:
        - monomers (list of monomer_settings):
        - director (string): Director for the polymer chains. Needs to be x,y or z. Director, direction_1 and direction_2 need to be different.
        - direction_1 (string): Direction 1 for the polymer chains. Needs to be orthogonal from director and x,y or z. Director, direction_1 and direction_2 need to be different.
        - direction_2 (string):Direction 2 for the polymer chains. Needs to be orthogonal from director and x,y or z. Director, direction_1 and direction_2 need to be different.
        - nb_chains_1 (int in string): Number of chains that will be placed in direction_1.
        - nb_chains_2 (int in string): Number of chains that will be placed in direction_2.
        - nb_monomers_per_chain (int in string): Number of monomers per chain.
        - spacing_between_chains (float in string): Empty space between each chain.
        - translate (bool in string): Wether or not to apply a random translation on the chains.
        - trans_amp (list of floats in string): Range of possible values for the random translation
        - rotate (bool in string): Wether or not to apply a random rotation on lateral fragments.
        - rot_amp (list of floats in string): Range of possible values for the random rotation
        - boundaries (nested list of floats in string or string): Boundaries of the system. If auto, boundaries will be calculated by the script
        - direction_angle (string): Direction in which the angled bonds (zigzag conformation) are formed. Needs to be orthogonal from director and x,y or z.
        - sizes (dictionary of floats in string): Size of the particles in the system.
        - angles (dictionary of floats in string): Angles of the bonds of the particles.
    """
    def __init__(self, input_file):
        """Class creator. Defines all the recognized settings.

        Args:
            input_file (string): Path to the input file.
        """
        print("Reading input file ...")
        file_content = self.read_settings(input_file)
        self.generate_settings(file_content)
        print("Input file read!")

    def read_settings(self, input_file):
        """Read lines from the input file, removes comments and formats the lines with settings

        Args:
            input_file (string): Path to the input file.

        Returns:
            nested list of strings: Settings of the system. One item of the list corresponds to a list containing the setting name and the value of the parameter in a string format.
        """
        with open(input_file, "rt") as file:
            all_lines = file.readlines()

        all_lines = [line.strip() for line in all_lines]

        setting_lines = []
        for i, line in enumerate(all_lines):
            line = self.cut_comments(line)

            if not line:
                continue
            self.unvalid_syntax(line, i)
            setting_name, parameter = self.format_line(line)
            setting_lines.append([setting_name, parameter])
        return setting_lines

    def cut_comments(self, line):
        """Removes comments from the line. Cuts everything after '#'.

        Args:
            line (string): Single line of the input file

        Returns:
            string: Single line without the comments
        """
        for i,char in enumerate(line):
            if char == "#":
                line = line[0:i]
                break
        return line

    def unvalid_syntax(self, line, i):
        """Checks if the line has correct syntax.

        Args:
            line (string): Single line of the input file
            i (int): Position of the line in the input file. Serves only as feedback

        Raises:
            EOFError: No '=' in the line
            EOFError: More than one '=' in the line
            EOFError: '=' with no parameter value after
        """
        line = line.split("=")
        if len(line) == 1:
            raise EOFError("No '=' on line", i)
        elif len(line) > 2:
            raise EOFError("More than one '=' on line", i)
        elif not line[1].strip():
            raise EOFError("No value after '=' on line", i)

    def format_line(self, line):
        """Formats the line by splitting it at the '=' and removing white spaces in both parts.

        Args:
            line (string): Single line of the input file.

        Returns:
            string: Name of the setting
            string: Value of the parameter
        """
        setting, parameter = [i.strip() for i in line.split("=")]
        return setting, parameter

    def generate_settings(self, file_content):
        """Transfers the settings from a nested list format to attributes of the class.

        Args:
            file_content (nested list of strings): Settings in a clustered format
        """
        self.monomers = self.generate_monomers(file_content)
        for setting in file_content:

            s = setting[0]
            p = setting[1]

            if s == "director":
                self.director = p
            elif s == "direction_1":
                self.direction_1 = p
            elif s == "direction_2":
                self.direction_2 = p
            elif s == "nb_chains_1":
                self.nb_chains_1 = p
            elif s == "nb_chains_2":
                self.nb_chains_2 = p
            elif s == "nb_monomers_per_chain":
                self.nb_monomers = p
            elif s == "spacing_between_chains":
                self.spacing = p
            elif s == "translate_on_director":
                self.translate = p
            elif s == "translation_amplitude":
                self.trans_amp = p
            elif s == "rotate_along_director":
                self.rotate = p
            elif s == "rotation_amplitude":
                self.rot_amp = p
            elif s == "boundaries":
                self.boundaries = p
            elif s == "direction_angle":
                self.direction_angle = p
            elif s == "sizes":
                self.sizes = p
            elif s == "angles":
                self.angles = p
            elif s == "groups":
                self.groups = p
            elif s.startswith("monomer"):
                self.add_monomer_property(s,p)
            else:
                print("setting not implemented:",s,p)

    def generate_monomers(self, file_content):
        """Generate the monomer_settings class which will be used to store settings that are relevant to only one monomer.

        Args:
            file_content (nested list of strings): Settings in a clustered format

        Returns:
            list of monomer_settings: List containing the monomer_settings classes of each monomer.
        """
        id_max = 0
        for setting in file_content:
            if setting[0].startswith("monomer"):
                id_current = int(setting[0][7])
                if id_current > id_max:
                    id_max = id_current
        monomers = []
        for i in range(id_max):
            monomers.append(monomer_settings(i))
        return monomers

    def add_monomer_property(self, setting, parameter):
        """Adds a setting value to the corresponding monomer_settings.

        Args:
            setting (string): Name of the setting
            parameter (string): Value of the setting
        """
        m_id, setting = setting.split("_")
        m_id = int(m_id[-1]) - 1

        if setting == "composition":
            self.monomers[m_id].add_composition(parameter)
        elif setting == "length":
            self.monomers[m_id].add_length(parameter)
        elif setting == "probability":
            self.monomers[m_id].add_probability(parameter)
        else:
            print("monomer setting not implemented yet")