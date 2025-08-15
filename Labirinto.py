from typing import List, Optional, Tuple

def id_celula(grid: List[List[int]], r: int, c: int) -> Optional[int]:
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
        return None
    v = grid[r][c]
    return v if v != 0 else None

# ---- VARIANTES (entradas x,y vindas da CLI) ----
# Interpretação A: origem no TOPO-ESQUERDO (top-left)

def map_top_left_colrow_1b(x: int, y: int) -> Tuple[int,int]:
    # x=coluna (1-based), y=linha (1-based)
    r = y - 1
    c = x - 1
    return r, c

def map_top_left_rowcol_1b(x: int, y: int) -> Tuple[int,int]:
    # x=linha (1-based), y=coluna (1-based)
    r = x - 1
    c = y - 1
    return r, c

def map_top_left_colrow_0b(x: int, y: int) -> Tuple[int,int]:
    # x=coluna (0-based), y=linha (0-based)
    r = y
    c = x
    return r, c

def map_top_left_rowcol_0b(x: int, y: int) -> Tuple[int,int]:
    # x=linha (0-based), y=coluna (0-based)
    r = x
    c = y
    return r, c

# Interpretação B: origem em BAIXO-ESQUERDO (bottom-left)

def map_bottom_left_colrow_1b(x: int, y: int, nlinhas: int) -> Tuple[int,int]:
    # x=coluna (1-based), y=linha (1-based; cresce para cima)
    r = (nlinhas - y)
    c = x - 1
    return r, c

def map_bottom_left_rowcol_1b(x: int, y: int, nlinhas: int) -> Tuple[int,int]:
    # x=linha (1-based; cresce para cima), y=coluna (1-based)
    r = (nlinhas - x)
    c = y - 1
    return r, c

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

def testar_mapeamentos(grid: List[List[int]], x: int, y: int) -> None:
    n = len(grid)
    casos = [
        ("TL col,row 1-based",  lambda x,y: map_top_left_colrow_1b(x,y)),
        ("TL row,col 1-based",  lambda x,y: map_top_left_rowcol_1b(x,y)),
        ("TL col,row 0-based",  lambda x,y: map_top_left_colrow_0b(x,y)),
        ("TL row,col 0-based",  lambda x,y: map_top_left_rowcol_0b(x,y)),
        ("BL col,row 1-based",  lambda x,y: map_bottom_left_colrow_1b(x,y,n)),
        ("BL row,col 1-based",  lambda x,y: map_bottom_left_rowcol_1b(x,y,n)),
    ]
    for nome, fn in casos:
        r, c = fn(x, y)
        cid = id_celula(grid, r, c)
        print(f"{nome:>20} → (r={r}, c={c}) → id={cid}")

if __name__ == "__main__":
    from typing import List

    # você já tem a função ler_config(path)
    grid: List[List[int]] = ler_config("configuracao.txt")

    # Teste com as coordenadas do enunciado
    x, y = 4, 1
    testar_mapeamentos(grid, x, y)
