from monomer import monomer_settings

class system_settings():
    def __init__(self, input_file):
        file_content = self.read_settings(input_file)
        self.generate_settings(file_content)

    def read_settings(self, input_file):
        with open(input_file, "rt") as file:
            all_lines = file.readlines()

        all_lines = [line.strip() for line in all_lines]

        setting_lines = []
        for i, line in enumerate(all_lines):
            line = self.cut_comments(line)

            if not line:
                continue
            elif self.unvalid_syntax(line, i):
                raise EOFError # Edit to real error
            else:
                setting_name, parameter = self.format_line(line)
                setting_lines.append([setting_name, parameter])
        return setting_lines

    def is_comment(self, line):
        flag = False
        if line[0] == "#":
            flag = True
        return flag

    def cut_comments(self, line):
        for i,char in enumerate(line):
            if char == "#":
                line = line[0:i]
                break
        return line

    def unvalid_syntax(self, line, i):
        flag = False
        line = line.split("=")
        if len(line) == 1:
            print("No '=' on line", i)
            flag = True
        elif len(line) > 2:
            print("More than one '=' on line", i)
            flag = True
        elif not line[1].strip():
            print("No value after '=' on line", i)
            flag = True
        return flag

    def format_line(self, line):
        setting, parameter = [i.strip() for i in line.split("=")]
        return setting, parameter

    def generate_settings(self, file_content):
        """[summary]

        Args:
            file_content ([type]): [description]
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
            elif s.startswith("monomer"):
                self.add_monomer_property(s,p)
            else:
                print("setting not implemented:",s,p)

    def generate_monomers(self, file_content):
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