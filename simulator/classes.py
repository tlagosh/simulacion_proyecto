# Archivo de clases del proyecto

import numpy as np
import random
import math
import time
import sys
import os

class Planta:

    def __init__(self, x, y, distribucion_demanda, hora_inicial, hora_termino, x_1=0, x_2=0, x_3=0):
        self.x = x
        self.y = y
        self.hora_inicial = hora_inicial
        self.hora_termino = hora_termino
        self.x_1 = x_1
        self.x_2 = x_2
        self.x_3 = x_3

        if distribucion_demanda == "Normal":
            self.distribucion_demanda = np.random.normal(self.x_1, self.x_2, 1000000)
            # El inventario inicial es de 2 veces el promedio de la demanda
            self.inventario = 2 * self.distribucion_demanda.mean()
        elif distribucion_demanda == "Triangular":
            self.distribucion_demanda = np.random.triangular(self.x_1, self.x_2, self.x_3, 1000000)
            # El inventario inicial es de 2 veces el promedio de la demanda
            self.inventario = 2 * self.distribucion_demanda.mean()

        self.demanda_actual = 0
        

class Celda:

    def __init__(self, x, y, produccion, cam_min, cam_max, capacidad_camion):
        self.x = x
        self.y = y
        self.produccion = produccion

        self.camiones = []
        cantidad_camiones = random.randint(cam_min, cam_max)
        for i in range(cantidad_camiones):
            self.camiones.append(Camion(i, self.x, self.y, capacidad_camion))


class Camion:

    def __init__(self, id, x, y, capacidad):
        self.id = id
        self.x = x
        self.y = y
        self.capacidad = capacidad
        self.carga_actual = 0
        self.hora_llegada = 0
        self.hora_salida = 0
        self.id_planta = 0
