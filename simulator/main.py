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

    print(f"Costo promedio de transporte: {costo_total_transporte}")
    print(f"Costo promedio de inventario: {costo_total_inventario}")
    print(f"Costo promedio de quiebre de stock: {costo_total_quiebre}")

    # print(f"a: ", costo_total_transporte/costo_total_inventario)
    # print(f"b: ", costo_total_transporte/costo_total_quiebre)

def print_grafico_por_replica(simulaciones):

    # we open a csv file to write the data
    with open('grafico_por_replica.csv', 'w') as f:

        # graficamos la suma de costos de transporte, inventario y quiebre de stock de todo el año

        #primero graficamos los títulos de la tabla
        # print("Replica         |Costo Transporte |Costo Inventario |Costo Quiebre Stock |a    |b")
        print("Replica         |Costo Transporte |Costo Inventario |Costo Quiebre Stock |Costo Total |Porcentaje de Satisfaccion de Demanda")
        f.write("Replica,Costo Transporte,Costo Inventario,Costo Quiebre Stock,Costo Total,Porcentaje de Satisfaccion de Demanda\n")

        CT = 0
        CI = 0
        CQ = 0
        A = 0
        B = 0
        DEMANDA_INSATISFECHA = 0
        DEMANDA_TOTAL = 0

        count = 1
        for replica in simulaciones.values():
            costo_total_transporte = 0
            costo_total_inventario = 0
            costo_total_quiebre = 0
            demanda_insatisfecha = 0
            demanda_total = 0
            for planta in replica:
                for dia in planta.data.costos:
                    costo_total_transporte += planta.data.costos[dia]["costo_transporte"]
                    costo_total_inventario += planta.data.costos[dia]["costo_inventario"]
                    costo_total_quiebre += planta.data.costos[dia]["costo_quiebre_stock"]
                demanda_insatisfecha += float(planta.demanda_pendiente)
                demanda_total += float(planta.demanda_total)

            a = costo_total_transporte/costo_total_inventario
            b = costo_total_transporte/costo_total_quiebre

            # print(f"Replica {count}\t|{round(costo_total_transporte, 2)} \t  |{round(costo_total_inventario, 2)}\t    |{round(costo_total_quiebre, 2)} de {365*3}\t |{round(a, 2)} |{round(b, 2)}")
            print(f"Replica {count}\t|{round(costo_total_transporte, 2)} \t  |{round(costo_total_inventario, 2)}\t    |{round(costo_total_quiebre, 2)}\t |{round(costo_total_transporte + costo_total_inventario + costo_total_quiebre, 2)} |{round(((demanda_total - demanda_insatisfecha)/demanda_total)*100, 2)}%")
            f.write(f"{count},{round(costo_total_transporte, 2)},{round(costo_total_inventario, 2)},{round(costo_total_quiebre, 2)},{round(costo_total_transporte + costo_total_inventario + costo_total_quiebre, 2)},{round(((demanda_total - demanda_insatisfecha)/demanda_total)*100, 2)}\n")
            count += 1

            CT += costo_total_transporte
            CI += costo_total_inventario
            CQ += costo_total_quiebre
            A += a
            B += b
            DEMANDA_INSATISFECHA += demanda_insatisfecha
            DEMANDA_TOTAL += demanda_total

        CT /= len(simulaciones)
        CI /= len(simulaciones)
        CQ /= len(simulaciones)
        A /= len(simulaciones)
        B /= len(simulaciones)
        DEMANDA_INSATISFECHA /= len(simulaciones)
        DEMANDA_TOTAL /= len(simulaciones)
        
        # print(f"Promedio\t|{round(CT, 2)} \t  |{round(CI, 2)}\t    |{round(CQ, 2)} de {365*3}\t |{round(A, 2)} |{round(B, 2)}")
        print(f"Promedio\t|{round(CT, 2)} \t  |{round(CI, 2)}\t    |{round(CQ, 2)}\t |{round(CT + CI + CQ, 2)} |{round(((DEMANDA_TOTAL - DEMANDA_INSATISFECHA)/DEMANDA_TOTAL)*100, 2)}%")
        f.write(f"Promedio,{round(CT, 2)},{round(CI, 2)},{round(CQ, 2)},{round(CT + CI + CQ, 2)},{round(((DEMANDA_TOTAL - DEMANDA_INSATISFECHA)/DEMANDA_TOTAL)*100, 2)}\n")
    
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
    # print_medidas_desempeño(simulaciones[REPLICAS - 1])

    print("\n____________________________________________________")

    # calculamos las medidas de desempeño promedio de todas las simulaciones
    # print_medidas_promedio(simulaciones)

    print_grafico_por_replica(simulaciones)

