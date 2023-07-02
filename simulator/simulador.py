from camion import Camion
from celda import Celda
from planta import Planta
import params
from params import INVENTARIO_OBJETIVO
import random
from tqdm import tqdm


class Simulador:
    def __init__(self):
        self.dia = 0
        self.celdas = []
        self.plantas = []
        self.politica = ""
        self.camiones_sobrantes_simulación = 0

    def simular_n(self, numero_replicas, politica):

        plantas_por_simulación = {}
        self.politica = politica

        for i in tqdm(range(numero_replicas)):
            self.dia = 0
            self.celdas = []
            self.plantas = []
            plantas = self.simular()
            plantas_por_simulación[i] = plantas
            print(f"Camiones sobrantes: {self.camiones_sobrantes_simulación}")
        
        return plantas_por_simulación

    def simular(self):
        self.generar_plantas()
        self.generar_celdas()
        self.camiones_sobrantes_simulación = 0

        # Dado la política de restock actual, tenemos que asignar las celdas a plantas
        # Lo anterior se hace con la siguiente función
        if self.politica == "E":
            self.asignar_celdas_a_plantas()
        
        progress_bar = tqdm(total=params.DIAS_SIMULACION)

        while self.dia < params.DIAS_SIMULACION + params.DIAS_TRANSIENTE:
            self.main_loop()
            progress_bar.update(1)
        
        progress_bar.close()

        return self.plantas

    def generar_plantas(self):
        id_planta = 0
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
            self.plantas.append(planta__nueva)
            id_planta += 1

    def generar_celdas(self):
        id_celda = 0
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
                    id_celda += 1

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
                if self.dia >= params.DIAS_TRANSIENTE:
                    planta.data.lluvia[self.dia - params.DIAS_TRANSIENTE] = True

        self.finalizar_dia()

    def hay_lluvia(self):
        return random.random() < params.PROBABILIDAD_LLUVIA

    def iniciar_dia(self):

        params.PROBABILIDAD_LLUVIA += params.PROBABILIDAD_LLUVIA_INCREMENTO

        for planta in self.plantas:
            # Se inicia por revisar si hay quiebre de stock
            if planta.quiebre_de_stock():
                if self.dia >= params.DIAS_TRANSIENTE:
                    planta.data.costos[self.dia - params.DIAS_TRANSIENTE]["costo_quiebre_stock"] += params.COSTO_QUIEBRE_STOCK

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
                if self.dia >= params.DIAS_TRANSIENTE:
                    planta.data.dias_demanda_insastisfecha += 1

        for celda in self.celdas:
            celda.iniciar_camiones()
            celda.iniciar_madera()

    def enviar_camiones(self):

        ## Politica de restock ESTÁTICA ##
        if self.politica == "E":
            for planta in self.plantas:

                pedido = planta.hacer_pedido()

                if pedido > 0:
                    for coordenadas_celda in planta.celdas:

                        # Enviar camiones de esa celda a la planta
                        if pedido > 0:
                            celda = self.get_celda(coordenadas_celda)
                            if celda.quedan_camiones() and celda.camiones[0].puedo_llegar(planta):
                                pedido -= celda.madera_disponible_para_transportar()
                                camiones = celda.enviar_camiones(planta)
                                planta.recibir_camiones(camiones)

                        else:
                            break
        
            for celda in self.celdas:
                if celda.camiones_disponibles() > 0:
                    self.camiones_sobrantes_simulación += celda.camiones_disponibles()

        ## Politica de restock DINAMICA ##
        elif self.politica == "D":

            camiones_por_celda = []
            for celda in self.celdas:
                factores_plantas = []

                for planta in self.plantas:
                    factor = planta.get_factor(celda)
                    factores_plantas.append((planta, factor))

                # print([x[1] for x in factores_plantas])

                suma_factores = sum([x[1] for x in factores_plantas])

                # print([x[1] for x in factores_plantas], suma_factores, celda.camiones_disponibles())
                camiones_plantas = [(x[0], int(x[1] * ((celda.camiones_disponibles() / suma_factores) if suma_factores > 0 else 0))) for x in factores_plantas]

                if sum([x[1] for x in camiones_plantas]) < celda.camiones_disponibles():
                    # Le pasamos los camiones restantes a la planta con mayor factor
                    camiones_plantas = sorted(camiones_plantas, key=lambda x: x[1], reverse=True)
                    camiones_plantas[0] = (camiones_plantas[0][0], camiones_plantas[0][1] + (celda.camiones_disponibles() - sum([x[1] for x in camiones_plantas])))

                # print(camiones_plantas)

                camiones_por_celda.append((celda, camiones_plantas))

            pedidos = []
            for planta in self.plantas:
                pedido = planta.hacer_pedido()
                pedidos.append((planta, pedido))

            # # print(pedidos)
            
            pedidos = sorted(pedidos, key=lambda x: x[1], reverse=True)

            for planta, pedido in pedidos:
                camiones_por_celda = sorted(camiones_por_celda, key=lambda x: self.get_distance(planta, x[0]), reverse=True)
                camiones_sobrantes = 0
                for celda, camiones_plantas in camiones_por_celda:
                    if pedido > 0:
                        for planta2, camiones in camiones_plantas:
                            if planta == planta2:
                                if camiones > 0:
                                    if celda.quedan_camiones() and celda.camiones[0].puedo_llegar(planta):
                                        camiones = celda.enviar_n_camiones(camiones)
                                        planta.recibir_camiones(camiones)
                                        pedido -= len(camiones) * params.CAPACIDAD_CAMION
                                else:
                                    break
                    else:
                        for planta2, camiones in camiones_plantas:
                            if planta == planta2:
                                camiones_sobrantes += camiones

                        # planta_que_recibe = 0
                        # for planta2, camiones in camiones_plantas:
                        #     if planta != planta2:
                        #         if planta_que_recibe == 0:
                        #             camiones += int(camiones_sobrantes/2)
                        #             camiones_sobrantes -= int(camiones_sobrantes/2)
                        #             planta_que_recibe += 1
                        #         else:
                        #             camiones += int(camiones_sobrantes)
            
            for celda in self.celdas:
                if celda.camiones_disponibles() > 0:
                    self.camiones_sobrantes_simulación += celda.camiones_disponibles()

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
