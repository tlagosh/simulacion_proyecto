from params import CAMIONES_MAX, CAMIONES_MIN, CELDA_PRODUCCION
import random
from camion import Camion


class Celda:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.produccion = CELDA_PRODUCCION
        self.camiones = []
        self.iniciar_camiones()

    def __str__(self):
        return f"Celda: ({self.x}, {self.y})"

    def iniciar_camiones(self):
        self.camiones = []
        cantidad_camiones = random.randint(CAMIONES_MIN, CAMIONES_MAX)
        for i in range(cantidad_camiones):
            self.camiones.append(Camion(i, self.x, self.y))

    def enviar_camion(self):
        camion = self.camiones.pop()
        return camion

    def madera_disponible(self):

        cantidad_madera = 0
        for camion in self.camiones:
            cantidad_madera += camion.capacidad

        return cantidad_madera

    def enviar_camiones(self, planta):
        return self.camiones

    def quedan_camiones(self):
        return len(self.camiones) > 0
