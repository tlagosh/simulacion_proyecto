import numpy as np
from params import HORA_INICIAL, HORA_TERMINO, COSTO_TRANSPORTE, COSTO_INVENTARIO
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
        self.inventario = 0
        self.demanda_diaria = 0
        # Si es mayor a 0 sumar uno a data.dias_demanda_insatisfecha
        self.demanda_pendiente = 0
        self.camiones = []
        # Por política actual de reposición:
        self.celdas = []
        self.data = Data()

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
        return self.inventario < self.demanda_diaria

    def subir_inventario(self, cantidad):
        self.inventario += cantidad

    def demanda_satisfecha(self):
        return self.inventario >= self.demanda_diaria

    def recibir_camion(self, camion):
        self.camiones.append(camion)

    def recibir_camiones(self, camiones):
        self.camiones += camiones
        self.inventario += sum([camion.capacidad for camion in camiones])

    def set_inventario_inicial(self):
        self.inventario = 2 * self.distribucion_demanda.mean()

    def set_quiebre_de_stock_inicial(self):
        self.inventario = 2 * self.distribucion_demanda.mean()

    def hacer_pedido(self):
        # Todos los dias se pide lo que falta para llegar a 3*promedio_demanda_diaria
        # Si hay demanda pendiente, se pide toda la demanda pendiente + 3*promedio_demanda_diaria

        pedido = 0
        if self.demanda_pendiente > 0:
            pedido = self.demanda_pendiente + 3 * self.distribucion_demanda.mean()
        else:
            if self.inventario < 3 * self.distribucion_demanda.mean():
                pedido = 3 * self.distribucion_demanda.mean() - self.inventario

        return pedido

    def satisfacer_demanda(self):
        self.inventario - self.demanda_diaria

    def finalizar_dia(self, dia):
        for camion in self.camiones:
            self.data.recorridos[dia].append(camion.celda_inicio)
            self.data.costos[dia]["costo_transporte"] += self.costo_distancia_recorrida(
                camion)
        self.data.costos[dia]["costo_inventario"] += int(self.inventario * COSTO_INVENTARIO)

    def costo_distancia_recorrida(self, camion):
        return camion.capacidad*COSTO_TRANSPORTE*(abs(self.x - camion.celda_inicio[0]) + abs(self.y - camion.celda_inicio[1]))
