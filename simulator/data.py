import params


class Data:
    def __init__(self):
        self.costos = {}
        self.set_costos()
        self.dias_demanda_insastisfecha = 0

    def set_costos(self):
        for dia in range(0, params.DIAS_SIMULACION):
            self.costos[dia] = {}
            self.costos[dia]["costo_transporte"] = 0
            self.costos[dia]["costo_inventario"] = 0
            self.costos[dia]["costo_quiebre_stock"] = 0

    def costo_total_transporte(self):
        return sum([value["costo_transporte"] for value in self.costos.values()])

    def costo_total_inventario(self):
        return sum([value["costo_inventario"] for value in self.costos.values()])

    def costo_total_quiebre_stock(self):
        return sum([value["costo_quiebre_stock"] for value in self.costos.values()])

    def costo_total(self):
        return self.costo_total_transporte() + self.costo_total_inventario() + self.costo_total_quiebre_stock()
