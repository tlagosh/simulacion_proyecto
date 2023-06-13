from camion import Camion
from celda import Celda
from planta import Planta
import params
import random
from tqdm import tqdm


class Simulador:
    def __init__(self):
        self.dia = 0
        self.celdas = []
        self.plantas = []

    def simular(self):
        self.generar_plantas()
        self.generar_celdas()

        # Dado la política de restock actual, tenemos que asignar las celdas a plantas
        # Lo anterior se hace con la siguiente función
        self.asignar_celdas_a_plantas()
        
        progress_bar = tqdm(total=params.DIAS_SIMULACION)

        while self.dia < params.DIAS_SIMULACION:
            self.main_loop()
            progress_bar.update(1)
        
        progress_bar.close()

        return self.plantas

    def generar_plantas(self):
        for planta in params.PLANTAS:
            if planta[2] == "Normal":
                planta__nueva = Planta(
                    planta[0], planta[1], planta[2], planta[3][0], planta[3][1])
                planta__nueva.set_distribucion_normal()
            else:
                planta__nueva = Planta(
                    planta[0], planta[1], planta[2], planta[3][0], planta[3][1], planta[3][2])
                planta__nueva.set_distribucion_triangular()
            planta__nueva.set_inventario_inicial()
            planta__nueva.set_quiebre_de_stock_inicial()
            self.plantas.append(planta__nueva)

    def generar_celdas(self):
        for x in range(params.X_MAX_MAPA):
            for y in range(params.Y_MAX_MAPA):
                celda = True
                for planta in self.plantas:
                    if x == planta.x and y == planta.y:
                        celda = False
                    elif (abs(x - planta.x) + abs(y - planta.y) == 1):
                        celda = False
                        break
                if celda:
                    self.celdas.append(Celda(x, y))

    def asignar_celdas_a_plantas(self):
        # Cada planta, por turnos, va a elegir la celda más cercana a ella
        # y se la va a asignar
        celdas_disponibles = self.celdas.copy()
        while len(celdas_disponibles) > 0:
            for planta in self.plantas:
                if len(celdas_disponibles) > 0:
                    celda_mas_cercana = self.get_celda_mas_cercana(
                        celdas_disponibles, planta)
                    planta.celdas.append(
                        (celda_mas_cercana.x, celda_mas_cercana.y))
                    celdas_disponibles.remove(celda_mas_cercana)
                else:
                    break

    def get_celda_mas_cercana(self, celdas, planta):
        celda_mas_cercana = celdas[0]
        for celda in celdas:
            if self.get_distance(planta, celda) < self.get_distance(planta, celda_mas_cercana):
                celda_mas_cercana = celda
        return celda_mas_cercana

    def get_distance(self, planta, celda):
        return abs(planta.x - celda.x) + abs(planta.y - celda.y)

    def main_loop(self):

        self.iniciar_dia()

        # politica de restock
        if not self.hay_lluvia():
            self.enviar_camiones()
        else:
            for planta in self.plantas:
                planta.data.lluvia[self.dia] = True

        self.finalizar_dia()

    def hay_lluvia(self):
        return random.random() < params.PROBABILIDAD_LLUVIA

    def iniciar_dia(self):

        for planta in self.plantas:
            # Se inicia por revisar si hay quiebre de stock
            if planta.quiebre_de_stock():
                planta.data.costos[self.dia]["costo_quiebre_stock"] += params.COSTO_QUIEBRE_STOCK

            # Se setea la demanda diaria
            planta.set_demanda_diaria()
            planta.camiones = []

            # si hay demanda pendiente de dias anteriores, se suma a la demanda diaria
            if planta.demanda_pendiente > 0:
                planta.demanda_diaria += planta.demanda_pendiente
                planta.demanda_pendiente = 0
            # Se resta la demanda del inventario
            planta.inventario -= planta.demanda_diaria

            # Si el inventario no alcanza para la demanda de hoy, quedo con demanda pendiente para el dia siguiente
            if planta.inventario < 0:
                planta.demanda_pendiente = abs(planta.inventario)
                planta.inventario = 0
                planta.data.dias_demanda_insastisfecha += 1

        for celda in self.celdas:
            celda.iniciar_camiones()

    def enviar_camiones(self):

        for planta in self.plantas:

            pedido = planta.hacer_pedido()

            if pedido > 0:
                for coordenadas_celda in planta.celdas:

                    # Enviar camiones de esa celda a la planta
                    if pedido > 0:
                        celda = self.get_celda(coordenadas_celda)
                        if celda.quedan_camiones() and celda.camiones[0].puedo_llegar(planta):
                            pedido -= celda.madera_disponible()
                            camiones = celda.enviar_camiones(planta)
                            planta.recibir_camiones(camiones)

                    else:
                        break

    def get_celda(self, coordenadas_celda):
        for celda in self.celdas:
            if celda.x == coordenadas_celda[0] and celda.y == coordenadas_celda[1]:
                return celda

    def get_nearest_celda(self, planta):
        nearest_celda = self.celdas[0]
        for celda in self.celdas:
            if self.get_distance(planta, celda) < self.get_distance(planta, nearest_celda):
                nearest_celda = celda
        return nearest_celda

    def finalizar_dia(self):
        for planta in self.plantas:
            planta.finalizar_dia(self.dia)
        self.dia += 1
        id = 0
        # print("###### DIA " + str(self.dia) + " ######")
        # for planta in self.plantas:
        #     print("Data de Planta " + str(id) + ":")
        #     planta.data.show_data()
        #     print("")
        #     id += 1
