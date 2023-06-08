import numpy as np


class Planta:

    def __init__(self, x, y, distribucion_demanda, hora_inicial, hora_termino, primer_parametro_distribucion=0, segundo_parametro_distribucino=0, tercer_parametro_distribucion=0):
        self.x = x
        self.y = y
        self.hora_inicial = hora_inicial
        self.hora_termino = hora_termino
        self.primer_parametro_distribucion = primer_parametro_distribucion
        self.segundo_parametro_distribucino = segundo_parametro_distribucino
        self.tercer_parametro_distribucion = tercer_parametro_distribucion
        if distribucion_demanda == "Normal":
            self.distribucion_demanda = np.random.normal(
                self.primer_parametro_distribucion, self.segundo_parametro_distribucino, 1000000)
            self.inventario = 2 * self.distribucion_demanda.mean()
        elif distribucion_demanda == "Triangular":
            self.distribucion_demanda = np.random.triangular(
                self.primer_parametro_distribucion, self.segundo_parametro_distribucino, self.tercer_parametro_distribucion, 1000000)
            self.inventario = 2 * self.distribucion_demanda.mean()
        self.demanda_actual = 0
