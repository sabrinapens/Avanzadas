import sympy

#enteros
print(type(sympy.sympify(5)))         # <class 'sympy.core.numbers.Integer'>

#decimales
print(type(sympy.sympify(19.14)))      # <class 'sympy.core.numbers.Float'>

#strings
print(sympy.sympify("z**3 + 2"))         # z**3 + 2
print(type(sympy.sympify("z**3 + 2")))   # <class 'sympy.core.add.Add'>
