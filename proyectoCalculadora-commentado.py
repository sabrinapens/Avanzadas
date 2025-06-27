import sympy as syp
import numpy as npy
import matplotlib.pyplot as plt
from sympy import oo  

z = syp.symbols('z')#variable simbólica, con esto operará simpy

print("Calculadora de residuos de funciones racionales y trascendentales.\n")
print("1. Calculo de residuo.\n")
print("2. Aplicaciones a integrales reales.\n")

opcion = input("Seleccione una opción (1/2): ").strip() #strip elimina espacios en blanco

if opcion == "1":#siguiente bloque de elección
    print("\nTipo de función:")
    print("1. Racional (polinómica)")
    print("2. Trascendente (exp, log, trig)")
    tipo_funcion = input("Seleccione (1/2): ").strip()

#establece las variables permitidas y el diccionario a utilizar
    if tipo_funcion == "1":#importante distinción de decisión para no sobrecargar los diccionarios de datos permitidos y asegurar que sympyfy no se rompa
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
    else:#validar que no se ingresen valores edxtraños
        print("Opción no válida")
        exit()

    entrada = input(f"\nIngrese f(z) ({ejemplo}): ") #función que ongresa el usuario
    
    try:
        f = syp.sympify(entrada, locals=variables_permitidas) #sympify convierte la entrada en una expresión simbólica
        print(f"\nFunción aceptada: f(z) = {f}")
    except Exception as e:
        print(f"Error: {e}")
        exit()#este bloque de validación también hace la excepcion la fn se sale del diccionario.

    radio = float(input("\nRadio del contorno circular (ej: 3): "))#establecemos radio del contorno
    if radio <= 0:
        print("El radio debe ser un número positivo mayor a cero.")
        exit()
    t = npy.linspace(0, 2*npy.pi, 500)#trazado del círculo. origen;trayectoria;puntos equiespaciados
    z_vals = radio * npy.exp(1j * t)#array del contorno circular en el plano complejo

    try:
        polos = syp.singularities(f, z)#cálculo e impresión de polos
        print("\nPolos encontrados:")
        for p in polos:
            print(f"• z = {p}")
        
        polos_dentro = [p for p in polos if abs(p) < radio]#filtrado de polos dentro del contorno
        print(f"\nPolos dentro del contorno (|z| < {radio}):")
        for p in polos_dentro:
            print(f"• z = {p}")
            
        print("\nResiduos correspondientes:")
        suma_residuos = 0
        for p in polos_dentro:
            res = syp.residue(f, z, p)#cálculo de residuos
            suma_residuos += res
            print(f"Residuo en z = {p} → {res}")
        
        integral = 2*syp.pi*syp.I*suma_residuos
        print(f"\n🎯 Valor de la integral ∮f(z)dz = {integral}")
        
    except Exception as e:#importante para capturar errores de sintaxis en la funcion, o cosas raras como un polo no numérico o infinito
        print(f"Error en cálculo: {e}")
        polos = []
        polos_dentro = []


    plt.figure(figsize=(12, 5))#comenzamos a graficar, creando una figura vacía con dimensiones en pulgadas. es el canvas
    
    plt.subplot(1, 2, 1)#divide el canvas es una fila, dos columnas, y selecciona la primera subgráfica para trazar el contorno original
    plt.plot(npy.real(z_vals), npy.imag(z_vals), 'b-', label=f'Contorno |z|={radio}')#graf. en 2D; X=Re(z_vals), Y=Im(z_vals); b- = línea azul continua; etiqueta del contorno
    for p in polos:
        color = 'red' if abs(p) < radio else 'gray'#por cada polo DENTRO del contorno, se pinta de rojo. la distancia al centro es el módulo del polo. fuera del polo es gris
        plt.scatter(syp.re(p), syp.im(p), color=color, #dibujo de un punto individual en coordenada x=syp.re(p) y coordenada y=syp.im(p)
                   label=f'Polo en z={p}' if abs(p) < radio else None) #etiqueta del polo si está dentro del contorno
    plt.title("Plano z")
    plt.xlabel("Re(z)"); plt.ylabel("Im(z)")#los valores están declarados en el orden correcto; preguntar por la rotación en el ploteo 
    plt.grid(True); plt.legend()#cuadricula de fondo y leyenda
    plt.gca().set_aspect('equal')#get current axis; set aspect ratio igual para que el círculo se vea como un círculo
    
    plt.subplot(1, 2, 2)#subgráfica 2 para la imagen del contorno bajo f(z)
    try:
        f_vals = [complex(f.subs(z, val)) for val in z_vals]#para cada valor en el contorno, sustituye z por el valor y evalúa f(z) como un número complejo
        plt.plot([v.real for v in f_vals], [v.imag for v in f_vals], 'purple', label='f(z)')#grafica la imagen del contorno bajo f(z); X=Re(f_vals), Y=Im(f_vals); línea morada
        plt.title("Transformación bajo f(z)")
        plt.xlabel("Re(f(z))"); plt.ylabel("Im(f(z))")
        plt.grid(True); plt.legend()
        plt.gca().set_aspect('equal')
    except:
        plt.title("No se pudo graficar f(z)")
    
    plt.suptitle(f"Análisis de f(z) = {f}")
    plt.tight_layout()#ajusta el layout para que no se superpongan los títulos y etiquetas
    plt.show()

