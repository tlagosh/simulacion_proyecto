PRODUCCION = 1000
CAMIONES_MIN = 3
CAMIONES_MAX = 7
CAPACIDAD_CAMION = 30
HORA_INICIAL = 7
HORA_TERMINO = 17
# Costo de transporte por tonelada por km
COSTO_TRANSPORTE = 0.1
# Costo de inventario por tonelada por día
COSTO_INVENTARIO = float(
    input("Ingrese el costo de inventario por tonelada por día (a): "))
COSTO_QUIEBRE_DE_STOCK = float(
    input("Ingrese el costo de quiebre de stock (b): "))
PLANTAS = [(3, 2, "Normal", (4000, 200)),
           (7, 5, "Normal", (5000, 300)),
           (4, 8, "Triangualar", (4000, 5500, 7000))]
X_MAX_MAPA = 10
Y_MAX_MAPA = 10
