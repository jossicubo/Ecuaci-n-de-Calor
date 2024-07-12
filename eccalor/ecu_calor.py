# eccalor/ecu_calor.py

"""El módulo contiene las siguientes funciones

El módulo contiene las siguientes funciones:

- `generar_funcion(cond_ini)` - Genera una función f(x, y) a partir de condiciones iniciales que se proporcione.
- `calcB0n(a, b, g, n, f)` - Calcula el coeficiente B0n de la serie de Fourier para la función f(x, y).
- `calcBmn(a, b, g, m, n, f)` - Calcula el coeficiente Bmn de la serie de Fourier para la función f(x, y).
- `precalc_inte(a, b, g, iteraciones, f)` - Precalcula los coeficientes B0n y Bmn para la función f(x, y).
- `onda2D(a, b, g, iteraciones, k, t, B0n_n, Bmn_mn)` - Calcula la propagación de la onda de calor 2D.
- `generar_imagenes(a, b, g, k, t_inicial, t_final, num_pasos, iteraciones, progreso_barra,     vmax, f)` - Genera una serie de imágenes para la animación del calor en la placa


"""

def generar_funcion(cond_ini):
    """Genera una función f(x, y) a partir de condiciones iniciales que se proporcione

    Args:
        cond_ini (str): Las condiciones iniciales se colocan en forma de cadena

    Returns:
        f (func): Retorna la función f(x, y) optimizada con Numba.
    """
    # Genera una función f(x, y) a partir de las condiciones iniciales suministradas en la ventana
    codigo = f"""def f(x, y):
    return {cond_ini}"""
    local_vars = {}
    exec(codigo, globals(), local_vars)  # Ejecuta el código para definir la función f
    return jit(nopython=True)(local_vars['f'])

def calcB0n(a, b, g, n, f):
    """Calcula el coeficiente B0n de la serie de Fourier para la función f(x, y).

    Args:
        a (float): Largo de la placa.
        b (float): Ancho de la placa.
        g (int): Resolución de la malla.
        n (int): Índice del término de Fourier.
        f (func): Función f(x, y).

    Returns:
        B0n (float): Coeficiente
    """
    # Calculamos el coeficiente B0n de la serie de Fourier para una función f(x, y)
    integral = 0.0
    # Calculamos dx y dy como la razón entre el tamaño de la placa y la cantidad de puntos de la malla
    dx = a / g
    dy = b / g
    # Calculamos la integral para obtener los n de la Serie de Fourier
    for i in range(g):
        x = dx * (i + 0.5)
        for j in range(g):
            y = dy * (j + 0.5)
            val_f = f(x, y)
            integral += val_f * np.sin(n * np.pi * y / b) * dx * dy
    return 4 * integral / (a * b)

def calcBmn(a, b, g, m, n, f):
    """Calcula el coeficiente Bmn de la serie de Fourier para la función f(x, y).

    Args:
        a (float): Largo de la placa.
        b (float): Ancho de la placa.
        g (int): Resolución de la malla.
        m (int): Índice del término de Fourier en x.
        n (int): Índice del término de Fourier en y.
        f (func): Función f(x, y)

    Returns:
        Bmn (float): Coeficiente

    """
    # Calculamos el coeficiente Bmn de la serie de Fourier para una función f(x, y)
    integral = 0.0
    # Calculamos dx y dy como la razón entre el tamaño de la placa y la cantidad de puntos de la malla
    dx = a / g
    dy = b / g
    # Calculamos la integral para obtener los m,n de la Serie de Fourier
    for i in range(g):
        x = dx * (i + 0.5)
        for j in range(g):
            y = dy * (j + 0.5)
            val_f = f(x, y)
            integral += val_f * np.sin(n * np.pi * y / b) * np.cos(m * np.pi * x / a) * dx * dy
    return 4 * integral / (a * b)

