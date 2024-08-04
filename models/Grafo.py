from .Vertice import Vertice

class Grafo:

    COR_BRANCO = 0
    COR_CINZA = 1
    COR_PRETO = 2

    def __init__(self, *, numVertices, arestas = [], ehDirecionado) -> None:
        self.__ehDirecionado = ehDirecionado
        self.__LA = [
            Vertice(id = i, vizinhos=[]) for i in range(numVertices)
        ]

        arestas.sort(
            key = lambda aresta : aresta[2] # ordenando arestas para priorizar ordem lexicográfica (padronizar saída)
        )

        for aresta in arestas:
            self.__adicionarAresta(*aresta)
    
    def __adicionarAresta(self, idAresta, v1, v2, pesoAresta):

        self.__LA[v1].adicionarVizinho(idAresta = idAresta, idVizinho = v2, pesoAresta = pesoAresta)

        if self.__ehDirecionado:
            self.__LA[v2].adicionarVizinho(idAresta = idAresta, idVizinho = v1, pesoAresta = pesoAresta)
    
    @staticmethod
    def __escolherVerticeInicial(listaCores):

        for indexVertice, corVertice in enumerate(listaCores):
            if corVertice == Grafo.COR_BRANCO:
                return indexVertice
        return None
    
    def buscaEmLargura(self):

        numVertices = len(self.__LA)

        listaPais = [(-1, -1)] * numVertices # idAresta, pai
        listaCores = [Grafo.COR_BRANCO] * numVertices
        # listaDistancias = [0] * numVertices

        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        while indexInicialBusca is not None:
            
            filaVisita = [indexInicialBusca]
            listaCores[indexInicialBusca] = Grafo.COR_CINZA
            listaPais[indexInicialBusca] = (None, indexInicialBusca)

            while filaVisita:
                verticeAtual = filaVisita.pop(0)

                for idAresta, idVizinho, _ in self.__LA[verticeAtual].vizinhos:
                    if listaCores[idVizinho] == Grafo.COR_BRANCO:
                        filaVisita.append(idVizinho)
                        listaCores[idVizinho] = Grafo.COR_CINZA
                        listaPais[idVizinho] = (idAresta, verticeAtual)
                listaCores[verticeAtual] = Grafo.COR_PRETO
            
            indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        return listaPais
    

    def buscaEmProfundidade(self):
        
        numVertices = len(self.__LA)

        listaPais = [(-1, -1)] * numVertices # idAresta, pai
        listaCores = [Grafo.COR_BRANCO] * numVertices
        # listaDistancias = [0] * numVertices

        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)

        while indexInicialBusca is not None:
            listaPais[indexInicialBusca] = (None, indexInicialBusca)
            listaCores[indexInicialBusca] = Grafo.COR_CINZA
            self.__buscaEmProfundidadeAux(indexInicialBusca, listaPais, listaCores)
            indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        return listaPais


    def __buscaEmProfundidadeAux(self, verticeAtual, listaPais, listaCores):
        for idAresta, idVizinho, _ in self.__LA[verticeAtual].vizinhos:
            if listaCores[idVizinho] == Grafo.COR_BRANCO:
                listaCores[idVizinho] = Grafo.COR_CINZA
                listaPais[idVizinho] = (idAresta, verticeAtual)
                self.__buscaEmProfundidadeAux(idVizinho, listaPais, listaCores)
        listaCores[verticeAtual] = Grafo.COR_PRETO