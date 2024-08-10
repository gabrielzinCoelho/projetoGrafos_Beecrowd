import heapq

from .Vertice import Vertice

class Grafo:

    COR_BRANCO = 0
    COR_CINZA = 1
    COR_PRETO = 2

    def __init__(self, *, numVertices, arestas = [], ehDirecionado) -> None:
        self.__numVertices = numVertices
        self.ehDirecionado = ehDirecionado
        self.__LA = [
            # Vertice(id = i, vizinhos=[]) for i in range(numVertices)
            Vertice(vizinhos=[]) for _ in range(numVertices)
        ]

        if ehDirecionado:
            arestas.sort(
                key = lambda aresta : aresta[2] # ordenando arestas para priorizar ordem lexicográfica (padronizar saída beecrowd)
            )
            adicionarAresta = self.__adicionarArestasD
        else:
            arestas.sort(
                key = lambda aresta : (aresta[2], aresta[1]) # ordenando arestas para priorizar ordem lexicográfica (padronizar saída beecrowd)
            )
            adicionarAresta = self.__adicionarArestasND

        for aresta in arestas:
            adicionarAresta(*aresta)
    
    def __adicionarArestasD(self, idAresta, v1, v2, pesoAresta):

        self.__LA[v1].adicionarVizinho(idAresta = idAresta, idVizinho = v2, pesoAresta = pesoAresta)
    
    def __adicionarArestasND(self, idAresta, v1, v2, pesoAresta):

        self.__LA[v1].adicionarVizinho(idAresta = idAresta, idVizinho = v2, pesoAresta = pesoAresta)
        self.__LA[v2].adicionarVizinho(idAresta = idAresta, idVizinho = v1, pesoAresta = pesoAresta)
    
    @staticmethod
    def __escolherVerticeInicial(listaCores):

        for indexVertice, corVertice in enumerate(listaCores):
            if corVertice == Grafo.COR_BRANCO:
                return indexVertice
        return None
    
    
    def buscaEmLargura(self):

        listaPais = [(-1, -1)] * self.__numVertices # idAresta, pai
        listaCores = [Grafo.COR_BRANCO] * self.__numVertices
        listaDistancias = [0] * self.__numVertices

        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        while indexInicialBusca is not None:
            
            filaVisita = [indexInicialBusca]
            listaCores[indexInicialBusca] = Grafo.COR_CINZA
            listaPais[indexInicialBusca] = (None, indexInicialBusca)

            while filaVisita:
                verticeAtual = filaVisita.pop(0)
                novaDistancia = listaDistancias[verticeAtual] + 1

                for idAresta, idVizinho, _ in self.__LA[verticeAtual].vizinhos:
                    if listaCores[idVizinho] == Grafo.COR_BRANCO:
                        filaVisita.append(idVizinho)
                        listaCores[idVizinho] = Grafo.COR_CINZA
                        listaPais[idVizinho] = (idAresta, verticeAtual)
                        listaDistancias[idVizinho] = novaDistancia
                listaCores[verticeAtual] = Grafo.COR_PRETO
            
            indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        return listaPais, listaDistancias
    

    def buscaEmProfundidade(self, callbackPreto = None):

        def buscaEmProfundidadeAux(verticeAtual):
            for idAresta, idVizinho, _ in self.__LA[verticeAtual].vizinhos:
                if listaCores[idVizinho] == Grafo.COR_BRANCO:
                    listaCores[idVizinho] = Grafo.COR_CINZA
                    listaPais[idVizinho] = (idAresta, verticeAtual)
                    buscaEmProfundidadeAux(idVizinho)
            listaCores[verticeAtual] = Grafo.COR_PRETO
            if callbackPreto is not None:
                callbackPreto(verticeAtual)
    

        listaPais = [(-1, -1)] * self.__numVertices # idAresta, pai
        listaCores = [Grafo.COR_BRANCO] * self.__numVertices

        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)

        while indexInicialBusca is not None:
            listaPais[indexInicialBusca] = (None, indexInicialBusca)
            listaCores[indexInicialBusca] = Grafo.COR_CINZA
            buscaEmProfundidadeAux(indexInicialBusca)
            indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        return listaPais

    def arvoreDeLargura(self):

        listaCores = [Grafo.COR_BRANCO] * self.__numVertices
        arvoreDeLargura = []
        
        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        filaVisita = [indexInicialBusca]
        listaCores[indexInicialBusca] = Grafo.COR_CINZA
    
        while filaVisita:
            verticeAtual = filaVisita.pop(0)

            for idAresta, idVizinho, _ in self.__LA[verticeAtual].vizinhos:
                if listaCores[idVizinho] == Grafo.COR_BRANCO:
                    filaVisita.append(idVizinho)
                    listaCores[idVizinho] = Grafo.COR_CINZA
                    arvoreDeLargura.append(idAresta)
            listaCores[verticeAtual] = Grafo.COR_PRETO

        
        return arvoreDeLargura
    
    def arvoreDeProfundidade(self):

        def buscaEmProfundidadeAux(verticeAtual):
            for idAresta, idVizinho, _ in self.__LA[verticeAtual].vizinhos:
                if listaCores[idVizinho] == Grafo.COR_BRANCO:
                    arvoreDeProfundidade.append(idAresta)
                    listaCores[idVizinho] = Grafo.COR_CINZA
                    buscaEmProfundidadeAux(idVizinho)
            listaCores[verticeAtual] = Grafo.COR_PRETO

        listaCores = [Grafo.COR_BRANCO] * self.__numVertices
        arvoreDeProfundidade = []
        
        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        listaCores[indexInicialBusca] = Grafo.COR_CINZA
        buscaEmProfundidadeAux(indexInicialBusca)

        return arvoreDeProfundidade
    
    def ordemTopologica(self):

        def adicionarOrdemExecucao(verticePreto):
            ordemExecucao.insert(0, verticePreto)

        ordemExecucao = []
        self.buscaEmProfundidade(callbackPreto = adicionarOrdemExecucao)
        return ordemExecucao
    
    def AGM(self):

        def atualizaHeap(indexVertice):
            adicionadoAGM[indexVertice] = True
            for idAresta, vizinho, pesoAresta in self.__LA[indexVertice].vizinhos:
                if not adicionadoAGM[vizinho]:
                    heapq.heappush(heapArestas, (pesoAresta, vizinho, idAresta))

        adicionadoAGM = [False for _ in range(self.__numVertices)]
        AGM = [] # id_arestas que pertencem à AGM
        heapArestas = []

        custo = 0

        atualizaHeap(0)

        while heapArestas:
            c, vertice, idAresta = heapq.heappop(heapArestas)
            if not adicionadoAGM[vertice]:
                AGM.append(idAresta)
                atualizaHeap(vertice)
                custo += c
        print(c)
        return AGM
    
