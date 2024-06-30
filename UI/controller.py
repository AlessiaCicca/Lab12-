import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        nazioni=self._model.getNazioni
        for nazione in nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(
                text=nazione))
        ann = "201"
        for i in range(5, 9):
            anno = ann + str(i)
            self._view.ddyear.options.append(ft.dropdown.Option(
                text=anno))



    def handle_graph(self, e):
        nazione = self._view.ddcountry.value
        if nazione is None:
            self._view.create_alert("Selezionare una Nazione")
            return
        anno = self._view.ddyear.value
        if anno is None:
            self._view.create_alert("Selezionare un Anno")
            return
        grafo = self._model.creaGrafo(nazione, int(anno))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        self._view.update_page()



    def handle_volume(self, e):
        lista=self._model.volume()
        for (nodo,volume) in lista:
            self._view.txtOut2.controls.append(ft.Text(f"{self._model._idMap[nodo]} -> {volume}"))
        self._view.update_page()

    def handle_path(self, e):
        numero = self._view.txtN.value
        if numero == "":
            self._view.create_alert("Inserire un numero")
            return
        if int(numero) < 2:
            self._view.create_alert("Inserire un numero maggiore di 2")
            return
        costo, listaNodi = self._model.getBestPath(int(numero))
        self._view.txtOut3.controls.append(ft.Text(f"La soluzione migliore ha peso totale pari a {costo}"))
        for i in range(0, len(listaNodi)-1):
            self._view.txtOut3.controls.append(ft.Text(f"{listaNodi[i]} -> {listaNodi[i+1]}: {self._model.grafo[listaNodi[i]][listaNodi[i+1]]["weight"]}"))
        self._view.update_page()
