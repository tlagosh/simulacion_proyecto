from camion import Camion
from celda import Celda
from planta import Planta
import params
import random


class Simulador:
    def __init__(self):
        self.dia = 0
        self.celdas = []
        self.plantas = []

    def simular(self):
        self.generar_plantas()
        self.generar_celdas()
        self.set_destino_camiones()
        while self.dia < params.DIAS_SIMULACION:
            self.main_loop()

    def generar_plantas(self):
        for planta in params.PLANTAS:
            if planta[2] == "Normal":
                self.plantas.append(Planta(
                    planta[0], planta[1], planta[2], planta[3][0], planta[3][1]))
            else:
                self.plantas.append(Planta(
                    planta[0], planta[1], planta[2], planta[3][0], planta[3][1], planta[3][2]))

    def generar_celdas(self):
        for x in range(params.X_MAX_MAPA):
            for y in range(params.Y_MAX_MAPA):
                celda = True
                for planta in self.plantas:
                    if x == planta[0] and y == planta[1]:
                        celda = False
                    elif abs(x - planta[0]) <= 1 and abs(y - planta[1]) <= 1:
                        celda = False
                        break
                if celda:
                    self.celdas.append(Celda(x, y))

    def set_destino_camiones(self):
        for celda in self.celdas:
            for camion in celda.camiones:
                posibles_plantas = list(
                    filter(lambda planta: not planta.demanda_satisfecha(), self.plantas))
                camion.set_destino(posibles_plantas)

    def main_loop(self):
        self.iniciar_dia()
        self.finalizar_dia()

    def hay_lluvia(self):
        return random.random() < params.PROBABILIDAD_LLUVIA

    def iniciar_dia(self):
        for planta in self.plantas:
            planta.set_demanda_diaria()
            if planta.quiebre_de_stock():
                self.planta.data.costos[self.dia]["costo_quiebre_stock"] += params.COSTO_QUIEBRE_STOCK
            # RESTAR DEMANDA DE INVENTARIO
            # Si el inventario no alcanza para la demanda de hoy, quedo con demanda pendiente para el dia siguiente
            if not self.hay_lluvia():
                # Pedir camiones
                pass
            # self.enviar_camiones(planta)

    def enviar_camiones(self, planta):
        while planta.quiebre_de_stock():
            nearest_celda = self.get_nearest_celda(planta)
            camion_a_enviar = nearest_celda.enviar_camion(planta)
            if camion_a_enviar.planta_destino == (planta.x, planta.y):
                planta.recibir_camion(camion_a_enviar)

    def get_nearest_celda(self, planta):
        nearest_celda = self.celdas[0]
        for celda in self.celdas:
            if self.get_distance(planta, celda) < self.get_distance(planta, nearest_celda):
                nearest_celda = celda
        return nearest_celda

    def get_distance(self, planta, celda):
        return abs(planta.x - celda.x) + abs(planta.y - celda.y)

    def finalizar_dia(self):
        self.dia += 1
