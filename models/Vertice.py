class Vertice:
    def __init__(self, *, id, vizinhos = []) -> None:
        # self.__id = id
        self.vizinhos = list(vizinhos) # id_aresta, vizinho, peso_da_aresta
    
    def adicionarVizinho(self, *, idAresta, idVizinho, pesoAresta):
        self.vizinhos.append((idAresta, idVizinho, pesoAresta))