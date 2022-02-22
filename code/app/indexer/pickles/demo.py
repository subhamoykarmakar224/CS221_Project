# import pickle
#
#
# class Example:
#     def __init__(self, a=34, b='lol'):
#         self.a = a
#         self.b = b
#         self.d = {1: 'a', 2: 'b', 3: 'c'}
#
#
# obj1 = Example()
# obj2 = Example(100, 'Sam')
# dict1 = {}
# for i in range(1, 1000):
#     dict1[i] = i * 10
#
# pk1 = pickle.dumps(obj1)
# pk2 = pickle.dumps(obj2)
# pk3 = pickle.dumps(dict1)
#
# print(f"Pickle: \n{pk1}")
# print(f"Pickle: \n{pk2}")
# print(f"Pickle: \n{pk3}")
#
# print('------')
# upk1 = pickle.loads(pk1)
# upk2 = pickle.loads(pk2)
# upk3 = pickle.loads(pk3)
# print('Data: ', upk1.a)
# print('Data: ', upk2.a)
# print('Data: ', upk2.d)
# print('Data: ', upk3[40])

