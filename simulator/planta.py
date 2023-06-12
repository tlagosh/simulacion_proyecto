import numpy as np
from params import HORA_INICIAL, HORA_TERMINO
from data import Data


class Planta:

    def __init__(self, x, y, distribucion_demanda, primer_parametro_distribucion=0, segundo_parametro_distribucion=0, tercer_parametro_distribucion=0):
        self.x = x
        self.y = y
        self.hora_inicial = HORA_INICIAL
        self.hora_termino = HORA_TERMINO
        self.primer_parametro_distribucion = primer_parametro_distribucion
        self.segundo_parametro_distribucion = segundo_parametro_distribucion
        self.tercer_parametro_distribucion = tercer_parametro_distribucion
        self.distribucion_demanda = None
        if distribucion_demanda == "Normal":
            self.set_distribucion_normal()
        elif distribucion_demanda == "Triangular":
            self.set_distribucion_triangular()
        self.inventario = 0
        self.demanda_diaria = 0
        # Si es mayor a 0 sumar uno a data.dias_demanda_insatisfecha
        self.demanda_pendiente = 0
        self.camiones = []
        self.data = Data()
        self.set_inventario_inicial()

    def set_distribucion_normal(self):
        self.distribucion_demanda = np.random.normal(
            self.primer_parametro_distribucion, self.segundo_parametro_distribucion, 1000000)

    def set_distribucion_triangular(self):
        self.distribucion_demanda = np.random.triangular(
            self.primer_parametro_distribucion, self.segundo_parametro_distribucion, self.tercer_parametro_distribucion, 1000000)

    def set_demanda_diaria(self):
        self.demanda_diaria = np.random.choice(
            self.distribucion_demanda, size=1)

    def quiebre_de_stock(self):
        return self.inventario < 2 * self.distribucion_demanda.mean()

    def subir_inventario(self, cantidad):
        self.inventario += cantidad

    def demanda_satisfecha(self):
        return self.inventario >= self.demanda_diaria

    def recibir_camion(self, camion):
        self.camiones.append(camion)

    def set_inventario_inicial(self):
        self.inventario = 2 * self.distribucion_demanda.mean()

    def hacer_pedido(self):

        # Todos los dias se pide lo que falta para llegar a 3*promedio_demanda_diaria
        # Si hay demanda pendiente, se pide toda la demanda pendiente + 3*promedio_demanda_diaria
        pass

    def satisfacer_demanda(self):
        self.inventario - self.demanda_diaria
