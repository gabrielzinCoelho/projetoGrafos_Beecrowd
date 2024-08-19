import heapq
import copy

from .Vertice import Vertice

class Grafo:

    # cores utilizadas para identificar vertices
    COR_BRANCO = 0 
    COR_CINZA = 1
    COR_PRETO = 2

    def __init__(self, *, numVertices, arestas = [], ehDirecionado) -> None:
        self.__numVertices = numVertices
        self.__numArestas = len(arestas)
        self.ehDirecionado = ehDirecionado
        self.__LA = [
            Vertice(vizinhos = {}) for _ in range(numVertices)
        ]

        # lista de incidencia, utilizada em algoritmos como kruskall
        self.__listaDeIncidencia = list(arestas)

        # ordenando arestas para priorizar ordem lexicográfica (padronizar saída beecrowd)

        if ehDirecionado: # ordenacao pelo vertice de chegada
            arestas.sort(
                key = lambda aresta : aresta[2]
            )
            adicionarAresta = self.__adicionarArestasD

        else: # ordenacao pelo vertice de chegada e desempate pelo vertice de saida (ambos vertices com vizinhos ordenados)
            arestas.sort(
                key = lambda aresta : (aresta[2], aresta[1]) 
            )
            adicionarAresta = self.__adicionarArestasND

        for aresta in arestas:
            adicionarAresta(*aresta)
    
    def __adicionarArestasD(self, idAresta, v1, v2, pesoAresta):

        self.__LA[v1].adicionarVizinho(idAresta = idAresta, idVizinho = v2, pesoAresta = pesoAresta)
    
    def __adicionarArestasND(self, idAresta, v1, v2, pesoAresta):

        self.__LA[v1].adicionarVizinho(idAresta = idAresta, idVizinho = v2, pesoAresta = pesoAresta)
        self.__LA[v2].adicionarVizinho(idAresta = idAresta, idVizinho = v1, pesoAresta = pesoAresta)
    
    # fins de depuracao
    def __str__(self):
        outputStr = ""
        for i, vertice in enumerate(self.__LA):
            outputStr += f"{i}) {str(vertice)}\n"
        return outputStr

    # metodo de classe que busca a primeira ocorrencia de um vertice nao explorado
    @staticmethod
    def __escolherVerticeInicial(listaCores):

        for indexVertice, corVertice in enumerate(listaCores):
            if corVertice == Grafo.COR_BRANCO:
                return indexVertice
        return None    

    # DFS com personalizacao por callbacks, retorna numero de componentesEncontradas para GND
    # callbackPreto -> invocada quando vizinhanca do vertice é totalmente explorada
    # callbackCinza -> quando um vertice cinza eh encontrado na busca (e nao eh o pai), util para deteccao de ciclos
    #                   se True eh retornado, a busca eh encerrada (algoritmos nao tolerantes a ciclos)
    def buscaEmProfundidade(self, callbackPreto = None, callbackCinza = None):

        encerrarBusca = False

        def buscaEmProfundidadeAux(verticeAtual):

            nonlocal encerrarBusca

            for idAresta, (idVizinho, _) in self.__LA[verticeAtual].vizinhos.items():
                if listaCores[idVizinho] == Grafo.COR_BRANCO:
                    listaCores[idVizinho] = Grafo.COR_CINZA
                    listaPais[idVizinho] = (idAresta, verticeAtual)
                    buscaEmProfundidadeAux(idVizinho)
                    
                # ciclo encontrado (callbackCinza)
                elif listaCores[idVizinho] == Grafo.COR_CINZA and idVizinho != listaPais[verticeAtual][1] and callbackCinza is not None:
                    encerrarBusca = callbackCinza()
                    if encerrarBusca:
                        return
                    
            # vertice explorado (callback preto)                    
            listaCores[verticeAtual] = Grafo.COR_PRETO
            if callbackPreto is not None:
                callbackPreto(verticeAtual)
    
        # lista de pais importante para evitar falso positivo de deteccao de ciclos
        listaPais = [(-1, -1)] * self.__numVertices # idAresta, pai
        listaCores = [Grafo.COR_BRANCO] * self.__numVertices
        numComponentes = 0

        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)

        while indexInicialBusca is not None:
            numComponentes += 1
            listaPais[indexInicialBusca] = (None, indexInicialBusca)
            listaCores[indexInicialBusca] = Grafo.COR_CINZA
            buscaEmProfundidadeAux(indexInicialBusca)

            if encerrarBusca:
                break
            else:
                indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        
        return numComponentes

    # todo grafo bipartido eh 2-colorivel
    def ehBipartido(self):

        NAO_COLORIDO = -1
        COR_A = 0
        COR_B = 1
        CORES = COR_B, COR_A

        def corOposta(cor):
            return CORES[cor]

        # BFS, se vertice adjacente nao foi colorido atribui a ele uma cor oposta
        # caso contrario, verifica se a cor condiz com a propriedade de um grafo bipartido
        def bfsColorida(origem):
            
            filaVertices = [origem]

            while filaVertices:
                verticeAtual = filaVertices.pop(0)
                corVizinho = corOposta(listaCores[verticeAtual])
                for vizinho, _ in self.__LA[verticeAtual].vizinhos.values():

                    if listaCores[vizinho] == NAO_COLORIDO:
                        filaVertices.append(vizinho)
                        listaCores[vizinho] = corVizinho

                    elif listaCores[vizinho] == listaCores[verticeAtual]:
                        return False
            return True

        listaCores = [NAO_COLORIDO] * self.__numVertices

        for indexVertice in range(self.__numVertices): 
            if listaCores[indexVertice] == NAO_COLORIDO:
                if not bfsColorida(indexVertice):
                    return 0
        return 1


    # verifica conectividade, fraca para GD
    def ehConexo(self):

        # BFS padrao, contagem de vertices encontrados para determinar conectividade
        def verticesEncontradosBfs(grafo):

            listaCores = [Grafo.COR_BRANCO] * grafo.__numVertices
        
            filaVisita = [0]
            listaCores[0] = Grafo.COR_CINZA

            verticesEncontrados = 1

            while filaVisita:
                verticeAtual = filaVisita.pop(0)

                for idVizinho, _ in grafo.__LA[verticeAtual].vizinhos.values():
                    if listaCores[idVizinho] == Grafo.COR_BRANCO:
                        filaVisita.append(idVizinho)
                        listaCores[idVizinho] = Grafo.COR_CINZA
                        verticesEncontrados += 1
            return verticesEncontrados

        def criarGrafoNaoDirecionado():
            grafoNaoDirecionado = copy.deepcopy(self)

            for i, vertice in enumerate(self.__LA):
                    for idAresta, (idVizinho, _) in vertice.vizinhos.items():
                        grafoNaoDirecionado.__LA[idVizinho].vizinhos[idAresta] = (i, 0)
                
            return grafoNaoDirecionado

        # para GND, a busca eh feita no proprio grafo
        # para GD, a busca eh feita no grafo temporario resultante da remocao do sentido das arestas
        grafoBusca = self if not self.ehDirecionado else criarGrafoNaoDirecionado()

        return int((verticesEncontradosBfs(grafoBusca) == self.__numVertices))
    
    def possuiCiclo(self):

        # callback invocada quando um vertice cinza eh encontrado na DFS, com efeito colateral para informar disparo da mesma
        def callbackCiclo():
            nonlocal cicloEncontrado
            cicloEncontrado = True
            return True # encerrar busca

        cicloEncontrado = False

        self.buscaEmProfundidade(callbackCinza = callbackCiclo)
        return int(cicloEncontrado)
    
    def ehEuleriano(self): 

        def verticeGrauImparND():
            for vertice in self.__LA:
                if len(vertice.vizinhos) % 2:
                    return True
            return False

        def grauBalanceadoD():
            grauEntrada = [0] * self.__numVertices
            grauSaida = grauEntrada.copy()

            for i, vertice in enumerate(self.__LA):
                grauSaida[i] = len(vertice.vizinhos)
                for idVizinho, _ in vertice.vizinhos.values():
                    grauEntrada[idVizinho] += 1
            
            return grauEntrada == grauSaida

        # verifica conectividade, todo grafo euleriano deve ser conexo
        if not self.ehConexo():
            return 0

        # todos vertices com grau par, para GND
        if not self.ehDirecionado:
            return int(verticeGrauImparND() == False)
        
        # pseudossimetrico, para GD
        return int(grauBalanceadoD())
    
    def componentesConexas(self):
        # disponivel apenas para GND
        # o n° de componentes eh definido pela quantidade de vezes que a busca teve de ser reiniciada
        numComponentes = self.buscaEmProfundidade()
        return numComponentes

    def componentesFortementeConexas(self):
        # disponivel apenas para GD
        # DFS feita marcando tempo de saida (callback preto = marcarTempo)
        # arestas de arvore no grafo transposto identificam componentes

        def dfsComponentes():
            
            # vertices escolhidos em ordem decrescente de tempo de saida
            def escolherVerticeIncial():
                for indexVertice in ordemSaida:
                    if listaCores[indexVertice] == Grafo.COR_BRANCO:
                        return indexVertice
                return None    

            # DFS comum
            def buscaEmProfundidadeAux(verticeAtual):

                for idVizinho, _ in grafoTransposto.__LA[verticeAtual].vizinhos.values():
                    if listaCores[idVizinho] == Grafo.COR_BRANCO:
                        listaCores[idVizinho] = Grafo.COR_CINZA
                        buscaEmProfundidadeAux(idVizinho)                   

            numComponentes = 0
            listaCores = [Grafo.COR_BRANCO] * grafoTransposto.__numVertices
            indexInicialBusca = escolherVerticeIncial()

            # cada vez que a DFS eh reiniciada uma CFC eh detectada
            while indexInicialBusca is not None:
                numComponentes += 1
                listaCores[indexInicialBusca] = Grafo.COR_CINZA
                buscaEmProfundidadeAux(indexInicialBusca)
                indexInicialBusca = escolherVerticeIncial()

            return numComponentes

        def marcarTempo(indexVertice):
            ordemSaida.insert(0, indexVertice) # vertices inseridos em ordem decrescente de tempo de saida

        # G^t
        def criarGrafoTransposto():
            grafoTransposto = Grafo(numVertices = self.__numVertices, ehDirecionado = self.ehDirecionado)
            grafoTransposto.__numArestas = self.__numArestas

            # invertendo sentido das arestas
            for i, vertice in enumerate(self.__LA):
                    for idAresta, (idVizinho, pesoAresta) in vertice.vizinhos.items():
                        grafoTransposto.__LA[idVizinho].vizinhos[idAresta] = (i, pesoAresta)
                
            return grafoTransposto

        ordemSaida = []
        grafoTransposto = criarGrafoTransposto()
        self.buscaEmProfundidade(callbackPreto = marcarTempo)
        numComponentes = dfsComponentes()
        return numComponentes

    # BFS, adiciona vertices a lista que representa a arvore de busca resultante
    def arvoreDeLargura(self):

        listaCores = [Grafo.COR_BRANCO] * self.__numVertices
        arvoreDeLargura = []
        
        indexInicialBusca = Grafo.__escolherVerticeInicial(listaCores)
        filaVisita = [indexInicialBusca]
        listaCores[indexInicialBusca] = Grafo.COR_CINZA
    
        while filaVisita:
            verticeAtual = filaVisita.pop(0)

            for idAresta, (idVizinho, _) in self.__LA[verticeAtual].vizinhos.items():
                if listaCores[idVizinho] == Grafo.COR_BRANCO:
                    filaVisita.append(idVizinho)
                    listaCores[idVizinho] = Grafo.COR_CINZA
                    arvoreDeLargura.append(idAresta)
            listaCores[verticeAtual] = Grafo.COR_PRETO

        
        return arvoreDeLargura
    
    # DFS, adiciona vertices a lista que representa a arvore de busca resultante
    def arvoreDeProfundidade(self):

        def buscaEmProfundidadeAux(verticeAtual):
            for idAresta, (idVizinho, _) in self.__LA[verticeAtual].vizinhos.items():
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
    
    # DFS-based
    # quando um vertice se torna preto (nao possui dependentes nao explorados) eh add na pilha de execucao
    def ordemTopologica(self):

        # pilha de execucao, callbackPreto
        def adicionarOrdemExecucao(verticePreto):
            ordemExecucao.insert(0, verticePreto)
        
        # deteccao de ciclos, callbackCinza
        def callbackCiclo():
            nonlocal cicloEncontrado
            cicloEncontrado = True
            return True # encerrar busca

        cicloEncontrado = False
        ordemExecucao = []
        self.buscaEmProfundidade(callbackPreto = adicionarOrdemExecucao, callbackCinza = callbackCiclo)

        if cicloEncontrado:
            return [-1]
        
        return ordemExecucao
    
    # desenvolvido, mas nn utilizado
    def prim(self):

        # min heap de prioridades (arestas leves)
        def atualizaHeap(indexVertice):
            adicionadoAGM[indexVertice] = True
            for idAresta, (vizinho, pesoAresta) in self.__LA[indexVertice].vizinhos.items():
                if not adicionadoAGM[vizinho]:
                    heapq.heappush(heapArestas, (pesoAresta, vizinho, idAresta))

        # vertices explorados ou nao
        adicionadoAGM = [False for _ in range(self.__numVertices)]
        heapArestas = []

        custo = 0

        # inicializa a heap com os vizinhos da origem
        atualizaHeap(0)

        while heapArestas:
            # remove vertice com menor custo associado e verifica se eh uma aresta segura
            c, vertice, _ = heapq.heappop(heapArestas)
            if not adicionadoAGM[vertice]:
                atualizaHeap(vertice)
                custo += c
        return c
    

    def kruskall(self):

        # floresta de rotulos
        class UFDS:
            def __init__(self, numVertices):
                self.__rank = [0] * numVertices # altura da arvore
                self.__pai = [i for i in range(numVertices)]

            def buscaPai(self, indexVertice):
                
                verticeAtual = indexVertice
                verticesComponente = [] # vertices encontrados na busca pelo rotulo da arvore

                #rotulo da componente alcancado
                while self.__pai[verticeAtual] != verticeAtual:
                    verticeAtual = self.__pai[verticeAtual]
                    verticesComponente.append(verticeAtual)
                
                # compressao da arvore, otimizar futuras buscas
                for v in verticesComponente:    
                    self.__pai[v] = verticeAtual

                # rotulo da componente
                return verticeAtual
            
            def mesmaComponente(self, v1, v2):
                return self.buscaPai(v1) == self.buscaPai(v2)
            
            def unificaComponente(self, v1, v2):
                
                pai_v1 = self.buscaPai(v1)
                pai_v2 = self.buscaPai(v2)

                # uniao arvores de mesma altura, incrementa altura arvore resultante em 1
                if self.__rank[pai_v1] == self.__rank[pai_v2]:
                    self.__pai[pai_v2] = pai_v1
                    self.__rank[pai_v1] += 1
                
                # arvore "menor" se torna sub arvore (arvore mais achatada otimiza busca)
                else:
                    menorArvore, maiorArvore = (pai_v1, pai_v2) if self.__rank[pai_v1] < self.__rank[pai_v2] else (pai_v2, pai_v1)
                    self.__pai[menorArvore] = maiorArvore

        ufds = UFDS(self.__numVertices)
        arestas = sorted(self.__listaDeIncidencia, key = lambda aresta : aresta[3]) # ordena arestas pelo peso
        custoAGM = 0
        
        # adicao de arestas leves e seguras
        # limite de arestas = n - k, k eh o numero de componentes conexas
        # considerando melhor otimizacao, apenas descarta arestas excedentes
        for _, v1, v2, pesoAresta in arestas:
            if not ufds.mesmaComponente(v1, v2):
                ufds.unificaComponente(v1, v2)
                custoAGM += pesoAresta

        return custoAGM

    # deteccao de vertices e arestas pelo low de um vertice e numero de filhos da raiz
    def tarjan(self):

        # verifica vertice nao explorado
        def naoVisitado(indexVertice):
            return tempoDescoberta[indexVertice] == NAO_VISITADO

        # se chamada a partir da raiz da DFS, numero de filhos eh contado para determinar se raiz eh articulacao
        # caso contrario, verificacao é feita pelo low
        def tarjanAux(*, indexVertice, ehRaiz = False):
            
            # variaveis compartilhadas entre as execucoes, escopo da funcao externa
            nonlocal numFilhosRaiz, tempoAtual

            vertice = self.__LA[indexVertice]
            tempoDescoberta[indexVertice] = low[indexVertice] = tempoAtual
            
            # tempo de descoberta incrementado para cara vertice descoberto
            tempoAtual += 1

            for idAresta, (idVizinho, _) in vertice.vizinhos.items():

                # vizinho nao visitado, aresta de arvore
                if naoVisitado(idVizinho):

                    pai[idVizinho] = indexVertice

                    tarjanAux(indexVertice = idVizinho)
                    low[indexVertice] = min(low[indexVertice], low[idVizinho])
                    
                    # caso 1 articulacao: vertice raiz da arvore de busca
                    if ehRaiz:
                        numFilhosRaiz += 1
                    # caso 2 articulacao: vertice nn eh raiz da arvore 
                    elif low[idVizinho] >= tempoDescoberta[indexVertice]:
                        articulacoes.add(indexVertice)

                    # deteccao de ponte
                    if low[idVizinho] > tempoDescoberta[indexVertice]:
                        pontes.add(idAresta)

                # vizinho ja visitado, aresta de retorno ou cruzamento
                elif pai[indexVertice] != idVizinho:
                    low[indexVertice] = min(low[indexVertice], tempoDescoberta[idVizinho])

        NAO_VISITADO = -1

        # set, para evitar vertices duplicados
        articulacoes = set()
        pontes = set()

        tempoDescoberta = [NAO_VISITADO] * self.__numVertices
        low = [NAO_VISITADO] * self.__numVertices
        pai = [NAO_VISITADO] * self.__numVertices
        tempoAtual = 0

        # tarjan eh aplicado para cada componente conexa
        for i in range(self.__numVertices):
            if naoVisitado(i):
                numFilhosRaiz = 0
                tarjanAux(indexVertice = i, ehRaiz = True)
                if numFilhosRaiz > 1:
                    articulacoes.add(i)

        return articulacoes, pontes
    

    # utilizado para definir circuito/trilha euleriana
    def fleury(self, *, verticeInicial = 0):

        # verifica se a aresta obedece a regra da ponte
        def arestaValida(idAresta):

            nonlocal pontes
            
            if pontes is None:
                # primeira aresta sendo verificada

                numArestasDisponiveis = 0
                ehArestaUnica = True

                # na segunda aresta valida encontrada, ehArestaUnica eh False
                for vIdAresta in verticeAtual.vizinhos.keys():
                    if arestasNaoExploradas[vIdAresta]:
                        if numArestasDisponiveis == 0:
                            numArestasDisponiveis = 1
                        else:
                            ehArestaUnica = False
                            break
                
                # toda aresta unica eh ponte
                if ehArestaUnica:
                    return True
                
                # atualiza as arestas pontes do grafo atual
                _, pontes = self.tarjan()
            
            # pontes ja foram calculadas e aresta nao e unica
            # True se aresta nao eh ponte, False se aresta eh ponte
            return not (idAresta in pontes)

        NAO_EXPLORADO = True
        numArestasRestantes = self.__numArestas
        arestasNaoExploradas = [NAO_EXPLORADO] * self.__numArestas
        circuito = [verticeInicial]

        while numArestasRestantes:
            
            # utiliza arestas do ultimo vertice adicionado no circuito
            # pontes sao calculadas a cada adicao de aresta
            # (arestas nao pontes tendem a se tornar pontes a medida que as demais sao marcadas como exploradas)
            verticeAtual = self.__LA[circuito[-1]]
            pontes = None

            for idAresta, (idVizinho, _) in verticeAtual.vizinhos.items():
                if arestasNaoExploradas[idAresta] and arestaValida(idAresta):

                    arestasNaoExploradas[idAresta] = False                    
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
            
            # verifica se ha exatamente dois vertices com grau impar e seleciona vertice impar origem da trilha
            # fleury eh chamado utilizando vertice impar como origem

            trilhaEuleriana = self.fleury(verticeInicial = verticeImparInicial)
            return trilhaEuleriana

        # direcionado
        else:
            NotImplementedError()
    
    def fordFulkerson(self):

        PAI_NULO = (-1, -1)

        # grafoResidual eh copia do grafo original, com adicao de arestas antiparalelas com capacidade 0, inicialmente
        # necessario para solucao otima
        def criarGrafoResidual():
            grafoResidual = copy.deepcopy(self)

            for i, vertice in enumerate(self.__LA):
                    for idAresta, (idVizinho, _) in vertice.vizinhos.items():
                        grafoResidual.__LA[idVizinho].vizinhos[idAresta] = (i, 0) # (u, v) -> (v, u) + capacidade 0

            return grafoResidual

        # BFS, iniciando na origem e interrompida quando destino eh alcançado
        def buscaCaminhoAumentante():

            arestasPai = [PAI_NULO] * grafoResidual.__numVertices # idAresta, pai
            listaCores = [Grafo.COR_BRANCO] * grafoResidual.__numVertices
                
            filaVisita = [verticeOrigem]
            listaCores[verticeOrigem] = Grafo.COR_CINZA

            destinoAlcancado = False

            while filaVisita and not destinoAlcancado:
                verticeAtual = filaVisita.pop(0)

                for idAresta, (idVizinho, capacidadeAresta) in grafoResidual.__LA[verticeAtual].vizinhos.items():
                    if listaCores[idVizinho] == Grafo.COR_BRANCO and capacidadeAresta > 0:
                        filaVisita.append(idVizinho)
                        listaCores[idVizinho] = Grafo.COR_CINZA
                        arestasPai[idVizinho] = (idAresta, verticeAtual)

                        # primeiro vertice a encontrar o destino encerra a busca
                        if idVizinho == verticeDestino:
                            destinoAlcancado = True
                            break

            return arestasPai
        
        def atualizaFluxoRede():

            def atualizaCapacidade(v1, v2, idArestaFluxo, fluxoAresta):
                capacidadeAntiga = grafoResidual.__LA[v1].vizinhos[idArestaFluxo][1]
                grafoResidual.__LA[v1].vizinhos[idArestaFluxo] = (v2, capacidadeAntiga + fluxoAresta)
            
            arestasPai = buscaCaminhoAumentante()    

            # destino nao alcancado, nao ha caminho aumentante
            if arestasPai[verticeDestino] == PAI_NULO:
                return 0
            
            INFINITO = 1000000000
            verticeAtual = verticeDestino
            fluxoAtual = INFINITO

            caminhoAumentante = [] # u, v, idAresta (u, v)

            # versao iterativa do mapeamento do caminho aumentante, lista auxiliar caminhoAumentante
            while verticeAtual != verticeOrigem:
                idArestaPai, pai = arestasPai[verticeAtual]
                capacidadeAresta = grafoResidual.__LA[pai].vizinhos[idArestaPai][1]

                # a cada aresta do caminho aumentante, fluxo é limitado pelo menor valor encontrado
                fluxoAtual = min(fluxoAtual, capacidadeAresta)
                caminhoAumentante.append((pai, verticeAtual, idArestaPai))

                verticeAtual = pai

            # agora, com o fluxo calculado, as capacidades das arestas pertencentes ao caminho aumentante sao atualizadas
            # atualizando valores de capacidade para conservar fluxo
            for u, v, idAresta in caminhoAumentante:
                atualizaCapacidade(u, v, idAresta, -fluxoAtual) # menos fluxo (capacidade) na ida
                atualizaCapacidade(v, u, idAresta, fluxoAtual) # mais fluxo (capacidade) na volta
            
            return fluxoAtual

        verticeOrigem = 0
        verticeDestino = self.__numVertices - 1
        fluxoMaximo = 0
        grafoResidual = criarGrafoResidual()

        fluxoEncerrado = False

        # grafo Residual eh criado, enquanto houver fluxo escoado, caminho aumentante eh buscado 

        while not fluxoEncerrado:
            fluxo = atualizaFluxoRede()
            if fluxo <= 0:
                fluxoEncerrado = True
            else:
                fluxoMaximo += fluxo
        return fluxoMaximo
        

    def dijkstra(self):

        INDEFINIDO = 1000000000000

        # verifica se u reduz a estimativa de v, por meio da aresta (u, v)
        # retorna true, em caso afirmativo (determina se instancia de v com custo em questao deve ser add ou descartado)
        def relaxar(u, v, pesoAresta):
            novaEstimativa = listaDistancias[u] + pesoAresta
            if listaDistancias[v] > novaEstimativa:
                listaDistancias[v] = novaEstimativa
                return True
            return False
        
        origem = 0
        destino = self.__numVertices - 1

        explorado = [False] * self.__numVertices
        listaDistancias = [INDEFINIDO] * self.__numVertices
        
        # min heap de prioridade
        heap = [(0, origem)] # estimativa atual e vertice associado
        listaDistancias[origem] = 0

        while heap:

            # remove da fila vertice com menor estimativa (se nao explorado, faz parte da solucao otima)
            _, menorEstimativa = heapq.heappop(heap)

            if not explorado[menorEstimativa]:

                # caminho minimo para destino calculado, fim do algoritmo
                if menorEstimativa == destino:
                    return listaDistancias[menorEstimativa]

                explorado[menorEstimativa] = True

                # cada vertice explorado tenta relaxar os vizinhos
                for vizinho, pesoAresta in self.__LA[menorEstimativa].vizinhos.values():

                    # se estimativa melhora, nova instancia do vertice eh adicionada
                    # as eventuais estimativas calculadas anteriores posteriormente serao descartadas
                    if relaxar(menorEstimativa, vizinho, pesoAresta):
                        heapq.heappush(heap, (listaDistancias[vizinho], vizinho))


    # fecho transitivo utilizando DFS (padronizar gabarito e saida esperada)
    def fechoTransitivo(self):
        
        #DFS comum, adiona vertices na lista do fecho na ordem em que sao descobertos
        def buscaEmProfundidadeAux(verticeAtual):

            for idVizinho, _ in self.__LA[verticeAtual].vizinhos.values():
                if listaCores[idVizinho] == Grafo.COR_BRANCO:
                    fechoOrigem.append(idVizinho)
                    listaCores[idVizinho] = Grafo.COR_CINZA
                    buscaEmProfundidadeAux(idVizinho)                   

        listaCores = [Grafo.COR_BRANCO] * self.__numVertices
        fechoOrigem = []
        listaCores[0] = Grafo.COR_CINZA
        buscaEmProfundidadeAux(0)

        return fechoOrigem