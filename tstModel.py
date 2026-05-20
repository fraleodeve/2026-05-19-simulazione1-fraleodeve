from model.model import Model

mymodel = Model()
mymodel.buildGraph("Jazz")
n, a = mymodel.getDetails()
print(f"Nodi: {n}, archi: {a}")