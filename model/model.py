import copy
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

        self._soluzione_migliore = []

    def cercaSoluzione(self, artista):
        self._soluzione_migliore = []
        nodo = self.getArtista(artista)
        parziale = [nodo]

        # self.ricorsione(float("-inf"), parziale)
        self._ricorsione(parziale)

        print(nx.descendants(self._grafo, nodo))
        print(f"----{self._soluzione_migliore}")

        return self._soluzione_migliore

    def ricorsione(self, peso_ulitmo_arco, parziale):
        if len(parziale) > len(self._soluzione_migliore):
            self._soluzione_migliore = copy.deepcopy(parziale)

        nodo_corrente = parziale[-1]

        for vicino in self._grafo.neighbors(nodo_corrente):
            peso_arco_corrente = self._grafo[nodo_corrente][vicino][0]["weight"]
            if vicino not in parziale and peso_arco_corrente > peso_ulitmo_arco:
                parziale.append(vicino)
                self.ricorsione(peso_arco_corrente, parziale)
                parziale.pop()

    def _ricorsione(self, parziale):
        if len(parziale) > len(self._soluzione_migliore):
            self._soluzione_migliore = copy.deepcopy(parziale)

        ultimo = parziale[-1]
        for vicino in self._grafo.successors(ultimo):
            if vicino in parziale:
                continue
            peso = self._grafo[ultimo][vicino][0]["weight"]
            if len(parziale) > 1:
                penultimo = parziale[-2]
                peso_precedente = self._grafo[penultimo][ultimo][0]["weight"]
                if peso <= peso_precedente:
                    continue
            parziale.append(vicino)
            self._ricorsione(parziale)
            parziale.pop()

    def buildGraph(self, genere):
        self._grafo.clear()
        chiave = self.getGenere(genere)

        artisti = DAO.getArtisti(int(chiave))
        listaA = []
        for ele in artisti:
            listaA.append(ele.ArtistId)

        self._grafo.add_nodes_from(artisti)

        dictP = self.calcolaPopolarità(genere)
        dictC = self.calcolaClienti(genere)

        for key, val in dictC.items():
            listaC = []
            for el in val:
                if el in listaA:
                    listaC.append(el)
            if len(listaC) > 1:
                myEdges = itertools.combinations(listaC, 2)
                for i in myEdges:
                    if dictP[i[0]] > dictP[i[1]] and not self._grafo.has_edge(self._idMapArtisti[i[0]], self._idMapArtisti[i[1]]):
                        self._grafo.add_edge(self._idMapArtisti[i[0]], self._idMapArtisti[i[1]],weight = dictP[i[0]] + dictP[i[1]])
                    elif dictP[i[0]] < dictP[i[1]] and not self._grafo.has_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]]):
                        self._grafo.add_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]],weight = dictP[i[0]] + dictP[i[1]])
                    elif dictP[i[0]] == dictP[i[1]] and not self._grafo.has_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]]):
                        self._grafo.add_edge(self._idMapArtisti[i[0]], self._idMapArtisti[i[1]],weight=dictP[i[0]] + dictP[i[1]])
                        self._grafo.add_edge(self._idMapArtisti[i[1]], self._idMapArtisti[i[0]],weight=dictP[i[0]] + dictP[i[1]])

    def calcolaPopolarità(self, genere):
        compensi = DAO.getEdges()
        dizionario = defaultdict(int)
        for el in compensi:
            chiave = self.getGenere(genere)
            if chiave == el.GenreId:
                dizionario[el.ArtistId] += 1
        return dizionario

    def calcolaClienti(self, genere):
        compensi = DAO.getEdges()
        dizionario = defaultdict(set)
        for el in compensi:
            chiave = self.getGenere(genere)
            if chiave == el.GenreId:
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
        listaD = listaO[:5]
        return listaD

    def getBestNodo(self):
        nodo = max(self._grafo.nodes, key=lambda v: self._grafo.out_degree(v, weight='weight') - self._grafo.in_degree(v, weight='weight'))
        valore = self._grafo.out_degree(nodo, weight='weight')- self._grafo.in_degree(nodo, weight='weight')
        return nodo, valore

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getArtisti(self, genere):
        chiave = self.getGenere(genere)
        lista = DAO.getArtisti(chiave)
        lista.sort(key = lambda x: x.Name)
        return lista

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getGenere(self, genere):
        chiave = 0
        for key, val in self._idMapGeneri.items():
            if val.Name == genere:
                chiave = key
        return chiave

    def getArtista(self, artista):
        for key, val in self._idMapArtisti.items():
            if val.Name == artista:
                return val
