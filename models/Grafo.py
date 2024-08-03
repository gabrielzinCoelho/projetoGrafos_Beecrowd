from .Vertice import Vertice

class Grafo:

    def __init__(self, *, numVertices, arestas = [], ehDirecionado) -> None:
        self.__ehDirecionado = ehDirecionado
        self.__LA = [
            Vertice(id = i, vizinhos=[]) for i in range(numVertices)
        ]
        for aresta in arestas:
            self.__adicionarAresta(*aresta)
    
    def __adicionarAresta(self, idAresta, v1, v2, pesoAresta):

        self.__LA[v1].adicionarVizinho(idAresta, v2, pesoAresta)

        if self.__ehDirecionado:
            self.__LA[v2].adicionarVizinho(idAresta, v1, pesoAresta)