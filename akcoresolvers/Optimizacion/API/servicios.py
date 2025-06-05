import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scipy.optimize import linprog
import io
import csv
from sympy import symbols, Eq, solve, diff, integrate, factor, apart, simplify, expand, parse_expr, init_printing
from sympy.parsing.latex import parse_latex
import re

def resolver_grafico(datos):
    if len(datos["funcion_objetivo"]["coeficientes"]) != 2:
        return {"error": "El método gráfico solo funciona con 2 variables"}

    # Extraer datos
    coef_fo = datos["funcion_objetivo"]["coeficientes"]
    tipo = datos["funcion_objetivo"]["tipo"]
    restricciones = datos["restricciones"]

    # Aquí iría la lógica para graficar y encontrar la solución
    x = np.linspace(0, 10, 400)
    y = np.linspace(0, 10, 400)
    X, Y = np.meshgrid(x, y)

    plt.figure(figsize=(8, 6))

    for r in restricciones:
        a, b = r["coeficientes"]
        c = r["valor"]
        signo = r["signo"]

        if b != 0:
            y_restr = (c - a * x) / b
            plt.plot(x, y_restr, label=f"{a}x + {b}y {signo} {c}")
        else:
            plt.axvline(c, label=f"x {signo} {c}")

    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    grafica = base64.b64encode(buf.read()).decode('utf-8')

    # Resultados ficticios (luego lo calculas)
    resultado = {
        "mensaje": "Solución aproximada",
        "x_optimo": [2, 2],
        "z_optimo": 16,
        "grafica": grafica
    }

    return resultado


def generar_grafico(datos):
    if len(datos["funcion_objetivo"]["coeficientes"]) != 2:
        return {"error": "El método gráfico solo funciona con 2 variables"}

    coef_fo = datos["funcion_objetivo"]["coeficientes"]
    restricciones = datos["restricciones"]

    x = np.linspace(0, 10, 400)

    plt.figure(figsize=(8, 6))

    for r in restricciones:
        a, b = r["coeficientes"]
        c = r["valor"]
        signo = r["signo"]

        if b != 0:
            y_restr = (c - a * x) / b
            plt.plot(x, y_restr, label=f"{a}x + {b}y {signo} {c}")
        else:
            plt.axvline(c, label=f"x {signo} {c}")

    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf



def resolver_simplex(datos):
    
    # Validaciones básicas
    if 'funcion_objetivo' not in datos:
        return {"error": "Falta la función objetivo"}

    if 'coeficientes' not in datos['funcion_objetivo']:
        return {"error": "La función objetivo debe tener coeficientes"}

    if 'restricciones' not in datos or not isinstance(datos['restricciones'], list):
        return {"error": "Las restricciones deben ser una lista"}

    num_vars = len(datos["funcion_objetivo"]["coeficientes"])
    if num_vars < 1:
        return {"error": "La función objetivo debe tener al menos una variable"}

    for r in datos["restricciones"]:
        if len(r["coeficientes"]) != num_vars:
            return {"error": f"Todas las restricciones deben tener {num_vars} variables"}
        if r["signo"] not in ['<=', '=', '>=']:
            return {"error": "Signo de restricción inválido. Use <=, = o >="}

    # Preparar función objetivo
    c = np.array(datos["funcion_objetivo"]["coeficientes"], dtype=float)
    is_max = datos["funcion_objetivo"].get("tipo", "min").lower() == "max"
    if is_max:
        c = -c  # Invertimos para maximización

    # Restricciones
    A_ub = []
    b_ub = []
    A_eq = []
    b_eq = []

    for r in datos["restricciones"]:
        coefs = np.array(r["coeficientes"], dtype=float)
        val = float(r["valor"])

        if r["signo"] == "<=":
            A_ub.append(coefs)
            b_ub.append(val)
        elif r["signo"] == ">=":
            A_ub.append(-coefs)
            b_ub.append(-val)
        elif r["signo"] == "=":
            A_eq.append(coefs)
            b_eq.append(val)

    # Límites de variables
    bounds = [(0, None)] * num_vars

    # Resolver problema
    try:
        resultado = linprog(c, A_ub=A_ub or None, b_ub=b_ub or None,
                            A_eq=A_eq or None, b_eq=b_eq or None,
                            bounds=bounds, method='highs')
    except Exception as e:
        return {"error": f"Error interno al resolver el problema: {str(e)}"}

    # Interpretar resultados
    if resultado.success:
        solucion = {
            "mensaje": "Solución óptima encontrada",
            "z_optimo": round(-resultado.fun if is_max else resultado.fun, 4),
            "variables": {f"x{i+1}": round(valor, 4) for i, valor in enumerate(resultado.x)},
            "estado": "Óptimo"
        }
    elif resultado.status == 2:
        solucion = {"mensaje": "El problema no tiene solución factible (infeasible)"}
    elif resultado.status == 3:
        solucion = {"mensaje": "El problema es ilimitado (unbounded)"}
    elif resultado.status == 4:
        solucion = {"mensaje": "Problema ilimitado o sin solución clara"}
    else:
        solucion = {"mensaje": "No se pudo encontrar una solución óptima", "detalle": str(resultado)}

    # Generar CSV solo si hay solución
    if resultado.success:
        # Crear CSV en memoria
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Variable", "Valor"])

        for var, valor in solucion["variables"].items():
            writer.writerow([var, valor])

        writer.writerow(["Z óptimo", solucion["z_optimo"]])

        # Codificar CSV como Base64 para enviarlo en JSON
        csv_data = output.getvalue()
        solucion["archivo_csv"] = base64.b64encode(csv_data.encode()).decode('utf-8')

    return solucion


