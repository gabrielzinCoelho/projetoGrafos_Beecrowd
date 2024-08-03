class Vertice:
    def __init__(self, *, id, vizinhos = []) -> None:
        self.__id = id
        self.__vizinhos = vizinhos # id_aresta, vizinho, peso_da_aresta
    
    def adicionarVizinho(self, *, idAresta, idVizinho, pesoAresta):
        self.__vizinhos.append((idAresta, idVizinho, pesoAresta))