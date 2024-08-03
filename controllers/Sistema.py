from Utilitarios import Utilitarios
from .InterfaceGrafo import InterfaceGrafo

class Sistema:
    
    def __init__(self) -> None:
        self.__operacoes = None
        self.__interfaceGrafo = None

    def iniciar(self):
        self.__lerEntradas()
        self.__executarOperacoes()
    
    def __lerEntradas(self):
        self.__lerOperacoes()
        self.__interfaceGrafo = InterfaceGrafo()

    def __lerOperacoes(self):
        self.__operacoes = Utilitarios.lerListaInteiros()
    
    def __executarOperacoes(self):
        for idOperacao in self.__operacoes:
            self.__interfaceGrafo.executarOperacao(idOperacao)
    
    
    