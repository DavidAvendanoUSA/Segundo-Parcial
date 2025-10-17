import kotlin.math.*

sealed class CalcOutcome {
    data class Success(val value: Double) : CalcOutcome()
    data class Failure(val message: String) : CalcOutcome()
}

class ErrorManager {
    inline fun safe(block: () -> Double): CalcOutcome =
        try { CalcOutcome.Success(block()) }
        catch (e: IllegalArgumentException) { CalcOutcome.Failure("Entrada inválida: ${e.message}") }
        catch (e: ArithmeticException) { CalcOutcome.Failure("Error aritmético: ${e.message}") }
        catch (e: Exception) { CalcOutcome.Failure("Error: ${e.message}") }
}

class Memoria {
    private var memoria: Double = 0.0
    fun mPlus(x: Double) { memoria += x }
    fun mMinus(x: Double) { memoria -= x }
    fun mr(): Double = memoria
    fun mc() { memoria = 0.0 }
}

open class Calculadora {
    open fun sumar(a: Double, b: Double): Double = a + b
    fun sumar(a: Int, b: Int): Int = a + b
    open fun restar(a: Double, b: Double): Double = a - b
    fun restar(a: Int, b: Int): Int = a - b
    open fun multiplicar(a: Double, b: Double): Double = a * b
    fun multiplicar(a: Int, b: Int): Int = a * b
    open fun dividir(a: Double, b: Double): Double {
        require(b != 0.0) { "No se puede dividir entre cero." }
        return a / b
    }
}

class CalculadoraCientifica : Calculadora() {
    override fun dividir(a: Double, b: Double): Double {
        if (b == 0.0) throw ArithmeticException("División por cero.")
        return super.dividir(a, b)
    }

    fun potencia(base: Double, exp: Double): Double = base.pow(exp)

    fun raiz(numero: Double, indice: Double = 2.0): Double {
        require(indice != 0.0) { "El índice de la raíz no puede ser 0." }
        if (numero < 0 && indice % 2.0 == 0.0) throw IllegalArgumentException("Raíz par de número negativo.")
        return numero.pow(1.0 / indice)
    }

    fun evaluarExpresion(expresion: String): Double {
        val tokens = tokenizar(expresion)
        return evaluarTokens(tokens)
    }

    private fun tokenizar(expresion: String): List<String> {
        val regex = Regex("([+\\-*/^()])|(sin|cos|tan|log|ln|sqrt)|([0-9]+\\.?[0-9]*)")
        return regex.findAll(expresion.replace(" ", ""))
            .map { it.value }
            .toList()
    }

    private fun evaluarTokens(tokens: List<String>): Double {
        val numeros = ArrayDeque<Double>()
        val operadores = ArrayDeque<String>()

        for (token in tokens) {
            when {
                token.matches(Regex("[0-9]+\\.?[0-9]*")) -> numeros.addLast(token.toDouble())
                token == "(" -> operadores.addLast(token)
                token == ")" -> {
                    while (operadores.isNotEmpty() && operadores.last() != "(") {
                        aplicarOperador(operadores.removeLast(), numeros)
                    }
                    operadores.removeLast()
                    if (operadores.isNotEmpty() && operadores.last().matches(Regex("sin|cos|tan|log|ln|sqrt"))) {
                        aplicarFuncion(operadores.removeLast(), numeros)
                    }
                }
                token.matches(Regex("sin|cos|tan|log|ln|sqrt")) -> operadores.addLast(token)
                else -> {
                    while (operadores.isNotEmpty() && prioridad(operadores.last()) >= prioridad(token)) {
                        aplicarOperador(operadores.removeLast(), numeros)
                    }
                    operadores.addLast(token)
                }
            }
        }

        while (operadores.isNotEmpty()) {
            aplicarOperador(operadores.removeLast(), numeros)
        }

        return numeros.removeLast()
    }

    private fun prioridad(operador: String): Int = when (operador) {
        "+", "-" -> 1
        "*", "/" -> 2
        "^" -> 3
        "sin", "cos", "tan", "log", "ln", "sqrt" -> 4
        else -> 0
    }

    private fun aplicarOperador(operador: String, numeros: ArrayDeque<Double>) {
        val b = numeros.removeLast()
        val a = numeros.removeLast()
        val resultado = when (operador) {
            "+" -> sumar(a, b)
            "-" -> restar(a, b)
            "*" -> multiplicar(a, b)
            "/" -> dividir(a, b)
            "^" -> potencia(a, b)
            else -> throw IllegalArgumentException("Operador desconocido: $operador")
        }
        numeros.addLast(resultado)
    }

    private fun aplicarFuncion(funcion: String, numeros: ArrayDeque<Double>) {
        val a = numeros.removeLast()
        val resultado = when (funcion) {
            "sin" -> sin(a * PI / 180)
            "cos" -> cos(a * PI / 180)
            "tan" -> tan(a * PI / 180)
            "log" -> log10(a)
            "ln" -> ln(a)
            "sqrt" -> raiz(a)
            else -> throw IllegalArgumentException("Función desconocida: $funcion")
        }
        numeros.addLast(resultado)
    }
}

fun main() {
    val calculadora = CalculadoraCientifica()
    println("Calculadora Científica - Ingrese expresiones matemáticas")
    println("Ejemplos: 2 + 3 * sin(45) - log(10)")
    println("Funciones: sin, cos, tan, log, ln, sqrt")
    println("Escriba 'salir' para terminar")

    while (true) {
        print("> ")
        val input = readLine()?.trim()

        when {
            input == null -> continue
            input.equals("salir", ignoreCase = true) -> break
            input.isEmpty() -> continue
            else -> {
                try {
                    val resultado = calculadora.evaluarExpresion(input)
                    println("Resultado: $resultado")
                } catch (e: Exception) {
                    println("Error: ${e.message}")
                }
            }
        }
    }
}