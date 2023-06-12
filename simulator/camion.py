from params import CAPACIDAD_CAMION, VELOCIDAD_CAMION, COSTO_TRANSPORTE, 


class Camion:

    def __init__(self, id, x, y):
        self.id = id
        self.capacidad = CAPACIDAD_CAMION
        self.velocidad = VELOCIDAD_CAMION
        self.carga_actual = 0
        self.hora_llegada = 0
        self.hora_salida = 0
        self.id_planta = 0
        self.celda_inicio = (x, y)


    def distancia(self, x, y):
        return abs(self.celda_inicio[0] - x) + abs(self.celda_inicio[1] - y)
    
    def puedo_llegar(self, planta):
        distancia = 0
        puedo_llegar = False
        if self.velocidad*distancia < planta.hora_termino - planta.hora_inicial:
            puedo_llegar = True
        return puedo_llegar
            
