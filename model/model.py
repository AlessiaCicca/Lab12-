import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.getNazioni=DAO.getNazioni()
        self.grafo = nx.Graph()
        self._idMap = {}

    def creaGrafo(self, nazione,anno):
        self.nodi = DAO.getNodi(nazione)
        self.grafo.add_nodes_from(self.nodi)
        for v in self.nodi:
            self._idMap[v.Retailer_code] = v
        self.addEdges(nazione,anno)
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def addEdges(self, nazione,anno):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni(nazione,anno)
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    self.grafo.add_edge(nodo1, nodo2, weight=connessione.peso)

    def volume(self):
        dizio={}
        for nodo in self.grafo.nodes:
            somma=0
            for vicini in self.grafo.neighbors(nodo):
                somma+= self.grafo[nodo][vicini]["weight"]
            dizio[nodo.Retailer_code]=somma
        dizioOrder=list(sorted(dizio.items(), key=lambda item:item[1],reverse=True))
        return dizioOrder

    def getBestPath(self, limiteEsatto):
        self._soluzione = []
        self._costoMigliore = 0
        for nodo in self.grafo.nodes:
            parziale=[nodo]
            self._ricorsione(parziale,limiteEsatto+1)
        return self._costoMigliore,self._soluzione

    def _ricorsione(self, parziale, limiteEsatto):
        if len(parziale) == limiteEsatto:
            if self.peso(parziale)>self._costoMigliore:
                self._soluzione=copy.deepcopy(parziale)
                self._costoMigliore=self.peso(parziale)

        if len(parziale)<limiteEsatto:
            for n in self.grafo.neighbors(parziale[-1]):
                if len(parziale)==limiteEsatto-1 and n==parziale[0]:
                        parziale.append(n)
                        self._ricorsione(parziale, limiteEsatto)
                        parziale.pop()
                if len(parziale)<limiteEsatto-1 and n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale, limiteEsatto)
                    parziale.pop()

    def peso(self, listaNodi):
        pesoTot = 0
        for i in range(0, len(listaNodi) - 1):
            pesoTot += self.grafo[listaNodi[i]][listaNodi[i + 1]]["weight"]
        return pesoTot