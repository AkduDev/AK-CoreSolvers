import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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