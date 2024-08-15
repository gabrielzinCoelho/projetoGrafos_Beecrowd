from Utilitarios import Utilitarios
from models import Grafo

class InterfaceGrafo:

    def __init__(self) -> None:
        self.__lerGrafo()
        self.__defineOperacoes()

    def __lerGrafo(self):
        numVertices, numArestas = Utilitarios.lerListaInteiros()
        ehDirecionado = True if input().strip() == "direcionado" else False
        arestas = []

        for _ in range(numArestas):
            arestas.append(
                tuple(Utilitarios.lerListaInteiros()) # id_aresta, vértice_u, vértice_v, peso_da_aresta 
            )
        
        self.__grafo = Grafo(numVertices = numVertices, arestas = arestas, ehDirecionado = ehDirecionado)
    
    def __defineOperacoes(self):
        self.__dictOperacoes = {
            0: self.__verificarEhConexo, # Verificar (Conexo)
            1: lambda : print('x'), # Verificar (Bipartido)
            2: self.__verificarEhEuleriano, # Verificar (Euleriano)
            3: self.__verificarCiclo, # Verificar (Possui ciclo)
            4: self.__listarCConexas, # Listar (Componentes conexas)
            5: self.__listarCFConexas, # Listar (Componentes fortemente conexas)
            6: self.__listarArticulacoes, # Listar ( Vértices de Articulacao)
            7: self.__listarPontes, # Listar (Identificador das arestas ponte)
            8: self.__gerarArvoreProfundidade, # Gerar (Árvore de profundidade)
            9: self.__gerarArvoreLargura, # Gerar (Árvore de largura)
            10: self.__arvoreGeradoraMinima, # Gerar (Árvore geradora mínima)
            11: self.__ordemTopologica, # Gerar (Ordem topológica)
            12: lambda : print('x'), # Gerar (Valor do caminho mínimo entre dois vértices)
            13: self.__gerarFluxoMaximo, # Gerar (Valor do fluxo máximo)
            14: lambda : print('x'), # Gerar (Fecho transitivo)
            15: self.__listarTrilhaEuleriana, # Listar (Uma trilha Euleriana)
        }
    
    def executarOperacao(self, idOperacao):
        try:
            operacao = self.__dictOperacoes[idOperacao]
            if operacao is not None:
                operacao()
        except KeyError:
            return # operacao invalida
    
    def __verificarEhConexo(self):
        ehConexo = self.__grafo.ehConexo()
        print(ehConexo)
    
    def __verificarCiclo(self):
        possuiCiclo = self.__grafo.possuiCiclo()
        print(possuiCiclo)
    
    def __verificarEhEuleriano(self):
        ehEuleriano = self.__grafo.ehEuleriano()
        print(ehEuleriano)
    
    def __listarCConexas(self):
        if self.__grafo.ehDirecionado:
            print(-1)
        else:
            print(self.__grafo.componentesConexas())

    def __listarCFConexas(self):
        if not self.__grafo.ehDirecionado:
            print(-1)
        else:
            print(self.__grafo.componentesFortementeConexas())

    def __gerarArvoreLargura(self):
        arvoreDeLargura = self.__grafo.arvoreDeLargura()
        print(*arvoreDeLargura, sep = ' ')
    
    def __gerarArvoreProfundidade(self):
        arvoreProfundidade = self.__grafo.arvoreDeProfundidade()
        print(*arvoreProfundidade, sep = ' ')
    
    def __ordemTopologica(self):
        if not self.__grafo.ehDirecionado:
            print(-1)
        else:
            ordemExecucao = self.__grafo.ordemTopologica()
            print(*ordemExecucao, sep = ' ')

    def __arvoreGeradoraMinima(self):
        if self.__grafo.ehDirecionado:
            print(-1)
        else:
            custoAGM = self.__grafo.AGM()
            print(custoAGM)

    def __listarArticulacoes(self):
        if self.__grafo.ehDirecionado:
            print(-1)
        else:
            articulacoes, _ = self.__grafo.tarjan()
            if articulacoes:
                articulacoesOrdenadas = sorted(articulacoes)
                print(*articulacoesOrdenadas, sep = ' ')
            else:
                print(-1)
    
    def __listarPontes(self):
        if self.__grafo.ehDirecionado:
            print(-1)
        else:
            _, pontes = self.__grafo.tarjan()
            numPontes = len(pontes)
            print(numPontes)
    
    def __listarTrilhaEuleriana(self):
        trilhaEuleriana = self.__grafo.trilhaEuleriana()
        print(*trilhaEuleriana, sep = ' ')
    
    def __gerarFluxoMaximo(self):
        fluxoMaximo = self.__grafo.fordFulkerson()
        print(fluxoMaximo)