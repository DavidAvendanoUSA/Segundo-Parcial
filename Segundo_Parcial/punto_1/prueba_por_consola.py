from generador import generar_puntos
from perceptron import PerceptronAgent
import random

# Generar puntos (lista mezclada con [x, y, etiqueta])
puntos = generar_puntos(10)

# Separar por etiqueta para imprimir bonitos
rojos = [p for p in puntos if p[2] == 1]
azules = [p for p in puntos if p[2] == -1]

random.shuffle(puntos)

print("puntos rojos:")
for p in rojos:
    print(p)

print("\npuntos azules:")
for p in azules:
    print(p)

print("\nmezclados:")
for p in puntos:
    print(p)

# Crear perceptrón "puro" (no Mesa)
print("\nentrenando perceptron...\n")
n = PerceptronAgent(2, 0.1, 10)

for i in range(n.iteraciones):
    err = n.entrenar(puntos)
    print("iteracion", i+1, "error total:", err)

print("\npesos finales:")
print(n.pesos)

# Probar punto manual
print("\nprobar punto nuevo:")
x = float(input("x: "))
y = float(input("y: "))
r = n.predecir([x, y])
print("resultado:", r)

# Evaluación simple sobre los datos originales
print("\nverificacion:")
aciertos = 0
for p in puntos:
    pred = n.predecir([p[0], p[1]])
    real = p[2]
    if pred == real:
        aciertos += 1
    print(p, "->", pred, "(ok)" if pred == real else "(x)")

accuracy = aciertos / len(puntos) * 100
print(f"\nAccuracy sobre los datos de entrenamiento: {accuracy:.2f}%")

