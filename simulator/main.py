from simulador import Simulador
import json


if __name__ == "__main__":
    simulador = Simulador()
    plantas = simulador.simular()
    planta_id = 0
    for planta in plantas:
        with open(f"planta{planta_id}.json", "w") as file:
            json.dump(planta.data.costos, file, indent=4,
                      sort_keys=True, default=str)
        with open(f"planta{planta_id}recorridos.json", "w") as file:
            json.dump(planta.data.recorridos, file, indent=4,
                      sort_keys=True, default=str)
        planta_id += 1
