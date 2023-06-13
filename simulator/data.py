import params


class Data:
    def __init__(self):
        self.costos = {}
        self.set_costos()
        self.dias_demanda_insastisfecha = 0
        self.recorridos = {}
        self.set_recorridos()
        self.lluvia = {}
        self.set_lluvia()

    def set_costos(self):
        for dia in range(0, params.DIAS_SIMULACION):
            self.costos[dia] = {}
            self.costos[dia]["costo_transporte"] = 0
            self.costos[dia]["costo_inventario"] = 0
            self.costos[dia]["costo_quiebre_stock"] = 0

    def set_recorridos(self):
        for dia in range(0, params.DIAS_SIMULACION):
            self.recorridos[dia] = []

    def set_lluvia(self):
        for dia in range(0, params.DIAS_SIMULACION):
            self.lluvia[dia] = False

    def costo_total_transporte(self):
        return sum([value["costo_transporte"] for value in self.costos.values()])

    def costo_total_inventario(self):
        return sum([value["costo_inventario"] for value in self.costos.values()])

    def costo_total_quiebre_stock(self):
        return sum([value["costo_quiebre_stock"] for value in self.costos.values()])

    def costo_total(self):
        return self.costo_total_transporte() + self.costo_total_inventario() + self.costo_total_quiebre_stock()

    def show_data(self):
        print("Costo total de transporte: " +
              str(self.costo_total_transporte()))
        print("Costo total de inventario: " +
              str(self.costo_total_inventario()))
        print("Costo total de quiebre de stock: " +
              str(self.costo_total_quiebre_stock()))
        print("Costo total: " + str(self.costo_total()))
        print("Dias con demanda insatisfecha: " +
              str(self.dias_demanda_insastisfecha))
        
        print("Costo Promedio de transporte: " + str(self.costo_total_transporte()/params.DIAS_SIMULACION))
        print("Costo Promedio de inventario: " + str(self.costo_total_inventario()/params.DIAS_SIMULACION))
        print("Costo Promedio de quiebre de stock: " + str(self.costo_total_quiebre_stock()/params.DIAS_SIMULACION))
        # print("Recorridos: {}".format(self.recorridos))
