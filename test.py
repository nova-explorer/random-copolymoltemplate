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