import heapq

from .Vertice import Vertice

class Grafo:

    COR_BRANCO = 0
    COR_CINZA = 1
    COR_PRETO = 2

    def __init__(self, *, numVertices, arestas = [], ehDirecionado) -> None:
        self.__numVertices = numVertices
        self.__numArestas = len(arestas)
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
        return AGM
    

    def tarjan(self):

        def naoVisitado(indexVertice):
            return tempoDescoberta[indexVertice] == NAO_VISITADO

        def tarjanAux(*, indexVertice, ehRaiz = False):
            
            nonlocal numFilhosRaiz, tempoAtual

            vertice = self.__LA[indexVertice]
            tempoDescoberta[indexVertice] = low[indexVertice] = tempoAtual
            tempoAtual += 1

            for idAresta, idVizinho, _ in vertice.vizinhos:
                if naoVisitado(idVizinho):

                    pai[idVizinho] = indexVertice

                    tarjanAux(indexVertice = idVizinho)
                    low[indexVertice] = min(low[indexVertice], low[idVizinho])

                    if ehRaiz:
                        numFilhosRaiz += 1
                    elif low[idVizinho] >= tempoDescoberta[indexVertice]:
                        articulacoes.add(indexVertice)

                    if low[idVizinho] > tempoDescoberta[indexVertice]:
                        pontes.add(idAresta)

                elif pai[indexVertice] != idVizinho:
                    low[indexVertice] = min(low[indexVertice], tempoDescoberta[idVizinho])

        NAO_VISITADO = -1

        articulacoes = set()
        pontes = set()

        tempoDescoberta = [NAO_VISITADO] * self.__numVertices
        low = [NAO_VISITADO] * self.__numVertices
        pai = [NAO_VISITADO] * self.__numVertices
        tempoAtual = 0

        for i in range(self.__numVertices):
            if naoVisitado(i):
                numFilhosRaiz = 0
                tarjanAux(indexVertice = i, ehRaiz = True)
                if numFilhosRaiz > 1:
                    articulacoes.add(i)

        return articulacoes, pontes
    

    def fleury(self, *, verticeInicial = 0):

        def arestaValida(idAresta):

            nonlocal pontes
            
            if pontes is None:
                # primeira aresta sendo verificada

                numArestasDisponiveis = 0
                ehArestaUnica = True

                for vIdAresta, _, _ in verticeAtual.vizinhos:
                    if arestasNaoExploradas[vIdAresta]:
                        if numArestasDisponiveis == 0:
                            numArestasDisponiveis = 1
                        else:
                            ehArestaUnica = False
                            break
                
                if ehArestaUnica:
                    return True
                

                _, pontes = self.tarjan()
            
            # pontes ja foram calculadas e aresta nao e unica
            # True se aresta nao eh ponte, False se aresta eh ponte
            return not (idAresta in pontes)

        NAO_EXPLORADO = True
        numArestasRestantes = self.__numArestas
        arestasNaoExploradas = [NAO_EXPLORADO] * self.__numArestas
        circuito = [verticeInicial]

        while numArestasRestantes:

            verticeAtual = self.__LA[circuito[-1]]
            pontes = None

            for idAresta, idVizinho, _ in verticeAtual.vizinhos:
                if arestasNaoExploradas[idAresta] and arestaValida(idAresta):

                    arestasNaoExploradas[idAresta] = False
                    for vIdAresta, vIdVizinho, _ in self.__LA[idVizinho].vizinhos: # dict ou referencia cruzada -> acesso O(1)
                        if vIdVizinho == circuito[-1]:
                            arestasNaoExploradas[vIdAresta] = False
                            break
                    
                    circuito.append(idVizinho)
                    numArestasRestantes -= 1
                    break
        
        return circuito
    
    def trilhaEuleriana(self):
        
        # nao_direcionado
        if not self.ehDirecionado:

            numVerticesImpares = 0
            verticeImparInicial = None

            for indexVertice, vertice in enumerate(self.__LA):
                if len(vertice.vizinhos) % 2:
                    numVerticesImpares += 1
                    if verticeImparInicial is None:
                        verticeImparInicial = indexVertice
            
            if numVerticesImpares != 2:
                return None
            
            trilhaEuleriana = self.fleury(verticeInicial = verticeImparInicial)
            return trilhaEuleriana

        # direcionado
        else:
            NotImplementedError()

