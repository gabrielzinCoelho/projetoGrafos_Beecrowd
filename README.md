# Algoritmos em Grafos - versão Beecrowd

## Objetivo

Implementar um sistema modular para análise de propriedades de grafos.

A estrutura básica consistirá em um menu interativo onde o usuário poderá selecionar, via linha de comando, a propriedade do grafo que desejam analisar. 

## Funcões Implementadas

* Verificar se um grafo é conexo. 
    * Para o caso de grafos orientados, verificar conectividade fraca. 

* Verificar se um grafo não-orientado é bipartido. 

* Verificar se um grafo é Euleriano. 

* Verificar se um grafo possui ciclo. 

* Calcular a quantidade de componentes conexas em um grafo não-orientado. 

* Calcular a quantidade de componentes fortemente conexas em um grafo orientado. 

* Imprimir os vértices de articulação de um grafo não-orientado (priorizar a ordem lexicográfica dos vértices). 

* Calcular quantas arestas ponte possui um grafo não-orientado. 

* Imprimir a árvore em profundidade (priorizando a ordem lexicográfica dos vértices; 0 é a origem). 
    * Você deve imprimir o identificador das arestas. Caso o grafo seja desconexo, considere apenas a árvore com a raíz 0. 

* Árvore de largura (priorizando a ordem lexicográfica dos vértices; 0 é a origem).  
    * Você deve imprimir o identificador das arestas. Caso o grafo seja desconexo, considere apenas a árvore com a raíz 0.  

* Calcular o valor final de uma árvore geradora mínima (para grafos não-orientados).

* Imprimir a ordem os vértices em uma ordenação topológica. 
    * Esta função não fica disponível em grafos não direcionado. 
    * Deve-se priorizar a ordem lexicográfica dos vértices para a escolha de quais vértices explorar.

* Valor do caminho mínimo entre dois vértices (para grafos não-orientados com pelo menos um peso diferente nas arestas).  
    * 0 é a origem; n-1 é o destino. 

* Valor do fluxo máximo para grafos direcionados.  
    * 0 é a origem; n-1 é o destino. 

* Fecho transitivo para grafos direcionados. 
    * Deve-se priorizar a ordem lexicográfica dos vértices; 
    * 0 é o vértice escolhido.


