import sys
import numpy as np
from aigyminsper.search.search_algorithms import AEstrela
from aigyminsper.search.graph import State

class LabirintoCusto(State):

    def __init__(self, mapa, lin, col, op, move_cost=0):
        """
        Construtor do estado do labirinto.
        :param mapa: Matriz (numpy array) representando o labirinto e os custos.
        :param lin: Linha atual do agente.
        :param col: Coluna atual do agente.
        :param op: Operador (ação) que gerou este estado.
        :param move_cost: Custo do movimento para chegar a este estado.
        """
        super().__init__(op)
        self.mapa = mapa
        self.lin = lin
        self.col = col
        self.move_cost = move_cost
        self.lin_max = self.mapa.shape[0] - 1
        self.col_max = self.mapa.shape[1] - 1

    def successors(self):
        """
        Gera os estados sucessores a partir do estado atual.
        Verifica os quatro movimentos possíveis: cima, baixo, esquerda, direita.
        """
        successors = []
        
        # Cima
        if self.lin > 0:
            new_lin, new_col = self.lin - 1, self.col
            cost = self.mapa[new_lin][new_col]
            if cost > 0: # Verifica se não é uma parede
                successors.append(LabirintoCusto(self.mapa, new_lin, new_col, 'cima', cost))

        # Baixo
        if self.lin < self.lin_max:
            new_lin, new_col = self.lin + 1, self.col
            cost = self.mapa[new_lin][new_col]
            if cost > 0:
                successors.append(LabirintoCusto(self.mapa, new_lin, new_col, 'baixo', cost))

        # Esquerda
        if self.col > 0:
            new_lin, new_col = self.lin, self.col - 1
            cost = self.mapa[new_lin][new_col]
            if cost > 0:
                successors.append(LabirintoCusto(self.mapa, new_lin, new_col, 'esq', cost))

        # Direita
        if self.col < self.col_max:
            new_lin, new_col = self.lin, self.col + 1
            cost = self.mapa[new_lin][new_col]
            if cost > 0:
                successors.append(LabirintoCusto(self.mapa, new_lin, new_col, 'dir', cost))

        return successors

    def is_goal(self):
        """
        Verifica se o estado atual é um dos estados objetivo.
        Objetivos: célula 14 (1,1) e célula 18 (1,5).
        """
        return (self.lin == 1 and self.col == 1) or (self.lin == 1 and self.col == 5)

    def description(self):
        """Descrição do problema."""
        return "Agente para resolver um labirinto com custos variáveis."

    def cost(self):
        """Retorna o custo da ação que levou ao estado atual."""
        return self.move_cost

    def h(self):
        """
        Heurística para o algoritmo A*.
        Calcula a distância Manhattan até o objetivo mais próximo.
        Multiplica pelo menor custo de movimento possível (2) para ser admissível.
        """
        # Coordenadas dos objetivos
        goal1_lin, goal1_col = 1, 1  # Célula 14
        goal2_lin, goal2_col = 1, 5  # Célula 18

        # Distância Manhattan para cada objetivo
        dist1 = abs(self.lin - goal1_lin) + abs(self.col - goal1_col)
        dist2 = abs(self.lin - goal2_lin) + abs(self.col - goal2_col)

        # Retorna a menor distância multiplicada pelo custo mínimo de passo
        return min(dist1, dist2) * 2

    def env(self):
        """
        Representação textual do estado para poda na busca.
        A posição (linha, coluna) identifica unicamente um estado.
        """
        return f'({self.lin},{self.col})'


def load_map(file_path):
    """Carrega o mapa do arquivo de configuração."""
    return np.loadtxt(open(file_path, "rb"), delimiter=";")

def main(map_file, start_lin, start_col):
    """Função principal para executar a busca."""
    mapa = load_map(map_file)
    
    # Cria o estado inicial a partir dos argumentos da linha de comando
    # O custo para o estado inicial é 0 e não há operador de origem
    initial_state = LabirintoCusto(mapa, start_lin, start_col, '', 0)

    print("Iniciando busca pelo caminho de menor custo...")
    print(f"Estado Inicial: Célula na posição ({start_lin}, {start_col})")
    print(f"Objetivos: Célula 14 (1,1) ou Célula 18 (1,5)")
    print("-" * 30)

    # Utiliza o algoritmo AEstrela (A*), ideal para problemas com custo
    algorithm = AEstrela()
    result = algorithm.search(initial_state)

    if result:
        print("Solução encontrada!")
        print(f"Custo total do caminho: {result.g}")
        print("Sequência de ações:")
        print(result.show_path())
    else:
        print("Não foi possível encontrar uma solução.")

if __name__ == '__main__':
    # Verifica se os argumentos da linha de comando foram passados corretamente
    if len(sys.argv) != 4:
        print("Formato de execução: python LabirintoCusto.py <arquivo_configuracao> <linha_inicial> <coluna_inicial>")
        sys.exit(1)
        
    # Extrai os argumentos
    map_file_path = sys.argv[1]
    initial_lin = int(sys.argv[2])
    initial_col = int(sys.argv[3])
    
    main(map_file_path, initial_lin, initial_col)