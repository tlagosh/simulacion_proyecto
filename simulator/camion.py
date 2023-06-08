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
