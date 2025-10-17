# Calculadora Científica en Kotlin — Diseño, Justificación e Informe Final

## Introducción
Este proyecto consiste en una **calculadora científica desarrollada en Kotlin**, que aplica los principios de la **Programación Orientada a Objetos (POO)**.  
El objetivo es demostrar el uso de **herencia, polimorfismo, encapsulamiento, manejo de errores y memoria**, todo dentro de un solo archivo funcional.

---

## Diseño del sistema

### 1. Clase `Calculadora`
Es la **clase base** del sistema. Contiene las operaciones aritméticas esenciales:
- `sumar(a, b)`
- `restar(a, b)`
- `multiplicar(a, b)`
- `dividir(a, b)`

Implementa **sobrecarga de métodos** (polimorfismo en tiempo de compilación), permitiendo trabajar con `Int` y `Double`.  
También usa `require()` para validar que no se divida entre cero, aplicando **encapsulamiento** al controlar internamente los errores de operación.

---

### 2. Clase `CalculadoraCientifica`
Hereda de `Calculadora` y amplía sus funcionalidades con métodos científicos:
- **Potencia y raíz:** `potencia()`, `raiz()`
- **Trigonometría:** `seno()`, `coseno()`, `tangente()` (en grados)
- **Logaritmos y exponenciales:** `logBase10()`, `logBaseE()`, `exponencial()`
- **Conversión angular:** `gradosARadianes()` y `radianesAGrados()`

Además, **sobrescribe el método `dividir()`**, lanzando un mensaje personalizado cuando ocurre una división por cero.  
Esto demuestra **polimorfismo en tiempo de ejecución**, ya que redefine el comportamiento de la clase padre.

---

### 3. Clase `Memoria`
Implementa las funciones clásicas de las calculadoras físicas:
- `mPlus(x)` → suma un valor a la memoria.  
- `mMinus(x)` → resta un valor.  
- `mr()` → muestra el valor almacenado.  
- `mc()` → borra la memoria.

La memoria se mantiene **encapsulada** dentro de la clase y solo puede modificarse mediante sus propios métodos, evitando errores o manipulaciones externas.

---

### 4. Clase `ErrorManager` y `CalcOutcome`
Maneja las excepciones y devuelve resultados seguros sin interrumpir el programa:
- Si una operación se realiza correctamente, devuelve `Success(valor)`.  
- Si ocurre un error (por ejemplo, raíz de un número negativo o logaritmo de cero), devuelve `Failure(mensaje)`.

Esto implementa un **manejo de errores controlado y predecible**, útil para mantener la estabilidad del sistema.

---

## Funcionamiento general
1. El programa crea un objeto de `CalculadoraCientifica` junto con `Memoria` y `ErrorManager`.
2. Ejecuta operaciones básicas y avanzadas mostrando resultados paso a paso.
3. Los errores se manejan mediante `ErrorManager.safe { ... }`, sin detener el programa.
4. La memoria guarda y recupera valores correctamente.

---

## Ejemplo de flujo completo

1. **Operaciones básicas**
   - `sumar(5, 3)` → devuelve `8`  
   - `dividir(9.0, 3.0)` → devuelve `3.0`  

2. **Manejo de error**
   - `dividir(9.0, 0.0)` → produce `Error aritmético: División por cero.`  
   - `logBase10(-2.0)` → produce `Entrada inválida: log10(x) requiere x>0.`  

3. **Operaciones científicas**
   - `potencia(2, 4)` → `16.0`  
   - `raiz(16)` → `4.0`  
   - `seno(30°)` → `0.5`  
   - `ln(e)` → `1.0`  

4. **Memoria**
   - `mPlus(10.0)` → memoria = `10.0`  
   - `mPlus(2.5)` → memoria = `12.5`  
   - `mMinus(1.5)` → memoria = `11.0`  
   - `mr()` → muestra `11.0`  
   - `mc()` → borra memoria, vuelve a `0.0`

5. **Manejo controlado**
   - `ErrorManager.safe { calc.raiz(-16.0) }` → devuelve `"Error: Raíz par de número negativo."`  
   - `ErrorManager.safe { calc.dividir(10.0, 0.0) }` → devuelve `"Error aritmético: División por cero."`

---

## Conclusiones

- La calculadora demuestra **herencia** al extender la clase base `Calculadora` con nuevas funciones en `CalculadoraCientifica`.
- Muestra **polimorfismo** mediante:
  - Sobrecarga de métodos (`sumar()` con distintos tipos).
  - Sobrescritura (`dividir()` redefine el comportamiento original).
- La **clase Memoria** encapsula su propio estado y simula funciones reales de calculadora (M+, M-, MR, MC).
- La **clase ErrorManager** evita bloqueos y hace que el código sea más estable y seguro.
- El sistema es **modular, ampliable y robusto**, fácil de mantener y escalar con nuevas funciones (como trigonometría inversa o constantes científicas).
- Se demuestra que una arquitectura orientada a objetos bien estructurada **facilita la organización, legibilidad y reusabilidad del código**.

---

## Conclusión general
La implementación cumple completamente los principios de la **Programación Orientada a Objetos**:
- **Herencia** → CalculadoraCientifica amplía Calculadora.  
- **Polimorfismo** → Sobrecarga y sobrescritura de métodos.  
- **Encapsulamiento** → Clases con control interno de datos y validaciones.  
- **Abstracción** → Cada clase cumple un rol definido.  
- **Manejo de errores y memoria** → Control confiable y funcional.  

En resumen, el programa es un ejemplo completo y funcional de cómo aplicar los conceptos fundamentales de la POO en Kotlin para construir una calculadora científica estable y bien diseñada.