class Vertice:
    def __init__(self, *, vizinhos = {}) -> None:
        # self.__id = id
        self.vizinhos = dict(vizinhos) # id_aresta, vizinho, peso_da_aresta
    
    def adicionarVizinho(self, *, idAresta, idVizinho, pesoAresta):
        self.vizinhos[idAresta] = (idVizinho, pesoAresta)

    def __str__(self):
        return str(self.vizinhos)