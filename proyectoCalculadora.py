import sympy as syp
import numpy as npy
import matplotlib.pyplot as plt
from sympy import oo  # infinito

# Configuración inicial
z = syp.symbols('z')

# Menú principal
print("Calculadora de residuos de funciones racionales y trascendentales.\n")
print("1. Calculo de residuo.\n")
print("2. Aplicaciones a integrales reales.\n")

opcion = input("Seleccione una opción (1/2): ").strip()

if opcion == "1":
    print("\nTipo de función:")
    print("1. Racional (polinómica)")
    print("2. Trascendente (exp, log, trig)")
    tipo_funcion = input("Seleccione (1/2): ").strip()

    # Definir funciones permitidas
    if tipo_funcion == "1":
        variables_permitidas = {
            'z': z,
            'I': syp.I, 
            'pi': syp.pi
        }
        ejemplo = "Ej: (z**2 + 1)/(z - 2)"
    elif tipo_funcion == "2":
        variables_permitidas = {
            'z': z, 
            'sin': syp.sin, 
            'cos': syp.cos, 
            'exp': syp.exp, 
            'tan': syp.tan, 
            'log': syp.log,
            'pi': syp.pi, 
            'E': syp.E, 
            'I': syp.I
        }
        ejemplo = "Ej: exp(z)/(z**2 + pi**2)"
    else:
        print("Opción no válida")
        exit()

    # Ingreso de función
    entrada = input(f"\nIngrese f(z) ({ejemplo}): ")
    try:
        f = syp.sympify(entrada, locals=variables_permitidas)
        print(f"\nFunción aceptada: f(z) = {f}")
    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Configuración de contorno circular
    radio = float(input("\nRadio del contorno circular (ej: 3): "))
    t = npy.linspace(0, 2*npy.pi, 500)
    z_vals = radio * npy.exp(1j * t)

    # Cálculo de polos y residuos
    try:
        polos = syp.singularities(f, z)
        print("\nPolos encontrados:")
        for p in polos:
            print(f"• z = {p}")
        
        polos_dentro = [p for p in polos if abs(p) < radio]
        print(f"\nPolos dentro del contorno (|z| < {radio}):")
        for p in polos_dentro:
            print(f"• z = {p}")
            
        print("\nResiduos correspondientes:")
        suma_residuos = 0
        for p in polos_dentro:
            res = syp.residue(f, z, p)
            suma_residuos += res
            print(f"Residuo en z = {p} → {res}")
        
        integral = 2*syp.pi*syp.I*suma_residuos
        print(f"\n🎯 Valor de la integral ∮f(z)dz = {integral}")
        
    except Exception as e:
        print(f"Error en cálculo: {e}")
        polos = []
        polos_dentro = []

    # Visualización
    plt.figure(figsize=(12, 5))
    
    # Plano z
    plt.subplot(1, 2, 1)
    plt.plot(npy.real(z_vals), npy.imag(z_vals), 'b-', label=f'Contorno |z|={radio}')
    for p in polos:
        color = 'red' if abs(p) < radio else 'gray'
        plt.scatter(syp.re(p), syp.im(p), color=color, 
                   label=f'Polo en z={p}' if abs(p) < radio else None)
    plt.title("Plano z")
    plt.xlabel("Re(z)"); plt.ylabel("Im(z)")
    plt.grid(True); plt.legend()
    plt.gca().set_aspect('equal')
    
    # Plano w = f(z)
    plt.subplot(1, 2, 2)
    try:
        f_vals = [complex(f.subs(z, val)) for val in z_vals]
        plt.plot([v.real for v in f_vals], [v.imag for v in f_vals], 'purple', label='f(z)')
        plt.title("Transformación bajo f(z)")
        plt.xlabel("Re(f(z))"); plt.ylabel("Im(f(z))")
        plt.grid(True); plt.legend()
        plt.gca().set_aspect('equal')
    except:
        plt.title("No se pudo graficar f(z)")
    
    plt.suptitle(f"Análisis de f(z) = {f}", y=1.02)
    plt.tight_layout()
    plt.show()

