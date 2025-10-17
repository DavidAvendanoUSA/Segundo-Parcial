import random

class PerceptronAgent:
    def __init__(self, n_inputs=2, tasa_aprendizaje=0.1, iteraciones=100):
        """
        Crea un perceptrón con pesos aleatorios, tasa de aprendizaje y número de iteraciones.
        """
        # +1 para el sesgo (bias)
        self.pesos = [random.uniform(-1, 1) for _ in range(n_inputs + 1)]
        self.tasa = tasa_aprendizaje
        self.iteraciones = iteraciones
        
    def predecir(self, entradas):
        """
        Calcula la salida del perceptrón para una lista de entradas.
        """
        # Agregamos el bias
        entradas = entradas + [1]
        suma = sum(w * x for w, x in zip(self.pesos, entradas))
        # Función de activación: signo
        return 1 if suma >= 0 else -1

    def entrenar(self, datos):
        error_total = 0
        for punto in datos:
            # 👇 Obtenemos todas las coordenadas excepto la última (etiqueta)
            entradas = punto[:-1]  # [x, y]
            etiqueta = punto[-1]   # etiqueta (1 o -1)
            
            prediccion = self.predecir(entradas)
            error = etiqueta - prediccion
            error_total += abs(error)

            # Actualizar pesos (incluyendo bias)
            for i in range(len(self.pesos)):
                # 👇 El último peso es el bias (siempre se multiplica por 1)
                entrada = entradas[i] if i < len(entradas) else 1
                self.pesos[i] += self.tasa * error * entrada

        return error_total