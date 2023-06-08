from camion import Camion
from celda import Celda
from planta import Planta
import params


class Simulador:
    def __init__(self):
        self.t = 0
        self.celdas = []
        self.plantas = []

    def generar_plantas(self):
        for planta in params.INIT_PLANTAS:
            if planta[2] == "Normal":
                planta[3] = (planta[3][0], planta[3][1], 0)
            self.plantas.append(Planta(planta[0], planta[1], planta[2], params.HORA_INICIAL,
                                params.HORA_TERMINO, planta[3][0], planta[3][1], planta[3][2]))

    def generar_celdas(self):
        for x in range(params.X_MAX_MAPA):
            for y in range(params.Y_MAX_MAPA):
                celda = True
                for planta in self.plantas:
                    if x == planta[0] and y == planta[1]:
                        celda = False
                        break
                if celda:
                    self.celdas.append(Celda(x, y, params.PRODUCCION))

    def simular(self):
        self.generar_plantas()
        self.generar_celdas()
        while self.t < params.HORA_TERMINO:
            self.main_loop()

    def main_loop(self):
        pass
