from decimal import Decimal, getcontext
from typing import Callable, Union
import math

class ComputableReal:
    def __init__(self, value: Union[float, int, str, Callable[[int], Decimal]]):
        """
        Inicializa un número real computable
        
        Args:
            value: Puede ser un número directo o una función de aproximación
        """
        if callable(value):
            self.approximation = value
        else:
            decimal_value = Decimal(str(value))
            self.approximation = lambda p: decimal_value

    def __add__(self, other: 'ComputableReal') -> 'ComputableReal':
        return ComputableReal(
            lambda p: self.approximation(p + 1) + other.approximation(p + 1)
        )

    def __mul__(self, other: 'ComputableReal') -> 'ComputableReal':
        return ComputableReal(
            lambda p: self.approximation(p + 1) * other.approximation(p + 1)
        )

    def __truediv__(self, other: 'ComputableReal') -> 'ComputableReal':
        def divide_with_precision(p: int) -> Decimal:
            # Aumentamos la precisión para división
            getcontext().prec = p + 10
            numerator = self.approximation(p + 10)
            denominator = other.approximation(p + 10)
            if denominator == 0:
                raise ZeroDivisionError("División por cero")
            return numerator / denominator
        return ComputableReal(divide_with_precision)

    def to_decimal(self, precision: int) -> Decimal:
        """Obtiene aproximación con precisión específica"""
        getcontext().prec = precision
        return self.approximation(precision)

# Funciones matemáticas computables
def computable_sin(x: ComputableReal) -> ComputableReal:
    return ComputableReal(
        lambda p: Decimal(str(math.sin(float(x.to_decimal(p + 2)))))
    )

def computable_exp(x: ComputableReal) -> ComputableReal:
    return ComputableReal(
        lambda p: Decimal(str(math.exp(float(x.to_decimal(p + 2)))))
    )

# Ejemplo de uso práctico: Cálculo de e^(π/4) * sin(π/3)
if __name__ == "__main__":
    # Definimos π
    pi = ComputableReal(
        lambda p: Decimal('3.141592653589793238462643383279502884197169399375105820974944592307816406286')
    )
    
    # Cálculos
    pi_fourth = pi / ComputableReal(4)
    pi_third = pi / ComputableReal(3)
    
    result = computable_exp(pi_fourth) * computable_sin(pi_third)
    
    # Mostramos resultados con diferentes precisiones
    print("Resultado con diferentes precisiones:")
    for prec in [5, 10, 20]:
        print(f"{prec} decimales: {result.to_decimal(prec)}")