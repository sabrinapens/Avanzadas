# Debemos: Calcular el res(fx) trascendentales y racionales
# Visualizar polos/contornos
# Estimar inegrales con el TdR
# Posibles bibliotecas a usar:
#import sympy as sip
#import matplotlib.pyplot as plot
#import numpy as npy

# Variable simbólica, ejemplo:
#z = sip.symbols('z')

#prototipo 1

import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# variables simbólicas (forma abstracta para trabajar literalmente con variables)
z = sp.symbols('z')

# función predefinida de ejemplo
f = (z**2 + 1) / ((z - 1)*(z + 2))#como expr en el tutorial

# polos
polos = sp.singularities(f, z)
print(f"Polos encontrados: {polos}")

# residuos en cada polo
for polo in polos:
    res = sp.residue(f, z, polo)
    print(f"Residuo en z = {polo}: {res}")

# contorno ??? referencia externa, investigar más 
t = np.linspace(0, 2*np.pi, 500)
radio = 3
x = radio * np.cos(t)
y = radio * np.sin(t)

plt.figure(figsize=(6,6))
plt.plot(x, y, label='Circular contour')
plt.scatter([sp.re(p) for p in polos], [sp.im(p) for p in polos], color='red', label='Singularities')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True)
plt.gca().set_aspect('equal')
plt.legend()
plt.title("Contour and singularities")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.show()