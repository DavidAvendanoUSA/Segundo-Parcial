# interfaz.py — versión mínima, estable y sin UserParam
# Cambia la expresión aquí:
DEFAULT_EXPR = "2 + 3 * 4 - 5"

# Imports básicos y estables en Mesa 2.x
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, TextElement

from modelo_calculadora import CalculadoraAgentesModel, portrayal


class EstadoTexto(TextElement):
    def render(self, model):
        io = model.io
        lines = [
            f"<b>Expr:</b> {io.expr}",
            f"<b>RPN:</b> {' '.join(io.rpn) if io.rpn else '(pendiente)'}",
            f"<b>Stack:</b> {io.stack}",
            f"<b>Último:</b> {io.ultimo_mensaje or '(—)'}",
        ]
        if io.resultado_final is not None:
            lines.append(f"<b>Resultado:</b> {io.resultado_final}")
        if io.error:
            lines.append(f"<b>Error:</b> {io.error}")
        return "<br>".join(lines)


def lanzar():
    grid = CanvasGrid(portrayal, 7, 3, 700, 300)

    # Modelo sin parámetros de UI: usa la constante DEFAULT_EXPR
    def make_model():
        return CalculadoraAgentesModel(expresion=DEFAULT_EXPR)

    server = ModularServer(
        make_model,
        [grid, EstadoTexto()],
        "Calculadora por Agentes (mínima y estable)",
        {}
    )
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    lanzar()