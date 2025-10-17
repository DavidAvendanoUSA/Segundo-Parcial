from dataclasses import dataclass
from typing import Tuple, Optional
from mesa import Agent


@dataclass
class Mensaje:
    """Mensaje simple de petición/respuesta."""
    tipo: str                 # 'request' o 'response'
    operacion: str            # suma, resta, multiplicacion, division, potencia
    operandos: Tuple[float, float] | None = None
    resultado: Optional[float] = None
    emisor: Optional[int] = None
    receptor: Optional[int] = None


class OperacionAgente(Agent):
    """Agente base para operaciones binarias."""
    nombre_operacion = "operacion"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.activo = False  # para resaltar cuando está procesando

    def calcular(self, a: float, b: float) -> float:
        raise NotImplementedError

    def step(self):
        self.activo = False
        # Consumir a lo sumo un mensaje por tick para que la animación sea clara
        msg = self.model.recibir_mensaje(self.unique_id, esperado=self.nombre_operacion)
        if msg is None:
            return
        a, b = msg.operandos
        self.activo = True
        if self.nombre_operacion == "division" and b == 0:
            raise ZeroDivisionError("División por cero")
        r = self.calcular(a, b)
        # Responder al emisor (el IO)
        respuesta = Mensaje(
            tipo="response",
            operacion=self.nombre_operacion,
            resultado=r,
            emisor=self.unique_id,
            receptor=msg.emisor
        )
        self.model.enviar_mensaje(respuesta)


class AgenteSuma(OperacionAgente):
    nombre_operacion = "suma"
    def calcular(self, a, b): return a + b


class AgenteResta(OperacionAgente):
    nombre_operacion = "resta"
    def calcular(self, a, b): return a - b


class AgenteMultiplicacion(OperacionAgente):
    nombre_operacion = "multiplicacion"
    def calcular(self, a, b): return a * b


class AgenteDivision(OperacionAgente):
    nombre_operacion = "division"
    def calcular(self, a, b): return a / b


class AgentePotencia(OperacionAgente):
    nombre_operacion = "potencia"
    def calcular(self, a, b): return a ** b
