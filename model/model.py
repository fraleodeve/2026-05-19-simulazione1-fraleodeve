import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.MultiDiGraph()

        self._idMapArtisti = {}
        for el in DAO.getAllArtisti():
            self._idMapArtisti[el.ArtistId] = el

        self._idMapGeneri = {}
        for el in DAO.getAllGeneri():
            self._idMapGeneri[el.GenreId] = el

    def buildGraph(self, genere):
        chiave = 0
        self._grafo.clear()
        for key, val in self._idMapGeneri.items():
            if val.Name == genere:
                chiave = key

        artisti = DAO.getArtisti(int(chiave))
        listaA = []
        for ele in artisti:
            listaA.append(ele.ArtistId)

        self._grafo.add_nodes_from(artisti)

        dictP = self.calcolaPopolarità()
        sortedDictP = sorted(dictP.items(), key=lambda x: x[0])
        for i in sortedDictP:
            print(i)
        dictC = self.calcolaClienti()
        for key, val in dictC.items():
            print(key, val)

        for key, val in dictC.items():
            listaC = []
            for el in val:
                if el in listaA:
                    listaC.append(el)
            if len(listaC) > 1:
                print(listaC)
                myEdges = itertools.combinations(listaC, 2)
                for i in myEdges:
                    if dictP[i[0]] > dictP[i[1]] and not self._grafo.has_edge(self._idMapArtisti[i[0]], self._idMapArtisti[i[1]]):
                        print("---------------------------------", i[0], i[1], dictP[i[0]] + dictP[i[1]])
                        self._grafo.add_edge(self._idMapArtisti[i[0]], self._idMapArtisti[i[1]], weight = dictP[i[0]] + dictP[i[1]])
                    elif dictP[i[0]] < dictP[i[1]] and not self._grafo.has_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]]):
                        self._grafo.add_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]], weight = dictP[i[0]] + dictP[i[1]])
                    #else:
                        #self._grafo.add_edge(self._idMapArtisti[i[0]], self._idMapArtisti[i[1]],weight=dictP[i[0]] + dictP[i[1]])
                        #self._grafo.add_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]],weight=dictP[i[0]] + dictP[i[1]])

        listaO = self.getOutput()
        print(listaO)

    def calcolaPopolarità(self):
        compensi = DAO.getEdges()
        dizionario = defaultdict(int)
        for el in compensi:
            dizionario[el.ArtistId] += 1
        return dizionario

    def calcolaClienti(self):
        compensi = DAO.getEdges()
        dizionario = defaultdict(set)
        for el in compensi:
            dizionario[el.CustomerId].add(el.ArtistId)
        return dizionario

    def getOutput(self):
        listaO = []
        for key, val, data in self._grafo.edges(data=True):
            lista = list()
            lista.append(key)
            lista.append(val)
            lista.append(data["weight"])
            listaO.append(lista)
        listaO.sort(key = lambda x: x[2], reverse=True)
        print(listaO)

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)