elif opcion == "2":
    # ==============================================
    # OPCIÓN 2: INTEGRALES REALES (-∞ a ∞)
    # ==============================================
    
    print("\nRequisitos para la función f(z):")
    print("1. f(z) debe ser racional (cociente de polinomios)")
    print("2. El denominador no debe tener raíces reales")
    print("3. Grado(denominador) ≥ Grado(numerador) + 2")
    
    # Ingreso de función
    entrada = input("\nIngrese f(x) como función de z (ej: 1/(z**2 + 1)): ")
    try:
        f = syp.sympify(entrada, locals={'z': z})
        print(f"\nFunción aceptada: f(z) = {f}")
    except Exception as e:
        print(f"Error: {e}")
        exit()
    
    # Verificar que sea racional
    if not f.is_rational_function(z):
        print("La función no es racional")
        exit()
    
    # Verificar grado del denominador
    numerador, denominador = syp.fraction(f)
    grado_num = syp.degree(numerador, z)
    grado_den = syp.degree(denominador, z)
    
    if grado_den < grado_num + 2:
        print("No cumple condición de grados (den ≥ num + 2)")
        exit()
    
    # Encontrar polos en semiplano superior
    polos = syp.singularities(f, z)
    polos_superiores = [p for p in polos if syp.im(p) > 0]
    
    if not polos_superiores:
        print("No hay polos en el semiplano superior")
        exit()
    
    print("\nPolos en semiplano superior:")
    for p in polos_superiores:
        print(f"• z = {p}")
    
    # Calcular residuos
    print("\nResiduos correspondientes:")
    suma_residuos = 0
    for p in polos_superiores:
        res = syp.residue(f, z, p)
        suma_residuos += res
        print(f"Residuo en z = {p} → {res}")
    
    # Calcular integral
    integral_real = 2*syp.pi*syp.I*suma_residuos
    print(f"\nValor de la integral ∫f(x)dx (-∞ a ∞) ≈ {integral_real}")
    
    # Visualización
    plt.figure(figsize=(12, 5))
    
    # Contorno semicircular
    R = 10  # Radio grande para ∞
    theta = npy.linspace(0, npy.pi, 100)
    semicircle = R * npy.exp(1j * theta)
    eje_real = npy.linspace(-R, R, 200)
    contorno = npy.concatenate([eje_real, semicircle[::-1]])
    
    # Plano z
    plt.subplot(1, 2, 1)
    plt.plot(npy.real(contorno), npy.imag(contorno), 'b-', label='Contorno')
    for p in polos:
        color = 'red' if syp.im(p) > 0 else 'gray'
        plt.scatter(syp.re(p), syp.im(p), color=color, 
                   label=f'Polo en z={p}' if syp.im(p) > 0 else None)
    plt.title("Contorno de integración (semiplano superior)")
    plt.xlabel("Re(z)"); plt.ylabel("Im(z)")
    plt.grid(True); plt.legend()
    plt.gca().set_aspect('equal')
    plt.ylim(-1, R+1)
    
    # Gráfico de la función real
    plt.subplot(1, 2, 2)
    x_vals = npy.linspace(-5, 5, 400)
    try:
        f_real = syp.lambdify(z, f, 'numpy')
        y_vals = f_real(x_vals)
        plt.plot(x_vals, y_vals, 'purple', label='f(x)')
        plt.fill_between(x_vals, y_vals, alpha=0.3, color='purple')
        plt.title("Función real f(x)")
        plt.xlabel("x"); plt.ylabel("f(x)")
        plt.grid(True); plt.legend()
    except:
        plt.title("No se pudo graficar f(x)")
    
    plt.suptitle(f"Integral ∫({entrada})dx de -∞ a ∞ ≈ {integral_real}", y=1.02)
    plt.tight_layout()
    plt.show()

else:
    print("Opción no válida")
