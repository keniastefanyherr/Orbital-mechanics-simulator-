import numpy as np

G = 6.67430e-11  
M_TIERRA = 5.972e24  
R_TIERRA = 6.371e6   

def calcular_aceleracion(posicion):
    x, y = posicion
    distancia = np.sqrt(x**2 + y**2)
    if distancia < R_TIERRA:
        return np.array([0.0, 0.0]), True
    magnitud_a = (G * M_TIERRA) / (distancia**2)
    ax = -magnitud_a * (x / distancia)
    ay = -magnitud_a * (y / distancia)
    return np.array([ax, ay]), False