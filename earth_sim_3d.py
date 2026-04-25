from vpython import *
import numpy as np
# Importamos tu función y el radio real desde fisica.py
from fisica import calcular_aceleracion, R_TIERRA

# --- 1. CONFIGURACIÓN DE LA ESCENA ---
scene = canvas(title='Simulación LEO - Artemis Generation', width=1200, height=800, background=color.black)
scene.lights = [] # Eliminamos luces automáticas

# --- 2. CREACIÓN DE OBJETOS ---
# Tierra con radio real y textura interna
tierra = sphere(pos=vector(0,0,0), radius=R_TIERRA, 
                texture=textures.earth) 

# Satélite optimizado (Rojo neón con rastro cian)
satelite = sphere(pos=vector(0,0,0), radius=280000, color=color.red, 
                  emissive=True, make_trail=True, trail_type="curve", 
                  trail_color=color.cyan, retain=150)

# Luz Solar (Simula el Sol en una posición fija)
sun_light = local_light(pos=vector(1.5e7, 0, 1e7), color=color.white)
ambient_light = distant_light(direction=vector(-1, 0, 0), color=color.gray(0.2))

# --- 3. VARIABLES DE MOVIMIENTO (Datos de la ISS) ---
dt = 15 # Segundos por paso (un buen balance entre fluidez y velocidad)
altura_iss = 400000 
posicion = np.array([float(R_TIERRA + altura_iss), 0.0, 0.0])
velocidad = np.array([0.0, 7660.0, 0.0]) # Velocidad orbital circular

# --- 4. BUCLE PRINCIPAL ---
print("Simulación iniciada exitosamente.")

while True:
    rate(100) 
    
    # A. Rotación de la Tierra (Visual)
    tierra.rotate(angle=0.001, axis=vector(0, 1, 0))
    
    # B. Cálculo de física desde tu archivo fisica.py
    acel, choco = calcular_aceleracion([posicion[0], posicion[1]])
    
    if choco:
        print("¡Reentrada atmosférica detectada!")
        satelite.color = color.orange
        break
    
    # C. Integración de Euler (2D -> 3D)
    acel_3d = np.array([acel[0], acel[1], 0.0])
    velocidad += acel_3d * dt
    posicion += velocidad * dt
    
    # D. Actualizar esfera en el espacio 3D
    satelite.pos = vector(posicion[0], posicion[1], posicion[2])