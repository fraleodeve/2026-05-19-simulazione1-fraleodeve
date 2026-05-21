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
        genere = self._view._ddGenre.value
        if genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un genere."))
            self._view.update_page()
            return

        self._model.buildGraph(genere)
        nodi, archi = self._model.getDetails()
        nodoBest, valore = self._model.getBestNodo()
        lista = self._model.getOutput()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodi}", color = "red"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {archi}", color = "red"))
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {nodoBest}, con influenza: {valore}"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:", color = "red"))
        for el in lista:
            self._view.txt_result.controls.append(ft.Text(f"{el[0]} -> {el[1]}: {el[2]}"))

        self._view._ddArtist.disabled = False
        self._view._btnCreaGrafo.disabled = False

        artisti = self._model.getArtisti(genere)
        artistiDD = list(map(lambda x: ft.dropdown.Option(x), artisti))
        self._view._ddArtist.options = artistiDD

        self._view.update_page()

    def handleCammino(self,e):
        artista = self._view._ddArtist.value
        if artista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un artista."))
            self._view.update_page()
            return

        lista = self._model.cercaSoluzione(artista)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il cammino partendo da {artista}:"))
        for el in lista:
            self._view.txt_result.controls.append(ft.Text(f"- {el}"))
        self._view.update_page()
