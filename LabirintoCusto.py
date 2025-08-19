import sys
import numpy as np
from aigyminsper.search.search_algorithms import BuscaLargura, BuscaProfundidade, BuscaCustoUniforme, AEstrela
from aigyminsper.search.graph import State

class LabirintoCusto(State):

    def __init__(self, mapa, lin, col, op, move_cost=0):
        super().__init__(op)
        self.mapa = mapa
        self.lin = lin
        self.col = col
        self.move_cost = move_cost
        self.lin_max = self.mapa.shape[0] - 1
        self.col_max = self.mapa.shape[1] - 1

    def successors(self):
        successors = []
        moves = {'cima': (-1, 0), 'baixo': (1, 0), 'esq': (0, -1), 'dir': (0, 1)}

        for move_name, (d_lin, d_col) in moves.items():
            new_lin, new_col = self.lin + d_lin, self.col + d_col

            if 0 <= new_lin <= self.lin_max and 0 <= new_col <= self.col_max:
                cell_value = self.mapa[new_lin][new_col]
                
                if cell_value > 0:
                    cost = 4 if cell_value == 18 else 2
                    successors.append(LabirintoCusto(self.mapa, new_lin, new_col, move_name, cost))
        return successors

    def is_goal(self):
        cell_value = self.mapa[self.lin][self.col]
        return cell_value == 14 or cell_value == 18

    def description(self):
        return "Agente para resolver um labirinto com custos variáveis usando múltiplos algoritmos."

    def cost(self):
        return self.move_cost

    def h(self):
        goals_pos = np.where((self.mapa == 14) | (self.mapa == 18))
        min_dist = float('inf')
        for g_lin, g_col in zip(goals_pos[0], goals_pos[1]):
            dist = abs(self.lin - g_lin) + abs(self.col - g_col)
            if dist < min_dist:
                min_dist = dist
        return min_dist * 2

    def env(self):
        return f'({self.lin},{self.col})'

def load_map(file_path):
    return np.loadtxt(open(file_path, "rb"), delimiter=";", dtype=int)

def main(map_file, start_lin, start_col, algorithm_name):
    mapa = load_map(map_file)
    initial_state = LabirintoCusto(mapa, start_lin, start_col, '', 0)

    algorithm = None
    if algorithm_name.lower() == 'bfs':
        algorithm = BuscaLargura()
    elif algorithm_name.lower() == 'dfs':
        # Revertendo: O construtor não aceita argumentos.
        algorithm = BuscaProfundidade()
    elif algorithm_name.lower() == 'ucs':
        algorithm = BuscaCustoUniforme()
    elif algorithm_name.lower() == 'astar':
        algorithm = AEstrela()
    else:
        print(f"Erro: Algoritmo '{algorithm_name}' não reconhecido.")
        print("Opções válidas: bfs, dfs, ucs, astar")
        return

    print("-" * 30)
    print(f"Executando busca com o algoritmo: {algorithm_name.upper()}")
    print(f"Estado Inicial: Célula {mapa[start_lin][start_col]} na posição ({start_lin}, {start_col})")
    
    # CORREÇÃO: Tratando o caso especial do DFS na chamada do search.
    result = None
    if algorithm_name.lower() == 'dfs':
        # O parâmetro de profundidade 'm' é passado aqui.
        result = algorithm.search(initial_state, m=30)
    else:
        result = algorithm.search(initial_state)

    if result:
        print("\nSolução Encontrada!")
        goal_state = result.state
        goal_cell_value = mapa[goal_state.lin][goal_state.col]
        print(f"Objetivo Atingido: Célula {goal_cell_value} na posição ({goal_state.lin}, {goal_state.col})")
        print(f"Custo total do caminho: {result.g}")
        
        actions_string = result.show_path()
        num_steps = len(actions_string.split(';')) - 1
        print(f"Número de passos: {num_steps}")
        
        print("\n--- Sequência de Ações ---")
        print(actions_string)
    else:
        print("\nNão foi possível encontrar uma solução.")
    print("-" * 30)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Formato de execução: python LabirintoCusto.py <mapa.txt> <lin_inicial> <col_inicial> <algoritmo>")
        print("Algoritmos disponíveis: bfs, dfs, ucs, astar")
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])