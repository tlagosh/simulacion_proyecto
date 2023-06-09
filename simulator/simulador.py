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
        for planta in params.INIT_PLANTAS:
            if planta[2] == "Normal":
                planta[3] = (planta[3][0], planta[3][1], 0)
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
        if not self.hay_lluvia():
            self.iniciar_dia()

        self.finalizar_dia()

    def hay_lluvia(self):
        return random.random() < params.PROBABILIDAD_LLUVIA

    def iniciar_dia(self):
        for planta in self.plantas:
            planta.set_demanda_diaria()
            if planta.quiebre_de_stock():
                self.planta.data.costos[self.dia]["costo_quiebre_stock"] += params.COSTO_QUIEBRE_STOCK
                self.enviar_camiones(planta)

    def enviar_camiones(self, planta):
        pass

    def finalizar_dia(self):
        self.dia += 1