def precalc_inte(a, b, g, iteraciones, f):
    """Precalcula los coeficientes B0n y Bmn para la función f(x, y).

    Args:
        a (float): Largo de la placa.
        b (float): Ancho de la placa.
        g (int): Resolución de la malla.
        iteraciones (int): Número de términos de Fourier a calcular.
        f (func): Función f(x, y).

    Returns:
        B0n_n (array): Arreglo de los coeficientes subn de la Serie de Fourier
        Bmn_mn (array): Matriz de los coeficientes submn de la Serie de Fourier
    """
    # Usamos listas para B0n_n y una matriz para Bmn_mn
    B0n_n = np.zeros(iteraciones)
    Bmn_mn = np.zeros((iteraciones, iteraciones))
    #Asignamos los valores
    for n in range(1, iteraciones + 1):
        B0n_n[n - 1] = calcB0n(a, b, g, n, f)
    for m in range(1, iteraciones + 1):
        for n in range(1, iteraciones + 1):
            Bmn_mn[m - 1][n - 1] = calcBmn(a, b, g, m, n, f)
    return B0n_n, Bmn_mn

def onda2D(a, b, g, iteraciones, k, t, B0n_n, Bmn_mn):
    """Calcula la propagación de la onda de calor 2D.

    Args:
        a (float): Largo de la placa.
        b (float): Ancho de la placa.
        g (int): Resolución de la malla.
        iteraciones (int): Número de términos de Fourier a calcular.
        k (float): Constante de difusión.
        t (float): Tiempo.

    Returns:
        x, y, u (array): Matriz Z con los valores de temperatura en cada punto (x, y) de la malla.
    """
    # Generamos la malla y u
    x = np.linspace(0, a, g)
    y = np.linspace(0, b, g)
    u = np.zeros((g, g))
    for n in range(1, iteraciones + 1):
        B0n = B0n_n[n - 1]
        u += 0.5 * B0n * np.exp(-(n ** 2 / b ** 2) * np.pi ** 2 * k * t) * np.sin(n * np.pi * y[:, None] / b)
        # y[:, None] convierte y a una matriz bidimensional lo que mejora el cálculo al usar Broadcasting de Numpy
    for m in range(1, iteraciones + 1):
        for n in range(1, iteraciones + 1):
            Bmn = Bmn_mn[m - 1][n - 1]
            u += Bmn * np.exp(-(m ** 2 / a ** 2 + n ** 2 / b ** 2) * np.pi ** 2 * k * t) \
                 * np.sin(n * np.pi * y[:, None] / b) * np.cos(m * np.pi * x[None, :] / a) #igual para x e y
    return x, y, u

def generar_imagenes(a, b, g, k, t_inicial, t_final, num_pasos, iteraciones, progreso_barra, vmax, f):
    """Genera una serie de imágenes para la animación del calor en la placa

    Args:
        a (float): Largo de la placa.
        b (float): Ancho de la placa.
        g (int): Resolución de la malla.
        k (float): Constante de difusión.
        t_inicial (float): Tiempo inicial.
        t_final (float): Tiempo final.
        num_pasos (int): Número de pasos de tiempo.
        iteraciones (int): Número de términos de Fourier a calcular.
        progreso_barra (tk.DoubleVar): Variable para la barra de progreso.
        vmax (float): Valor máximo de la temperatura.
        f (func): Función f(x, y).

    Returns:
        imágenes (array): Lista de imágenes generadas.
    """
    B0n_n, Bmn_mn = precalc_inte(a, b, g, iteraciones, f)
    imagenes = []
    for step in range(num_pasos + 1):
        t = t_inicial + step * (t_final - t_inicial) / num_pasos
        x, y, Z = onda2D(a, b, g, iteraciones, k, t, B0n_n, Bmn_mn)
        fig, ax = plt.subplots(figsize=(10, 8), dpi=150)  # Usamos figsize y dpi para que la gráfica se vea bien
        # mantenemos el calor inicial vmax para que las gráficas mantengan concordancia
        c = ax.contourf(x, y, Z, cmap='viridis', levels=20, vmin=0, vmax=vmax)
        fig.colorbar(c)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Onda de calor en t={:.2f}s'.format(t))
        fig.canvas.draw()  # Grafica la figura usando canvas
        imagen = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8').reshape(
            fig.canvas.get_width_height()[::-1] + (3,))
        imagenes.append(imagen)
        ax.clear()  # Limpiamos el gráfico
        plt.close(fig)  # Cerramos la figura para evitar tener datos innecesarios en memoria
        progreso = (step / num_pasos) * 100
        progreso_var.set(progreso)
        vent.update_idletasks()
        print(f"Progreso: {progreso:.1f}%") # Para tener el progreso en la terminal al generar las imágnes
    return imagenes