elif opcion == "2":#opción principal 2, para calcular integrales reales usando el Teorema de Residuos
    print("\nRequisitos para la función f(z):")
    print("1. f(z) debe ser racional (cociente de polinomios)")
    print("2. El denominador no debe tener raíces reales")
    print("3. Grado(denominador) ≥ Grado(numerador) + 2")#el grado de un polinomio es el exponente más alto de su variable
    
    entrada = input("\nIngrese f(x) como función de z (ej: 1/(z**2 + 1)): ")#valor del usuario como función de z para sympy
    try:
        f = syp.sympify(entrada, locals={'z': z}) #diccionario con solo z
        print(f"\nFunción aceptada: f(z) = {f}")
    except Exception as e:
        print(f"Error: {e}")
        exit()
    
    if not f.is_rational_function(z):
        print("La función no es racional")
        exit()
    
    numerador, denominador = syp.fraction(f) #syp.fraction separa la función en su numerador y denominador, ambos polinomios
    grado_num = syp.degree(numerador, z) #calcula el grado del numerador y después del denominador
    grado_den = syp.degree(denominador, z)
    
    if grado_den < grado_num + 2:
        print("No cumple condición de grados (den ≥ num + 2)")
        exit()
    
    polos = syp.singularities(f, z) #cálculo de polos 
    polos_superiores = [p for p in polos if syp.im(p) > 0] #filtrado de polos en el semiplano superior, donde la parte imaginaria es positiva
    
    if not polos_superiores:
        print("No hay polos en el semiplano superior")
        exit()
    
    print("\nPolos en semiplano superior:")
    for p in polos_superiores:
        print(f"• z = {p}")#imprime los polos encontrados en el semiplano superior
    
    print("\nResiduos correspondientes:")
    suma_residuos = 0
    for p in polos_superiores:
        res = syp.residue(f, z, p)
        suma_residuos += res
        print(f"Residuo en z = {p} → {res}")#cálculo e impresion de residuos en cada polo del semiplano superior
    
    integral_real = 2*syp.pi*syp.I*suma_residuos
    print(f"\nValor de la integral ∫f(x)dx (-∞ a ∞) ≈ {integral_real}")#presentamos el valor de la integral
    
    plt.figure(figsize=(12, 5))
    
    R = 10  #radio pre seleccionado para el contorno
    theta = npy.linspace(0, npy.pi, 100) #trazado del semicirculo superior
    semicircle = R * npy.exp(1j * theta) #semicirculo en el plano *complejo*
    #se hace la extensión al plano complejo específicamente para poder aplicar el teorema. Si no, no se puede
    eje_real = npy.linspace(-R, R, 200)
    contorno = npy.concatenate([eje_real, semicircle[::-1]])#creacion del ontorno, concatenando el eje real y el semicirculo invertido donde el ::1 en el semicirculo invierte el orden de los puntos para que vaya de derecha a izquierda
    
    plt.subplot(1, 2, 1)# subgráfica 1 para el contorno de integración
    plt.plot(npy.real(contorno), npy.imag(contorno), 'b-', label='Contorno')
    for p in polos:
        color = 'red' if syp.im(p) > 0 else 'gray'
        plt.scatter(syp.re(p), syp.im(p), color=color, #dibuja los polos en el plano complejo
                   label=f'Polo en z={p}' if syp.im(p) > 0 else None)
    plt.title("Contorno de integración (semiplano superior)")
    plt.xlabel("Re(z)"); plt.ylabel("Im(z)")
    plt.grid(True); plt.legend()
    plt.gca().set_aspect('equal')
    plt.ylim(-1, R+1)
    
    plt.subplot(1, 2, 2)#subgráfica 2 para la función real f(x)
    x_vals = npy.linspace(-5, 5, 400)#valores de x para graficar f(x) en el rango [-5, 5]
    try:
        f_real = syp.lambdify(z, f, 'numpy')#lambdify convierte la función simbólica en una función numérica; numpy permite evaluarla con arrays
        y_vals = f_real(x_vals)#evalúa f(x) para cada valor de x
        plt.plot(x_vals, y_vals, 'purple', label='f(x)')#grafica la función real f(x); X=x_vals, Y=y_vals; con una línea morada
        plt.fill_between(x_vals, y_vals, alpha=0.3, color='purple')
        plt.title("Función real f(x)")
        plt.xlabel("x"); plt.ylabel("f(x)")
        plt.grid(True); plt.legend()
    except:
        plt.title("No se pudo graficar f(x)")
    
    plt.suptitle(f"Integral ∫({entrada})dx de -∞ a ∞ ≈ {integral_real}")
    plt.tight_layout()
    plt.show()

else:
    print("Opción no válida")
