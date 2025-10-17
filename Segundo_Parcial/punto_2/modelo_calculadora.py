import re
from typing import List, Dict, Optional
from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agentes_operaciones import (
    Mensaje,
    AgenteSuma, AgenteResta, AgenteMultiplicacion, AgenteDivision, AgentePotencia
)

# ---------- Parser (tokens -> RPN con Shunting Yard) ----------
NUM_RE = r"-?\d+(?:\.\d+)?"

class Parser:
    PRE = {'+':1,'-':1,'*':2,'/':2,'^':3}
    RIGHT = {'^'}
    TOK = re.compile(rf"\s*(?:({NUM_RE})|([+\-*/^()]))")

    def tokens(self, expr: str) -> List[str]:
        out, i = [], 0
        while i < len(expr):
            m = self.TOK.match(expr, i)
            if not m: raise ValueError(f"Token no reconocido cerca de: {expr[i:]}")
            num, sym = m.groups()
            out.append(num if num is not None else sym)
            i = m.end()
        return out

    def a_rpn(self, toks: List[str]) -> List[str]:
        out, st = [], []
        for t in toks:
            if re.fullmatch(NUM_RE, t):
                out.append(t)
            elif t in self.PRE:
                while st and st[-1] in self.PRE:
                    top = st[-1]
                    if ((top not in self.RIGHT and self.PRE[top] >= self.PRE[t]) or
                        (top in self.RIGHT and self.PRE[top] > self.PRE[t])):
                        out.append(st.pop())
                    else:
                        break
                st.append(t)
            elif t == '(':
                st.append(t)
            elif t == ')':
                while st and st[-1] != '(':
                    out.append(st.pop())
                if not st: raise ValueError("Paréntesis desbalanceados")
                st.pop()
            else:
                raise ValueError(f"Token inesperado: {t}")
        while st:
            top = st.pop()
            if top in '()': raise ValueError("Paréntesis desbalanceados")
            out.append(top)
        return out


# ---------- Agente IO ----------
class AgenteIO(Agent):
    """Convierte la expresión a RPN y la evalúa paso a paso."""
    def __init__(self, unique_id, model, expr: str):
        super().__init__(unique_id, model)
        self.parser = Parser()
        self.expr = expr
        self.rpn: List[str] = []
        self.i = 0
        self.stack: List[float] = []
        self.esperando = False
        self.operador_en_curso: Optional[str] = None
        self.ultimo_mensaje: str = ""
        self.resultado_final: Optional[float] = None
        self.error: Optional[str] = None

    def reiniciar_expr(self, expr: str):
        self.__init__(self.unique_id, self.model, expr)

    def _op_to_agent_name(self, t: str) -> str:
        return {'+':'suma','-':'resta','*':'multiplicacion','/':'division','^':'potencia'}[t]

    def step(self):
        if self.error or self.resultado_final is not None:
            return

        try:
            if not self.rpn:
                toks = self.parser.tokens(self.expr)
                self.rpn = self.parser.a_rpn(toks)
                self.i = 0
                self.ultimo_mensaje = f"RPN: {' '.join(self.rpn)}"

            if self.esperando:
                resp = self.model.recibir_mensaje(self.unique_id, esperado=self.operador_en_curso, tipo='response')
                if resp:
                    self.stack.append(resp.resultado)
                    self.esperando = False
                    self.operador_en_curso = None
                    self.ultimo_mensaje = f"Respuesta {resp.operacion}: {resp.resultado}"
                return

            if self.i >= len(self.rpn):
                if len(self.stack) == 1:
                    self.resultado_final = self.stack[-1]
                    self.ultimo_mensaje = f"Resultado = {self.resultado_final}"
                else:
                    self.error = "Expresión inválida"
                return

            t = self.rpn[self.i]
            self.i += 1

            if re.fullmatch(NUM_RE, t):
                self.stack.append(float(t))
                self.ultimo_mensaje = f"Apilar número {t}"
                return

            if len(self.stack) < 2:
                self.error = "Faltan operandos"
                return

            b = self.stack.pop()
            a = self.stack.pop()
            agente_op = self._op_to_agent_name(t)

            req = Mensaje(
                tipo="request",
                operacion=agente_op,
                operandos=(a, b),
                emisor=self.unique_id,
                receptor=self.model.obtener_id_agente(agente_op)
            )
            self.model.enviar_mensaje(req)
            self.esperando = True
            self.operador_en_curso = agente_op
            self.ultimo_mensaje = f"Solicitar {agente_op}({a}, {b})"

        except Exception as e:
            self.error = str(e)


# ---------- Modelo Mesa ----------
class CalculadoraAgentesModel(Model):
    def __init__(self, expresion: str = "2 + 3 * 4 - 5"):
        super().__init__()
        self.running = True
        self.grid = MultiGrid(7, 3, torus=False)
        self.schedule = SimultaneousActivation(self)
        self._mensajes: List[Mensaje] = []

        self.io = AgenteIO(1, self, expresion)
        self.schedule.add(self.io)
        self.grid.place_agent(self.io, (1, 1))

        self.agentes_ops: Dict[str, Agent] = {}
        def add(op_cls, uid, pos, key):
            ag = op_cls(uid, self)
            self.schedule.add(ag)
            self.grid.place_agent(ag, pos)
            self.agentes_ops[key] = ag

        add(AgenteSuma, 2, (3, 2), 'suma')
        add(AgenteResta, 3, (3, 0), 'resta')
        add(AgenteMultiplicacion, 4, (4, 2), 'multiplicacion')
        add(AgenteDivision, 5, (4, 0), 'division')
        add(AgentePotencia, 6, (5, 1), 'potencia')

        self.datacollector = DataCollector(
            model_reporters={
                "StackSize": lambda m: len(m.io.stack),
                "Hecho": lambda m: 1 if m.io.resultado_final is not None else 0
            }
        )

    def enviar_mensaje(self, msg: Mensaje):
        self._mensajes.append(msg)

    def recibir_mensaje(self, receptor_id: int, esperado: Optional[str] = None, tipo: Optional[str] = None):
        for i, m in enumerate(self._mensajes):
            if m.receptor == receptor_id and (esperado is None or m.operacion == esperado) and (tipo is None or m.tipo == tipo):
                return self._mensajes.pop(i)
        return None

    def obtener_id_agente(self, nombre_op: str) -> int:
        return self.agentes_ops[nombre_op].unique_id

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        if self.io.resultado_final is not None or self.io.error is not None:
            self.running = False


# ---------- Visualización ----------
def portrayal(agent):
    if agent is None:
        return
    if isinstance(agent, AgenteIO):
        return {
            "Shape": "circle", "Color": "#1f78b4", "Filled": "true",
            "r": 0.8, "Layer": 1, "text": "IO", "text_color": "white"
        }
    color = "#33a02c"
    label = "?"
    activo = getattr(agent, "activo", False)
    if agent.nombre_operacion == "suma": label = "+"
    elif agent.nombre_operacion == "resta": label = "-"
    elif agent.nombre_operacion == "multiplicacion": label = "×"
    elif agent.nombre_operacion == "division": label = "÷"
    elif agent.nombre_operacion == "potencia": label = "^"
    return {
        "Shape": "rect", "Color": ("#ff7f00" if activo else color),
        "Filled": "true", "w": 0.9, "h": 0.9, "Layer": 0,
        "text": label, "text_color": "white"
    }

