import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getAllGeneri()
        generiDD = list(map(lambda x: ft.dropdown.Option(x), generi))
        self._view._ddGenre.options = generiDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genere = self._view.ddGenre.value
        self._model.buildGraph(genere)
        nodi, archi = self._model.getDetails()
        lista = self._model.getOutput()
        nodoBest, valore = self._model.getBestNodo()

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass