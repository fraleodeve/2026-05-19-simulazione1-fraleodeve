from model.model import Model

mymodel = Model()
mymodel.buildGraph("Latin")
n, a = mymodel.getDetails()
print(f"Nodi: {n}, archi: {a}")