import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from fisica import calcular_aceleracion, R_TIERRA

# --- CONFIGURACIÓN INICIAL ---
# Posición inicial: 400km sobre la superficie (Órbita de la ISS)
altura_inicial = 400000 
pos_x, pos_y = R_TIERRA + altura_inicial, 0

# Velocidad inicial: 7660 m/s (Velocidad orbital necesaria)
vel_x, vel_y = 0, 7660 

posicion = np.array([float(pos_x), float(pos_y)])
velocidad = np.array([float(vel_x), float(vel_y)])
dt = 10  # Cada paso de la simulación representa 10 segundos reales

# Datos para el dibujo
x_hist, y_hist = [], []

# --- CONFIGURACIÓN DEL GRÁFICO ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-1e7, 1e7)
ax.set_ylim(-1e7, 1e7)

# Dibujar la Tierra
tierra = plt.Circle((0, 0), R_TIERRA, color='skyblue', label='Tierra')
ax.add_artist(tierra)
punto_satelite, = ax.plot([], [], 'ro', label='Satélite')
estela, = ax.plot([], [], 'white', alpha=0.3, linewidth=1)

def actualizar(frame):
    global posicion, velocidad
    
    # 1. Calcular física
    acel, choco = calcular_aceleracion(posicion)
    
    if choco:
        print("¡Colisión detectada!")
        return punto_satelite, estela

    # 2. Actualizar vectores (Método de Euler)
    velocidad += acel * dt
    posicion += velocidad * dt
    
    # 3. Guardar historial para la estela
    x_hist.append(posicion[0])
    y_hist.append(posicion[1])
    
    punto_satelite.set_data([posicion[0]], [posicion[1]])
    estela.set_data(x_hist, y_hist)
    
    return punto_satelite, estela

ani = FuncAnimation(fig, actualizar, frames=2000, interval=10, blit=True)
plt.legend()
plt.title("Simulador de Órbita Terrestre Baja (LEO)")
plt.show()