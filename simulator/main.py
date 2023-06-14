from simulador import Simulador
import json
from params import REPLICAS


def print_medidas_desempeño(plantas):

    print("\n")
    print("###### Medidas de desempeño Ultima Replica ######")
    print("\n")

    planta_id = 0

    costo_total_transporte = 0
    costo_total_inventario = 0
    costo_total_quiebre = 0

    for planta in plantas:

        print(f"###### Planta {planta_id} ######")

        # Imprimimos los días de quiebre de stock para cada planta
        print(f"Días demanda insatisfecha: {planta.data.dias_demanda_insastisfecha}")

        # imprimimos el número de días donde el costo de quiembre de stock fue mayor a 0
        
        dias_quiebre = 0
        costo_planta_quiebre = 0
        costo_planta_transporte = 0
        costo_planta_inventario = 0
        for dia in planta.data.costos:
            costo_planta_quiebre += planta.data.costos[dia]["costo_quiebre_stock"]
            costo_planta_transporte += planta.data.costos[dia]["costo_transporte"]
            costo_planta_inventario += planta.data.costos[dia]["costo_inventario"]
            if planta.data.costos[dia]["costo_quiebre_stock"] > 0:
                dias_quiebre += 1

        print(f"Días quiebre de stock: {dias_quiebre}")

        print(f"Costo total de quiebre de stock: {costo_planta_quiebre}")
        print(f"Costo total de transporte: {costo_planta_transporte}")
        print(f"Costo total de inventario: {costo_planta_inventario}")

        planta_id += 1

        costo_total_transporte += costo_planta_transporte
        costo_total_inventario += costo_planta_inventario
        costo_total_quiebre += costo_planta_quiebre

    print("###### Totales ######")

    print(f"Costo total de quiebre de stock: {costo_total_quiebre}")
    print(f"Costo total de transporte: {costo_total_transporte}")
    print(f"Costo total de inventario: {costo_total_inventario}")

def print_medidas_promedio(simulaciones):

    print("\n")
    print("###### Medidas de desempeño Promedio ######")

    costo_total_transporte = 0
    costo_total_inventario = 0
    costo_total_quiebre = 0

    for replica in simulaciones.values():

        costo_promedio_transporte = 0
        costo_promedio_inventario = 0
        costo_promedio_quiebre = 0

        for planta in replica:
            costo_planta_quiebre = 0
            costo_planta_transporte = 0
            costo_planta_inventario = 0
            for dia in planta.data.costos:
                costo_planta_quiebre += planta.data.costos[dia]["costo_quiebre_stock"]
                costo_planta_transporte += planta.data.costos[dia]["costo_transporte"]
                costo_planta_inventario += planta.data.costos[dia]["costo_inventario"]
            costo_promedio_quiebre += costo_planta_quiebre
            costo_promedio_transporte += costo_planta_transporte
            costo_promedio_inventario += costo_planta_inventario

        costo_total_quiebre += costo_promedio_quiebre
        costo_total_transporte += costo_promedio_transporte
        costo_total_inventario += costo_promedio_inventario

    costo_total_quiebre /= len(simulaciones)
    costo_total_transporte /= len(simulaciones)
    costo_total_inventario /= len(simulaciones)

    print(f"Costo promedio de quiebre de stock: {costo_total_quiebre}")
    print(f"Costo promedio de transporte: {costo_total_transporte}")
    print(f"Costo promedio de inventario: {costo_total_inventario}")



if __name__ == "__main__":

    simulador = Simulador()
    simulaciones = simulador.simular_n(REPLICAS)
    planta_id = 0

    # almacenamos los datos de cada planta de la última simulación para ser analizados
    for planta in simulaciones[REPLICAS - 1]:
        with open(f"planta{planta_id}.json", "w") as file:
            json.dump(planta.data.costos, file, indent=4,
                      sort_keys=True, default=str)
        with open(f"planta{planta_id}recorridos.json", "w") as file:
            json.dump(planta.data.recorridos, file, indent=4,
                      sort_keys=True, default=str)
        with open(f"planta{planta_id}lluvia.json", "w") as file:
            json.dump(planta.data.lluvia, file, indent=4,
                      sort_keys=True, default=str)
        
        planta_id += 1
    
    # imprimimos las medidas de desempeño de la última simulación
    print_medidas_desempeño(simulaciones[REPLICAS - 1])

    print("\n____________________________________________________")

    # calculamos las medidas de desempeño promedio de todas las simulaciones
    print_medidas_promedio(simulaciones)

