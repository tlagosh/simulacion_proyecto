import params
import random
from classes import Camion


class Celda:

    def __init__(self, x, y, produccion):
        self.x = x
        self.y = y
        self.produccion = produccion
        self.camiones = []
        cantidad_camiones = random.randint(
            params.CAMIONES_MIN, params.CAMIONES_MAX)
        for i in range(cantidad_camiones):
            self.camiones.append(
                Camion(i, self.x, self.y, params.CAPACIDAD_CAMION))
