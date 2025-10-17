# simulacion_mesa.py
# --------------------------------------------------------
# Simulación del Perceptrón como agente usando Mesa.
# --------------------------------------------------------

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from mesa.datacollection import DataCollector
from generador import generar_puntos
import random
import numpy as np

# --------------------------------------------------------
# 1️⃣ Perceptrón "dentro" de Mesa (entrenamiento)
# --------------------------------------------------------
class PerceptronAgent(Agent):
    def __init__(self, unique_id, model, n_inputs=2, tasa_aprendizaje=0.1):
        super().__init__(unique_id, model)
        self.pesos = np.random.rand(n_inputs + 1)  # +1 bias
        self.tasa_aprendizaje = tasa_aprendizaje
        self.errores = []

    def predict(self, inputs):
        inputs_con_bias = np.append(inputs, 1)
        suma = np.dot(self.pesos, inputs_con_bias)
        return 1 if suma >= 0 else -1

    def entrenar(self, datos_entrenamiento):
        error_total = 0
        for inputs, objetivo in datos_entrenamiento:
            prediccion = self.predict(inputs)
            error = objetivo - prediccion
            error_total += abs(error)
            inputs_con_bias = np.append(inputs, 1)
            self.pesos += self.tasa_aprendizaje * error * inputs_con_bias

        self.errores.append(error_total)
        return error_total

    def step(self):
        pass

# --------------------------------------------------------
#  Línea de decisión: agentes "punto de línea"
# --------------------------------------------------------
class LineaPunto(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

# --------------------------------------------------------
# 2️⃣ Agentes visuales (puntos de datos)
# --------------------------------------------------------
class PuntoAgent(Agent):
    def __init__(self, unique_id, model, clase):
        super().__init__(unique_id, model)
        self.clase = clase
        self.correcto = None

    def step(self):
        perceptron = self.model.perceptron
        inputs = np.array(self.pos)
        prediccion = perceptron.predict(inputs)
        self.correcto = (prediccion == self.clase)

# --------------------------------------------------------
# 3️⃣ Modelo de simulación
# --------------------------------------------------------
class Simulacion(Model):
    def __init__(self, cantidad_por_clase=10, tasa=0.1, iteraciones=10):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(20, 20, True)
        self.iteraciones = iteraciones
        self.tasa = tasa
        self.cantidad_por_clase = cantidad_por_clase
        self.current_step = 0
        self.running = True

        # Perceptrón "entrenador"
        self.perceptron = PerceptronAgent("perceptron", self, tasa_aprendizaje=tasa)
        self.schedule.add(self.perceptron)

        # Puntos de datos
        self.crear_entorno()

        # Data collector
        self.error_actual = 0
        self.datacollector = DataCollector(
            model_reporters={"Error": "error_actual"}
        )

        # Para controlar los agentes de la línea
        self._line_agents_ids = set()
        self._next_line_id = 100000  # id alto para no chocar con puntos

    def crear_entorno(self):
        puntos = generar_puntos(self.cantidad_por_clase, rango_x=(0, 19), rango_y=(0, 19), ruido=0.0)
        for i, (x, y, clase) in enumerate(puntos):
            agente = PuntoAgent(i, self, clase)
            x_pos = max(0, min(self.grid.width - 1, int(round(x))))
            y_pos = max(0, min(self.grid.height - 1, int(round(y))))
            self.grid.place_agent(agente, (x_pos, y_pos))
            self.schedule.add(agente)
        self.preparar_datos_entrenamiento()

    def preparar_datos_entrenamiento(self):
        self.datos_entrenamiento = []
        for agent in self.schedule.agents:
            if isinstance(agent, PuntoAgent):
                x, y = agent.pos
                inputs = np.array([x, y])
                objetivo = agent.clase
                self.datos_entrenamiento.append((inputs, objetivo))
        random.shuffle(self.datos_entrenamiento)

    # ---- helpers para la línea ----
    def _coords_linea_decision(self):
        coords = []
        w1, w2, b = self.perceptron.pesos
        if abs(w2) < 1e-9:
            return coords  # evito división por cero
        for x in range(self.grid.width):
            y = int(round((-w1 * x - b) / w2))
            if 0 <= y < self.grid.height:
                coords.append((x, y))
        return coords

    def _limpiar_linea(self):
        # Eliminar agentes de línea existentes
        to_remove = []
        for ag in list(self.schedule.agents):
            if isinstance(ag, LineaPunto):
                to_remove.append(ag)
        for ag in to_remove:
            # sacar del grid y del scheduler
            for cell in list(self.grid.coord_iter()):
                cell_content, x, y = cell
                if ag in cell_content:
                    self.grid.remove_agent(ag)
                    break
            self.schedule.remove(ag)
        self._line_agents_ids.clear()

    def _dibujar_linea(self):
        self._limpiar_linea()
        for (x, y) in self._coords_linea_decision():
            lp = LineaPunto(self._next_line_id, self)
            self._next_line_id += 1
            self.grid.place_agent(lp, (x, y))
            self.schedule.add(lp)
            self._line_agents_ids.add(lp.unique_id)

    def step(self):
        if self.current_step < self.iteraciones:
            # Entrenar
            error_total = self.perceptron.entrenar(self.datos_entrenamiento)
            self.error_actual = error_total
            self.datacollector.collect(self)

            # Redibujar la línea de decisión
            self._dibujar_linea()

            # Actualizar colores de puntos (y otros agentes visuales) en el tick
            self.schedule.step()

            self.current_step += 1
        else:
            self.running = False

# --------------------------------------------------------
# 4️⃣ Visualización
# --------------------------------------------------------
def agente_portrayer(agent):
    if agent is None:
        return
    portrayal = {"Filled": "true"}

    if isinstance(agent, PuntoAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        if agent.correcto is None:
            color = "gray"
        elif agent.correcto:
            color = "green"
        else:
            color = "red"
        portrayal["Color"] = color
        portrayal["Layer"] = 0

    elif isinstance(agent, PerceptronAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3

    elif isinstance(agent, LineaPunto):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 0.1

    return portrayal

# --------------------------------------------------------
# 5️⃣ Configuración de la visualización
# --------------------------------------------------------
def ejecutar_visualizacion():
    grid = CanvasGrid(agente_portrayer, 20, 20, 500, 500)
    chart = ChartModule(
        [{"Label": "Error", "Color": "red"}],
        data_collector_name='datacollector'
    )

    model_params = {
        "cantidad_por_clase": Slider("Número de puntos por clase", 10, 5, 50, 1),
        "tasa": Slider("Tasa de aprendizaje", 0.1, 0.01, 1.0, 0.01),
        "iteraciones": Slider("Iteraciones de entrenamiento", 10, 1, 100, 1)
    }

    server = ModularServer(
        Simulacion,
        [grid, chart],
        "Simulación Perceptrón con Mesa",
        model_params
    )
    server.port = 8521
    server.launch()

if __name__ == "__main__":
    ejecutar_visualizacion()

