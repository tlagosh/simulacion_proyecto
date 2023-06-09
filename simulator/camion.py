from params import CAPACIDAD_CAMION, VELOCIDAD_CAMION, COSTO_TRANSPORTE


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
        self.planta_destino = tuple()

    def set_destino(self, plantas):
        planta_destino = min(plantas, key=lambda planta: self.distancia(
            planta.x, planta.y))
        self.planta_destino = (planta_destino.x, planta_destino.y)

    def distancia(self, x, y):
        return abs(self.celda_inicio[0] - x) + abs(self.celda_inicio[1] - y)
