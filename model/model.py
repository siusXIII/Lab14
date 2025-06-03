import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._ordini = []
        self._allEdges = []
        self._idMapOrdini = {}

    def getStores(self):
        return DAO.DAOgetStores()

    def getNodes(self, store_id):
        self._ordini = DAO.DAOgetNodes(store_id)
        for ordine in self._ordini:
            self._idMapOrdini[ordine.order_id] = ordine
        return self._ordini

    def addEdges(self, store_id, giorni):
        self._allEdges = DAO.DAOgetArchi(store_id, giorni)
        for i in self._allEdges:
            u = self._idMapOrdini[i[0]]
            v = self._idMapOrdini[i[1]]
            if self._graph.has_edge(u, v):
                self._graph[u][v]["weight"] += i[2]
            else:
                self._graph.add_edge(u, v, weight=i[2])

    def build_graph(self, store_id, giorni):
        self._graph.clear()
        self.getNodes(int(store_id))
        if len(self._ordini) == 0:
            print("Attenzione, lista vuota!")
            return

        self._graph.add_nodes_from(self._ordini)
        self.addEdges(store_id, giorni)

    def getBFSfromTree(self, source):
        print(self._idMapOrdini[int(source)])
        tree = nx.bfs_tree(self._graph, self._idMapOrdini[int(source)])
        nodi = list(tree.nodes())
        return nodi[1:]

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def printGraphDetails(self):
        print(f"Numero nodi: {self._graph.number_of_nodes()}; Numero archi: {self._graph.number_of_edges()}")
