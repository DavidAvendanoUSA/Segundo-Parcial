import random

# Variables globales para acceder luego desde otros módulos
puntos_rojos = []
puntos_azules = []

def generar_puntos(cantidad_por_clase=10, rango_x=(0, 10), rango_y=(0, 10), ruido=0.2):
    global puntos_rojos, puntos_azules
    puntos_rojos = []
    puntos_azules = []

    # Puntos rojos (+1)
    for _ in range(cantidad_por_clase):
        x = random.uniform(rango_x[0], rango_x[1])
        y = random.uniform((rango_y[1] / 2) + 1, rango_y[1])  # arriba
        x += random.uniform(-ruido, ruido)
        y += random.uniform(-ruido, ruido)
        puntos_rojos.append([x, y, 1])

    # Puntos azules (-1)
    for _ in range(cantidad_por_clase):
        x = random.uniform(rango_x[0], rango_x[1])
        y = random.uniform(rango_y[0], (rango_y[1] / 2) - 1)  # abajo
        x += random.uniform(-ruido, ruido)
        y += random.uniform(-ruido, ruido)
        puntos_azules.append([x, y, -1])

    puntos_totales = puntos_rojos + puntos_azules
    random.shuffle(puntos_totales)
    return puntos_totales
