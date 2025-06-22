import sympy as syp
import numpy as npy
import matplotlib.pyplot as plt

# 1. Declarar variable simbólica y funciones permitidas
z = syp.symbols('z')
from sympy import sin, cos, exp, tan, log

# Diccionario seguro de funciones y variables permitidas
variables_permitidas = {
    'z': z,
    'sin': sin,
    'cos': cos,
    'exp': exp,
    'tan': tan,
    'log': log,
    'pi': syp.pi,
    'E': syp.E,
    'I': syp.I  # número imaginario
}

# 2. Pedir al usuario la función
entrada = input("Escribe una función de z (ej: (z**2 + 1)/(z - 2)): ")

try:
    funcion = syp.sympify(entrada, locals=variables_permitidas)
    print(f"\n✅ Función interpretada correctamente: f(z) = {funcion}")
except Exception as e:
    print("❌ Error: la expresión no es válida o segura.")
    print("Detalles:", e)
    exit()

# 3. Encontrar polos de la función
try:
    polos = syp.singularities(funcion, z)
    print("\n📍 Polos encontrados:")
    for p in polos:
        print(f"• z = {p}")
except Exception as e:
    print("❌ Error al calcular polos.")
    print("Detalles:", e)
    polos = []

# 4. Calcular residuos
print("\n🔁 Residuos en los polos:")
for polo in polos:
    try:
        res = syp.residue(funcion, z, polo)
        print(f"Residuo en z = {polo} → {res}")
    except Exception as e:
        print(f"No se pudo calcular el residuo en z = {polo}. Detalles:", e)

# 5. Generar contorno original (círculo)
t = npy.linspace(0, 2*npy.pi, 500)
radio = 3
z_vals = radio * npy.cos(t) + 1j * radio * npy.sin(t)  # puntos en el círculo

# 6. Aplicar la función f(z) al contorno
try:
    f_vals = [complex(funcion.subs(z, val)) for val in z_vals]
except Exception as e:
    print("\n❌ No se pudo aplicar f(z) al contorno.")
    print("Detalles:", e)
    f_vals = []

# 7. Graficar el contorno original y su imagen bajo f(z)
plt.figure(figsize=(10, 5))

# Gráfica 1: contorno original en el plano z
plt.subplot(1, 2, 1)
plt.plot(npy.real(z_vals), npy.imag(z_vals), label='Contorno original')
plt.scatter([syp.re(p) for p in polos], [syp.im(p) for p in polos], color='red', label='Polos')
plt.title("Plano z (entrada)")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.grid(True)
plt.gca().set_aspect('equal')
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.legend()

# Gráfica 2: imagen del contorno bajo f(z)
plt.subplot(1, 2, 2)
if f_vals:
    plt.plot([val.real for val in f_vals], [val.imag for val in f_vals], label='Imagen bajo f(z)', color='purple')
    plt.title("Plano w = f(z) (salida)")
    plt.xlabel("Re(f(z))")
    plt.ylabel("Im(f(z))")
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.legend()
else:
    plt.title("No se pudo graficar f(z)")

plt.tight_layout()
plt.show()
