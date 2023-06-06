# This proyect consist in a simulator for a wood factory, the factory is 100x100 km
# and is divided in 100 sectors of 10x10 km,
# in three of this sectors there are factorys that recive wood from the forest
# and produce wood planks, the rest of the sectors are forest.

import random
import math
import time
import sys
import os
import numpy as np
from classes import Planta, Celda, Camion

def generar_celdas(x_max, y_max, plantas):

    celdas = []
    for i in range(x_max):
        for j in range(y_max):
            celda = True
            for planta in plantas:
                if i == planta[0] and j == planta[1]: 
                    celda = False
                    break
            if celda:
                celdas.append(Celda(i, j, PRODUCCION, CAM_MIN, CAM_MAX, CAPACIDAD_CAMION))

    plantas = []
    for planta in plantas:
        if planta[2] == "Normal":
            planta[3] = (planta[3][0], planta[3][1], 0)
        plantas.append(Planta(planta[0], planta[1], planta[2], HORA_INICIAL, HORA_TERMINO, planta[3][0], planta[3][1], planta[3][2]))

    return celdas, plantas

def simulacion(celdas, plantas):

    pass


def main():

    # generamos las celdas y las plantas
    celdas, plantas = generar_celdas(10, 10, INIT_PLANTAS)

    # iniciamos la simulacion
    simulacion(celdas, plantas)

    pass

if __name__ == "__main__":

    ## PARAMETROS ##
    PRODUCCION = 1000
    CAM_MIN = 3
    CAM_MAX = 7
    CAPACIDAD_CAMION = 30
    HORA_INICIAL = 7
    HORA_TERMINO = 17
    COSTO_TRANSPORTE = 0.1 # Costo de transporte por tonelada por km
    COSTO_INVENTARIO = float(input("Ingrese el costo de inventario por tonelada por día (a): ")) # Costo de inventario por tonelada por día
    COSTO_QUIEBRE_DE_STOCK = float(input("Ingrese el costo de quiebre de stock (b): ")) # Costo único de quiebre de stock
    INIT_PLANTAS = [(3, 2, "Normal", (4000, 200)), (7, 5, "Normal", (5000, 300)), (4, 8, "Triangualar", (4000, 5500, 7000))]
    ## PARAMETROS ##

    main()
