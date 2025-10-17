# README — Segundo Parcial de Paradigmas de Programación

Este proyecto contiene las soluciones completas para los puntos del **Segundo Parcial** de la asignatura **Paradigmas de Programación**.  
Cada punto aplica un paradigma distinto y puede ejecutarse de manera independiente.

---

##  Punto 1 — Perceptrón con Agentes (Mesa)
**Descripción:**  
Simula el aprendizaje de un perceptrón simple usando el paradigma de agentes.  
El modelo genera puntos linealmente separables y muestra en tiempo real cómo el perceptrón ajusta sus pesos y su línea de decisión.

**Ejecución:**
1. Instalar la versión recomendada de Mesa:
   ```bash
   pip install "mesa[visualization]==2.1.4"
   ```
2. Ejecutar:
   ```bash
   python simulacion_mesa.py
   ```
3. Abrir el navegador en:  
   [http://127.0.0.1:8521](http://127.0.0.1:8521)

**Archivos principales:**
- `perceptron.py` — lógica del modelo de aprendizaje.  
- `generador.py` — genera los datos de entrenamiento.  
- `simulacion_mesa.py` — interfaz gráfica del simulador.

---

##  Punto 2 — Calculadora con Agentes (Mesa)
**Descripción:**  
Implementa una calculadora distribuida donde cada operación aritmética (suma, resta, multiplicación, división y potencia) es realizada por un agente independiente.  
El agente principal (IO) coordina la ejecución paso a paso utilizando notación postfija (RPN).

**Ejecución:**
1. Instalar la versión estable de Mesa:
   ```bash
   pip install "mesa[visualization]==2.1.4"
   ```
2. Ejecutar:
   ```bash
   python interfaz.py
   ```
3. Abrir el navegador en:  
   [http://127.0.0.1:8521](http://127.0.0.1:8521)

**Archivos principales:**
- `agentes_operaciones.py` — definición de los agentes de operación.  
- `modelo_calculadora.py` — modelo central y lógica de comunicación.  
- `interfaz.py` — visualización y control de simulación.

---

##  Punto 3 — Calculadora Científica en Kotlin (POO)
**Descripción:**  
Implementa una calculadora científica aplicando **herencia, polimorfismo, encapsulamiento, manejo de errores y memoria**.  
Se desarrolla en un solo archivo Kotlin.

**Ejecución:**
1. Abrir el archivo `CalculadoraCientifica.kt` en cualquier IDE compatible con Kotlin (IntelliJ o VS Code).  
2. Ejecutar el programa con:
   ```bash
   kotlinc CalculadoraCientifica.kt -include-runtime -d CalculadoraCientifica.jar
   java -jar CalculadoraCientifica.jar
   ```

**Archivo principal:**
- `CalculadoraCientifica.kt` — contiene todas las clases:  
  `Calculadora`, `CalculadoraCientifica`, `Memoria` y `ErrorManager`.

---

##  Requisitos generales
- Python 3.10 o superior.  
- Kotlin 1.9 o superior.  
- Librerías utilizadas:  
  - **Mesa 2.1.4** para los puntos 1 y 2.  
  - **kotlin.math** para el punto 3.

---
