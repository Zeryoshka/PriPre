from const_model import Const

model = Const()
model.load()
print(model.predict([0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]))
