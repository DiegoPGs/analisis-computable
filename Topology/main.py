from typing import List, Tuple, Callable
import numpy as np
from dataclasses import dataclass

@dataclass
class Point:
    coordinates: List[float]
    
class ComputableMetricSpace:
    def __init__(self, 
                base_points: List[Point],
                metric: Callable[[Point, Point], float],
                approximation_function: Callable[[int, Point], Point]):
        """
        Inicializa un espacio métrico computable
        
        Args:
            base_points: Conjunto denso numerable de puntos base
            metric: Función de distancia computable
            approximation_function: Función que aproxima puntos con precisión dada
        """
        self.base_points = base_points
        self.metric = metric
        self.approximate = approximation_function
    
    def distance(self, p1: Point, p2: Point) -> float:
        """Calcula la distancia entre dos puntos"""
        return self.metric(p1, p2)
    
    def find_approximation(self, point: Point, precision: int) -> Point:
        """Encuentra una aproximación de un punto con la precisión dada"""
        return self.approximate(precision, point)
    
    def is_cauchy_sequence(self, sequence: List[Point], epsilon: float) -> bool:
        """Verifica si una secuencia es de Cauchy"""
        for i in range(len(sequence)):
            for j in range(i + 1, len(sequence)):
                if self.distance(sequence[i], sequence[j]) >= epsilon:
                    return False
        return True

# Ejemplo: Espacio métrico de números reales en [0,1]
def euclidean_metric(p1: Point, p2: Point) -> float:
    return abs(p1.coordinates[0] - p2.coordinates[0])

def rational_approximation(precision: int, point: Point) -> Point:
    """Aproxima un número real con racionales"""
    return Point([round(point.coordinates[0], precision)])

# Crear un espacio métrico computable simple
base_points = [Point([i/10]) for i in range(11)]  # Puntos racionales en [0,1]
real_line_segment = ComputableMetricSpace(
    base_points=base_points,
    metric=euclidean_metric,
    approximation_function=rational_approximation
)

# Ejemplo de uso
if __name__ == "__main__":
    p1 = Point([0.3])
    p2 = Point([0.7])
    
    print(f"Distancia entre {p1.coordinates[0]} y {p2.coordinates[0]}: "
            f"{real_line_segment.distance(p1, p2)}")
    
    # Aproximación de un punto
    p3 = Point([np.pi/4])
    approx = real_line_segment.find_approximation(p3, 4)
    print(f"Aproximación de π/4 con 4 decimales: {approx.coordinates[0]}")