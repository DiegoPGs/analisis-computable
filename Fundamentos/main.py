from decimal import Decimal, getcontext
from typing import Callable

class ComputableNumber:
    def __init__(self, approximation_function: Callable[[int], Decimal]):
        """
        Inicializa un número computable con una función de aproximación
        
        Args:
            approximation_function: Una función que toma un nivel de precisión n
            y retorna una aproximación con error < 2^(-n)
        """
        self.approximation_function = approximation_function
        
    def approximate(self, precision: int) -> Decimal:
        """
        Calcula una aproximación del número con la precisión dada
        
        Args:
            precision: Número de bits de precisión requeridos
        
        Returns:
            Una aproximación decimal con error < 2^(-precision)
        """
        getcontext().prec = precision + 10  # Extra precisión para cálculos internos
        return self.approximation_function(precision)

# Ejemplo: Definición de π como número computable
def pi_approximation(precision: int) -> Decimal:
    """
    Implementación del algoritmo de Chudnovsky para aproximar π
    """
    # Configurar la precisión interna
    getcontext().prec = precision + 10
    C = 426880 * Decimal(10005).sqrt()
    L = 13591409
    X = 1
    M = 1
    K = 6
    S = L
    for i in range(1, precision):
        M = M * (K ** 3 - 16 * K) // (i ** 3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12
    pi = C / S
    return +pi  # Normaliza el resultado a la precisión actual

# Crear una instancia de π como número computable
pi = ComputableNumber(pi_approximation)

# Ejemplo de uso
if __name__ == "__main__":
    print(f"π con 10 decimales: {pi.approximate(10)}")
    print(f"π con 50 decimales: {pi.approximate(50)}")