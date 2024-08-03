class Utilitarios:

    @staticmethod
    def lerListaInteiros(*, numEntradas = None, valorPadrao = 0):
        entradas = [int(x) for x in input().strip().split()]
        if numEntradas is None:
            return entradas
        if numEntradas <= len(entradas):
            return entradas[:numEntradas + 1]
        
        entradasRestantes = (numEntradas - len(entradas)) * [valorPadrao]
        return entradas + entradasRestantes
        