class Utilitarios:

    @staticmethod
    def lerListaInteiros(*, numEntradas, valorPadrao = 0):
        entradas = [int(x) for x in input().strip().split()]
        if numEntradas <= len(entradas):
            return entradas[:numEntradas + 1]
        
        entradasRestantes = (numEntradas - len(entradas)) * [valorPadrao]
        return entradas + entradasRestantes
    
    def lerListaInteiros():
        entradas = [int(x) for x in input().strip().split()]
        return entradas
        