# CHATTTTTTTTTTTTTTTTTTTTTTTTTT CHATTTTTTTTTTTTTTTTTTTTTTTTTTTTT

def procesar_entrada(entrada):
    

    init_printing(use_unicode=True)

    try:
        # Eliminar espacios extra
        entrada = entrada.strip()

        # Identificar tipo de cálculo usando expresiones regulares
        if re.search(r'\bderivative\b|\bdiff\b', entrada, re.IGNORECASE):
            return procesar_derivada(entrada)
        elif re.search(r'\bintegral\b|\bint\b', entrada, re.IGNORECASE):
            return procesar_integral(entrada)
        elif re.search(r'\bfactor\b', entrada, re.IGNORECASE):
            return procesar_factor(entrada)
        elif re.search(r'\bapart\b', entrada, re.IGNORECASE):
            return procesar_apart(entrada)
        elif re.search(r'\bsolve\b', entrada, re.IGNORECASE):
            return procesar_ecuacion(entrada)
        elif re.search(r'\bsystem\b', entrada, re.IGNORECASE):
            return procesar_sistema_ecuaciones(entrada)
        elif re.search(r'\bsum\b|\badd\b', entrada, re.IGNORECASE):
            return procesar_suma(entrada)
        elif re.search(r'\bsubtract\b|\bresta\b', entrada, re.IGNORECASE):
            return procesar_resta(entrada)
        elif re.search(r'\bmultiply\b|\bmultiplicacion\b', entrada, re.IGNORECASE):
            return procesar_multiplicacion(entrada)
        elif re.search(r'\bdivide\b|\bdivision\b', entrada, re.IGNORECASE):
            return procesar_division(entrada)
        else:
            return procesar_expresion(entrada)

    except Exception as e:
        return {"error": f"No se pudo procesar la entrada: {str(e)}"}

