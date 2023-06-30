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
        self.madera_disponible = int(self.produccion/365)

    def __str__(self):
        return f"Celda: ({self.x}, {self.y})"
    
    def iniciar_madera(self):
        self.madera_disponible = int(self.produccion/365)

    def iniciar_camiones(self):
        self.camiones = []
        cantidad_camiones = random.randint(CAMIONES_MIN, CAMIONES_MAX)
        for i in range(cantidad_camiones):
            self.camiones.append(Camion(i, self.x, self.y))

    def enviar_camion(self):
        camion = self.camiones.pop()
        if self.madera_disponible >= camion.capacidad:
            self.madera_disponible -= camion.capacidad
            return camion
        else:
            return None
    
    def enviar_n_camiones(self, n):
        camiones = []
        for i in range(n):
            camiones.append(self.camiones.pop())

        camiones_que_se_pueden_enviar = []
        for camion in camiones:
            if self.madera_disponible >= camion.capacidad:
                self.madera_disponible -= camion.capacidad
                camiones_que_se_pueden_enviar.append(camion)
        
        return camiones_que_se_pueden_enviar

    def madera_disponible_para_transportar(self):

        cantidad_madera = 0
        for camion in self.camiones:
            cantidad_madera += camion.capacidad

        return min(cantidad_madera, self.madera_disponible)

    def enviar_camiones(self, planta):
        camiones = []
        while self.madera_disponible > 0 and len(self.camiones) > 0:
            camion = self.enviar_camion()
            if camion != None:
                camiones.append(camion)
            else:
                break

        return camiones

    def quedan_camiones(self):
        return len(self.camiones) > 0
    
    def camiones_disponibles(self):
        return len(self.camiones)
