from random import choice
from cubo import Cubo


class Buscador:
    def __init__(self, heuristica, profundidad=20):
        self.profundidad = profundidad
        self.threshold = profundidad
        self.min_threshold = None
        self.heuristica = heuristica
        self.movimientos = []

    def camino_ida_star(self, estado):
        while True:
            status = self.ida_star(estado, 1)
            if status:
                return self.movimientos
            self.movimientos = []
            self.threshold = self.min_threshold
        return []

    def ida_star(self, estado, valor_g):
        cubo = Cubo(estado=estado)
        if cubo.resuelto():
            return True
        elif len(self.movimientos) >= self.threshold:
            return False
        valor_minimo = float("inf")
        accion_elegida = None
        for a in [
            (r, n, d) for r in ["h", "v", "p"] for d in [0, 1] for n in range(cubo.n)
        ]:
            cubo = Cubo(estado=estado)
            if a[0] == "h":
                cubo.giro_horizontal(a[1], a[2])
            elif a[0] == "v":
                cubo.giro_vertical(a[1], a[2])
            elif a[0] == "p":
                cubo.giro_profundo(a[1], a[2])
            if cubo.resuelto():
                self.movimientos.append(a)
                return True
            cubo_string = cubo.to_string()
            valor_h = (
                self.heuristica[cubo_string]
                if cubo_string in self.heuristica
                else self.profundidad
            )
            valor_f = valor_g + valor_h
            if valor_f < valor_minimo:
                valor_minimo = valor_f
                accion_elegida = [(cubo_string, a)]
            elif valor_f == valor_minimo:
                if accion_elegida is None:
                    accion_elegida = [(cubo_string, a)]
                else:
                    accion_elegida.append((cubo_string, a))
        if accion_elegida is not None:
            if self.min_threshold is None or valor_minimo < self.min_threshold:
                self.min_threshold = valor_minimo
            siguiente_accion = choice(accion_elegida)
            self.movimientos.append(siguiente_accion[1])
            status = self.ida_star(siguiente_accion[0], valor_g + valor_minimo)
            if status:
                return status
        return False

    def a_star(self, estado, valor_g):
        cubo = Cubo(estado=estado)
        if cubo.resuelto():
            return True
        accion_elegida = None
        for a in [
            (r, n, d) for r in ["h", "v", "p"] for d in [0, 1] for n in range(cubo.n)
        ]:
            cubo = Cubo(estado=estado)
            if a[0] == "h":
                cubo.giro_horizontal(a[1], a[2])
            elif a[0] == "v":
                cubo.giro_vertical(a[1], a[2])
            elif a[0] == "p":
                cubo.giro_profundo(a[1], a[2])
            if cubo.resuelto():
                self.movimientos.append(a)
                return True
            cubo_string = cubo.to_string()
            valor_h = (
                self.heuristica[cubo_string]
                if cubo_string in self.heuristica
                else self.profundidad
            )
            valor_f = valor_g + valor_h
            if accion_elegida is None:
                accion_elegida = [(cubo_string, a)]
            else:
                accion_elegida.append((cubo_string, a))
        if accion_elegida is not None:
            siguiente_accion = choice(accion_elegida)
            self.movimientos.append(siguiente_accion[1])
            status = self.ida_star(siguiente_accion[0], valor_f)
            if status:
                return status
        return False

    def camino_a_star(self, estado):
        while True:
            status = self.a_star(estado, 1)
            if status:
                return self.movimientos
            self.movimientos = []
        return []