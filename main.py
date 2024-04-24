import os.path
from cubo import Cubo
from buscador import Buscador


def cargar_desde_archivo(filename):
    with open(filename, "r") as file:
        estado = "".join(line.strip().replace(" ", "") for line in file)
    estado = estado.lower()
    if len(estado) < 54:
        raise ValueError("Faltan mas caracteres")
    if len(estado) > 54:
        raise ValueError("Deben ser menos caracteres")
    color_count = {color: estado.count(color) for color in set(estado)}
    for color, count in color_count.items():
        if count != 9:
            raise ValueError(f"Numero invalido de colores hay {color} veces")
    return estado


def generar_heuristica(estado, acciones, movimientos, heuristica=None):
    if heuristica is None:
        heuristica = {estado: 0}
    que = [(estado, 0)]
    print("Espere.....")
    processed_nodes = 0
    while True:
        if not que:
            break
        s, d = que.pop()
        if d > movimientos:
            continue
        for a in ACCIONES:
            cubo = Cubo(estado=s)
            if a[0] == "h":
                cubo.giro_horizontal(a[1], a[2])
            elif a[0] == "v":
                cubo.giro_vertical(a[1], a[2])
            elif a[0] == "s":
                cubo.giro_profundo(a[1], a[2])
            a_str = cubo.to_string()
            if a_str not in heuristica or heuristica[a_str] > d + 1:
                heuristica[a_str] = d + 1
                que.append((a_str, d + 1))
            processed_nodes += 1

    
   
    with open("heuristica.txt", "w") as f:
        for key, value in heuristica.items():
            f.write(f"{key}: {value}\n")
    print("Terminado")
    return heuristica


def leer_heuristica(archivo):

    with open(archivo, "r") as f:
        heuristica = {}
        for line in f:
            items = line.strip().split(': ')
            if len(items) == 2:
                key, value = items
                heuristica[key] = int(value)
    return heuristica


estado = cargar_desde_archivo("cubo.txt")
cubo = Cubo(estado=estado)
ACCIONES = [(r, n, d) for r in ['h', 'v', 'p'] for d in [0, 1] for n in
            range(cubo.n)]  
cubo.mostrar()

if os.path.exists("heuristica.txt"):
    heuristica = leer_heuristica("heuristica.txt")
else:
    generar_heuristica(estado=cubo.iniciar(),acciones=ACCIONES, movimientos=5)
    heuristica = leer_heuristica("heuristica.txt")

buscador = Buscador(heuristica)
movimientos = buscador.camino_ida_star(cubo.to_string())
for movimiento in movimientos:
    if movimiento[0] == 'h':
        if movimiento[2]==1:
            print(f"Giro horizontal : fila({movimiento[1] + 1}) direccion:derecha")
        else:
            print(f"Giro horizontal : fila({movimiento[1] + 1}) direccion:izquierda")
        cubo.giro_horizontal(movimiento[1], movimiento[2])
    elif movimiento[0] == 'v':
        if movimiento[2]==1:
            print(f"Giro vertical : columna({movimiento[1] + 1}) direccion:arriba")
        else:
            print(f"Giro vertical : columna({movimiento[1] + 1}) direccion:abajo")
        cubo.giro_vertical(movimiento[1], movimiento[2])
    elif movimiento[0] == 'p':
        if movimiento[2] == 0:
            print(f"Giro profundo : columna({movimiento[1] + 1}) empezando de la cara azul direccion:arriba")
        else:
            print(f"Giro profundo : columna({movimiento[1] + 1}) empezando de la cara azul direccion:abajo")
        cubo.giro_profundo(movimiento[1], movimiento[2])    
cubo.mostrar()