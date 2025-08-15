from typing import List

def ler_config(path: str) -> List[List[int]]:
    """
    Lê o arquivo configuracao.txt e devolve uma matriz de inteiros.
    '0' = parede. Demais = id da célula.
    """
    grid: List[List[int]] = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # ignora linhas vazias
                continue
            row = [int(x) for x in line.split(';')]
            grid.append(row)
    return grid

# ---- teste rápido ----
if __name__ == "__main__":
    grid = ler_config("configuracao.txt")
    print("Linhas:", len(grid))
    print("Colunas:", len(grid[0]))
    print("Primeira linha:", grid[0])
    print("Última linha:", grid[-1])
