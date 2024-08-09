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
            1: None, # Verificar (Conexo)
            2: None, # Verificar (Bipartido)
            3: None, # Verificar (Euleriano)
            4: None, # Verificar (Possui ciclo)
            5: None, # Listar (Componentes conexas)
            6: None, # Listar (Componentes fortemente conexas)
            7: None, # Listar (Uma trilha Euleriana)
            8: None, # Listar ( Vértices de Articulacao)
            9: None, # Listar (Identificador das arestas ponte)
            10: self.__gerarArvoreProfundidade, # Gerar (Árvore de profundidade)
            11: self.__gerarArvoreLargura, # Gerar (Árvore de largura)
            12: None, # Gerar (Árvore geradora mínima)
            13: None, # Gerar (Ordem topológica)
            14: None, # Gerar (Valor do caminho mínimo entre dois vértices)
            15: None, # Gerar (Valor do fluxo máximo)
            16: None, # Gerar (Fecho transiƟvo)
        }
    
    def executarOperacao(self, idOperacao):
        try:
            operacao = self.__dictOperacoes[idOperacao]
            if operacao is not None:
                operacao()
        except KeyError:
            return # operacao invalida
    
    def __gerarArvoreLargura(self):
        arvoreDeLargura = self.__grafo.arvoreDeLargura()
        print(*arvoreDeLargura, sep = ' ')
    
    def __gerarArvoreProfundidade(self):
        arvoreProfundidade = self.__grafo.arvoreDeProfundidade()
        print(*arvoreProfundidade, sep = ' ')