def procesar_derivada(entrada):
    # Ejemplo: derivative(x**2 + 3*x + 2, x)
    match = re.search(r'derivative\(([^,]+),\s*([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para derivada. Usa: derivative(expresion, variable)"}

    expr_str = match.group(1).strip()
    var_str = match.group(2).strip()

    try:
        expr = parse_expr(expr_str)
        var = symbols(var_str)
        derivada = diff(expr, var)

        return {
            "tipo": "derivada",
            "expresion": str(expr),
            "variable": str(var),
            "derivada": str(derivada)
        }
    except Exception as e:
        return {"error": f"No se pudo calcular la derivada: {str(e)}"}

def procesar_integral(entrada):
    # Ejemplo: integral(x**2 + 3*x + 2, x)
    match = re.search(r'integral\(([^,]+),\s*([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para integral. Usa: integral(expresion, variable)"}

    expr_str = match.group(1).strip()
    var_str = match.group(2).strip()

    try:
        expr = parse_expr(expr_str)
        var = symbols(var_str)
        integral = integrate(expr, var)

        return {
            "tipo": "integral",
            "expresion": str(expr),
            "variable": str(var),
            "integral": str(integral)
        }
    except Exception as e:
        return {"error": f"No se pudo calcular la integral: {str(e)}"}

def procesar_factor(entrada):
    # Ejemplo: factor(x**2 - 1)
    match = re.search(r'factor\(([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para factorización. Usa: factor(expresion)"}

    expr_str = match.group(1).strip()

    try:
        expr = parse_expr(expr_str)
        factored_expr = factor(expr)

        return {
            "tipo": "factor",
            "expresion": str(expr),
            "factorizado": str(factored_expr)
        }
    except Exception as e:
        return {"error": f"No se pudo factorizar la expresión: {str(e)}"}

def procesar_apart(entrada):
    # Ejemplo: apart(1/(x**2 - 1), x)
    match = re.search(r'apart\(([^,]+),\s*([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para descomposición en fracciones parciales. Usa: apart(expresion, variable)"}

    expr_str = match.group(1).strip()
    var_str = match.group(2).strip()

    try:
        expr = parse_expr(expr_str)
        var = symbols(var_str)
        apart_expr = apart(expr, var)

        return {
            "tipo": "apart",
            "expresion": str(expr),
            "variable": str(var),
            "apartado": str(apart_expr)
        }
    except Exception as e:
        return {"error": f"No se pudo descomponer la expresión: {str(e)}"}

def procesar_ecuacion(entrada):
    # Ejemplo: solve(x**2 - 5*x + 6 = 0, x)
    match = re.search(r'solve\(([^,]+),\s*([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para resolver ecuación. Usa: solve(ecuacion, variable)"}

    eq_str = match.group(1).strip()
    var_str = match.group(2).strip()

    try:
        lhs, rhs = eq_str.split('=')
        eq = Eq(parse_expr(lhs.strip()), parse_expr(rhs.strip()))
        var = symbols(var_str)
        solucion = solve(eq, var)

        return {
            "tipo": "ecuacion",
            "ecuacion": str(eq),
            "variable": str(var),
            "solucion": [str(sol) for sol in solucion]
        }
    except Exception as e:
        return {"error": f"No se pudo resolver la ecuación: {str(e)}"}

def procesar_sistema_ecuaciones(entrada):
    # Ejemplo: system({x + y = 5, x - y = 1}, x, y)
    match = re.search(r'system\({([^}]+)},\s*([^,]+),\s*([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para sistema de ecuaciones. Usa: system({ecuacion1, ecuacion2}, variable1, variable2)"}

    eqs_str = match.group(1).strip()
    var1_str = match.group(2).strip()
    var2_str = match.group(3).strip()

    try:
        eqs = [Eq(parse_expr(eq.split('=')[0].strip()), parse_expr(eq.split('=')[1].strip())) for eq in eqs_str.split(',')]
        vars = symbols(f"{var1_str} {var2_str}")
        solucion = solve(eqs, vars)

        return {
            "tipo": "sistema_ecuaciones",
            "ecuaciones": [str(eq) for eq in eqs],
            "variables": [str(var) for var in vars],
            "solucion": {str(var): str(sol) for var, sol in solucion.items()}
        }
    except Exception as e:
        return {"error": f"No se pudo resolver el sistema de ecuaciones: {str(e)}"}

def procesar_suma(entrada):
    # Ejemplo: sum(2 + 3)
    match = re.search(r'sum\(([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para suma. Usa: sum(expresion1, expresion2, ...)"}

    expr_str = match.group(1).strip()
    try:
        exprs = [parse_expr(expr.strip()) for expr in expr_str.split(',')]
        resultado = sum(exprs)

        return {
            "tipo": "suma",
            "expresiones": [str(expr) for expr in exprs],
            "resultado": str(resultado)
        }
    except Exception as e:
        return {"error": f"No se pudo calcular la suma: {str(e)}"}

def procesar_resta(entrada):
    # Ejemplo: subtract(5 - 2)
    match = re.search(r'subtract\(([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para resta. Usa: subtract(expresion1, expresion2, ...)"}

    expr_str = match.group(1).strip()
    try:
        exprs = [parse_expr(expr.strip()) for expr in expr_str.split(',')]
        resultado = exprs[0] - sum(exprs[1:])

        return {
            "tipo": "resta",
            "expresiones": [str(expr) for expr in exprs],
            "resultado": str(resultado)
        }
    except Exception as e:
        return {"error": f"No se pudo calcular la resta: {str(e)}"}

def procesar_multiplicacion(entrada):
    # Ejemplo: multiply(2 * 3)
    match = re.search(r'multiply\(([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para multiplicación. Usa: multiply(expresion1, expresion2, ...)"}

    expr_str = match.group(1).strip()
    try:
        exprs = [parse_expr(expr.strip()) for expr in expr_str.split(',')]
        resultado = 1
        for expr in exprs:
            resultado *= expr

        return {
            "tipo": "multiplicacion",
            "expresiones": [str(expr) for expr in exprs],
            "resultado": str(resultado)
        }
    except Exception as e:
        return {"error": f"No se pudo calcular la multiplicación: {str(e)}"}

def procesar_division(entrada):
    # Ejemplo: divide(10 / 2)
    match = re.search(r'divide\(([^,]+),\s*([^)]+)\)', entrada, re.IGNORECASE)
    if not match:
        return {"error": "Formato incorrecto para división. Usa: divide(expresion1, expresion2)"}

    expr1_str = match.group(1).strip()
    expr2_str = match.group(2).strip()

    try:
        expr1 = parse_expr(expr1_str)
        expr2 = parse_expr(expr2_str)
        resultado = expr1 / expr2

        return {
            "tipo": "division",
            "expresion1": str(expr1),
            "expresion2": str(expr2),
            "resultado": str(resultado)
        }
    except Exception as e:
        return {"error": f"No se pudo calcular la división: {str(e)}"}

def procesar_expresion(entrada):
    # Ejemplo: simplify(x**2 - 1)
    try:
        expr = parse_expr(entrada)
        simplificada = simplify(expr)

        return {
            "tipo": "expresion",
            "original": str(expr),
            "simplificada": str(simplificada)
        }
    except Exception as e:
        return {"error": f"No se pudo procesar la expresión: {str(e)}"}