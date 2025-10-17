# Diseño y justificación del perceptrón con agentes

## Objetivo
El propósito fue construir un **perceptrón simple** usando el entorno **Mesa** de Python para observar cómo este aprende a separar puntos en un plano.  
El modelo debía ajustar una **línea de decisión** que divide los puntos de dos clases distintas (por ejemplo, rojos y azules) según sus coordenadas.

---

## Cómo funciona el perceptrón
El perceptrón recibe dos valores de entrada (x e y) y tiene un peso para cada uno más un valor de **sesgo**.  
La combinación de estos tres números define una **línea** que intenta separar las dos clases.  
Cada punto se evalúa así:

\[
a = w_1x + w_2y + b
\]

Si el resultado `a` es positivo, el punto se clasifica como **+1**; si es negativo, como **-1**.  
Esto crea una frontera (la línea donde `a = 0`) que va ajustándose durante el entrenamiento.

---

## Aprendizaje
Cada vez que el perceptrón se equivoca, corrige sus pesos con la siguiente regla:

\[
w_i = w_i + tasa\_aprendizaje \times (objetivo - prediccion) \times entrada_i
\]

En palabras simples:
- Si el perceptrón acierta, no cambia nada.  
- Si falla, mueve los pesos un poco hacia la dirección correcta.  
- Qué tanto se mueve depende de la **tasa de aprendizaje** (un número entre 0 y 1).

---

## Diseño con agentes en Mesa
- **PerceptronAgent:** actualiza los pesos según los puntos de entrenamiento.  
- **PuntoAgent:** representa un punto con su clase (1 o -1) y se colorea verde si está bien clasificado, rojo si no.  
- **LineaPunto:** marca visualmente la línea de separación que va cambiando conforme el perceptrón aprende.

El modelo se ejecuta por **iteraciones**, cada una equivalente a una “época” de aprendizaje.  
En cada paso:
1. El perceptrón revisa todos los puntos y ajusta los pesos.  
2. Se redibuja la línea con los nuevos valores.  
3. Los puntos cambian de color según su clasificación actual.  
4. Se grafica el error total de esa época.

---

## Evaluación
Cuando termina el entrenamiento, se puede probar con nuevos puntos.  
Si la mayoría se clasifica bien, significa que el perceptrón **aprendió** la frontera entre las dos clases.

---

# Informe – Conclusiones

## Conclusiones
Durante las pruebas se comprobó que el perceptrón **aprende más rápido** cuando la **tasa de aprendizaje** es **alta**, y más lento cuando es baja.  
Sin embargo, una tasa demasiado alta puede causar que la línea “salte” de un lado a otro antes de estabilizarse.

- Con una **tasa baja** (por ejemplo 0.03):  
  El aprendizaje es **lento pero estable**. El error baja poco a poco, y la línea se va ajustando suavemente.  
  En el simulador, la mayoría de puntos tardan varias iteraciones en volverse verdes.

- Con una **tasa alta** (por ejemplo 0.6):  
  El error baja **rápido** en las primeras épocas. En pocas iteraciones, la línea encuentra una buena separación.  
  A veces al inicio oscila un poco, pero logra una clasificación correcta con menos pasos.

En resumen:
> Una tasa de aprendizaje **alta mejora la velocidad de entrenamiento**, mientras que una **baja da un proceso más lento pero estable**.  
> Lo ideal es encontrar un valor medio que combine **rapidez** sin perder **precisión**.

 