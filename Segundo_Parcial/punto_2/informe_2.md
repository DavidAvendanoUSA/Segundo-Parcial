# Diseño y justificación – Calculadora con Agentes

## Objetivo
El objetivo de este proyecto es crear una calculadora que funcione mediante agentes.  
Cada agente realiza una operación específica como suma, resta, multiplicación, división o potencia, mientras que un agente principal (IO) coordina el proceso de cálculo paso a paso.

---

## Estructura del sistema

### Agente IO (Entrada/Salida)
El agente IO recibe una expresión matemática escrita en forma normal, por ejemplo `2 + 3 * 4 - 5`.  
Convierte la expresión a **notación postfija (RPN)** para respetar la precedencia de las operaciones.  
Luego lee cada elemento de la expresión uno por uno:
- Si el elemento es un número, lo guarda en una pila.
- Si el elemento es un operador, envía un mensaje al agente correspondiente para que realice la operación.  
Cuando todos los elementos se procesan, el IO muestra el resultado final.

### Agentes de operación
Cada agente representa una operación aritmética y solo realiza su función:
- El agente Suma suma dos números.
- El agente Resta resta el segundo número del primero.
- El agente Multiplicación multiplica ambos valores.
- El agente División realiza la división y detecta si se intenta dividir entre cero.
- El agente Potencia eleva un número a otro.

Cada agente espera recibir un mensaje del agente IO con los valores que debe procesar, ejecuta su cálculo y devuelve el resultado.

### Comunicación
La comunicación entre agentes se realiza por medio de mensajes simples.  
Cada mensaje contiene el tipo de operación, los valores y los identificadores del emisor y del receptor.  
Este intercambio simula cómo los agentes colaboran entre sí para resolver la expresión completa.

### Visualización
El sistema muestra los agentes en una grilla.  
El agente IO se ubica a la izquierda y los agentes de operación a la derecha.  
Durante la simulación, los agentes que están activos se iluminan para indicar que están trabajando.  
En el panel lateral se pueden observar:
- La expresión actual.
- La versión convertida a RPN.
- El contenido de la pila.
- El último mensaje enviado.
- El resultado final.

---

## Funcionamiento del proceso
Ejemplo: `2 + 3 * 4 - 5`  
RPN equivalente: `2 3 4 * + 5 -`

1. El agente IO coloca los valores `2`, `3` y `4` en la pila.  
2. Envía un mensaje al agente de Multiplicación, que calcula `3 * 4 = 12` y devuelve el resultado.  
3. El IO apila el resultado y solicita al agente Suma calcular `2 + 12 = 14`.  
4. Luego apila el número `5` y pide al agente Resta calcular `14 - 5 = 9`.  
5. El agente IO muestra el resultado final, que es **9**.

---

## Conclusiones
El modelo basado en agentes permite observar claramente cómo cada operación se ejecuta de forma independiente.  
El agente IO coordina la secuencia de pasos y garantiza que la expresión se resuelva respetando la precedencia de las operaciones.  
El uso de notación postfija simplifica la evaluación y evita errores por orden de ejecución.  
El sistema también puede detectar errores como divisiones por cero o expresiones incompletas.  
El proceso es visual, entendible y demuestra cómo los agentes pueden cooperar para resolver un problema matemático complejo.

---

## Resultados demostrativos
Expresión 1: `2 + 3 * 4 - 5` → Resultado: **9**  
Expresión 2: `-3 + 5 * 2 ^ 3` → Resultado: **37**  
En ambas expresiones se verifica el orden correcto de las operaciones: primero potencias, luego multiplicaciones y divisiones, y finalmente sumas y restas.  
Esto confirma el correcto funcionamiento del modelo basado en agentes.