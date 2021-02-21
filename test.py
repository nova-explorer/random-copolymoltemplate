class test():
    def __init__(self):
        pass
    def add_property(self, prop):
        self.prop = prop

# test_list = [test()]*10
test_list = []
for i in range(10):
    test_list.append(test())
cnt = 0
for i in test_list:
    i.add_property(cnt)
    cnt+=1

for i in test_list:
    print(i.prop)

class monomer():
    def __init__(self, settings, director, inversion_counter):
        self.mono_settings = mono_settings
        self.sys_settings = sys_settings
        self.evaluate_composition()
        self.create_atom_list(inversion_counter)
        self.evaluate_length()
        self.evaluate_probability()
        self.create_lammps_ids()

def create_atom_list(self, inversion_counter):
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