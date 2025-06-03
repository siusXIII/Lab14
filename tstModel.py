from model.model import Model

myModel = Model()
myModel.build_graph(3, 5)
myModel.printGraphDetails()

myModel.getBFSfromTree(9)
