# eccalor/difefini.py
"""
Calculamos la ecuación diferencial del calor usando Diferencias Finitas

El módulo maneja 4 funciones:

- `condini1(x, y, cmax)` - Genera una condición de frontera donde los bordes izquierdo, superior e inferior son cmax, mientras que el borde derecho es igual a cero
- `condini2(x, y, cmax)` - Genera una condición inicial donde se crea una isla de calor en el centro de la malla con su centro de calor cmax
- `condini3(x, y, cmax)` - Genera una condición de frontera donde los bordes izquierdo, superior e inferios son iguales a cero, mientras que el borde derecho es igual a cmax
- `act_calor(Z, k, dt, dx, dy)` - Calcula el valor siguiente de calor con los valores actuales de calor usando el método de diferencias finitas
- `generarimagen(x, y, Z, t, vmax) `- Genera una gráfica a partir de los datos suministrados
- `generardatos(x, y, Z, k, dt, t_inicial, t_final, num_pasos, vmax, dx, dy) `- Genera todas las imágenes a partir de los datos suministrados

"""


def condini1(x, y, cmax):
    """ genera una malla Z, de tamaño x,y con las siguientes condiciones iniciales, cmax en los bordes izquierdo, superior e inferior, 0 en el borde derecho.

    Examples:
        >>> x = np.linspace(0,100,100)
        >>> y = np.linspace(0,200,100)
        >>> cmax = 500
        >>> condini1(x, y, cmax)
        [[500, 500, ..., 0], [500, 0, ..., 0], ..., [500, 500, ..., 0]]

    Args:
        x (array): Arreglo espacial de pasos equidistantes
        y (array): Arreglo espacial de pasos equidistantes
        cmax (float): Variable de calor

    Returns:
        Z (array): Grilla con los valores asignados por las condiciones iniciales
    """
    Z = np.zeros_like(x)
    Z[:, 0] = Z[0, :] = Z[-1, :] = cmax
    Z[:, -1] = 0
    return Z


def condini2(x, y, cmax):
    """ genera una malla Z, de tamaño x,y con las siguientes condiciones iniciales, cmax en el centro, cero en los bordes

    Examples:
        >>> x = np.linspace(0,100,100)
        >>> y = np.linspace(0,200,100)
        >>> cmax = 500
        >>> condini1(x, y, cmax)
        [[0, 0, ..., 0], [0, 0, ..., 0], ..., [0, ..., 500, ..., 0], ..., [0, 0, ..., 0], [0, 0, ..., 0]]

    Args:
        x (array): Arreglo espacial de pasos equidistantes
        y (array): Arreglo espacial de pasos equidistantes
        cmax (float): Variable de calor

    Returns:
        Z (array): Grilla con los valores asignados por las condiciones iniciales
    """
    Z = np.zeros_like(x)
    centro_x = int(x.shape[0] / 2)
    centro_y = int(y.shape[1] / 2)
    radio1 = int(min(x.shape[0], y.shape[1]) / 12)
    radio2 = int(min(x.shape[0], y.shape[1]) / 10)
    radio3 = int(min(x.shape[0], y.shape[1]) / 8)
    radio4 = int(min(x.shape[0], y.shape[1]) / 6)
    for i in prange(x.shape[0]):
        for j in prange(y.shape[1]):
            if (i - centro_x) ** 2 + (j - centro_y) ** 2 <= radio4 ** 2:
                Z[i, j] = cmax/6
            if (i - centro_x) ** 2 + (j - centro_y) ** 2 <= radio3 ** 2:
                Z[i, j] = cmax/4
            if (i - centro_x) ** 2 + (j - centro_y) ** 2 <= radio2 ** 2:
                Z[i, j] = cmax/2
            if (i - centro_x) ** 2 + (j - centro_y) ** 2 <= radio1 ** 2:
                Z[i, j] = cmax
    return Z

def condini3(x, y, cmax):
    """ genera una malla Z, de tamaño x,y con las siguientes condiciones iniciales, cmax en el borde derecho, 0 en los bordes izquierdo, superior e inferior.

    Examples:
        >>> x = np.linspace(0,100,100)
        >>> y = np.linspace(0,200,100)
        >>> cmax = 500
        >>> condini1(x, y, cmax)
        [[0, 0, ..., 500], [0, 0, ..., 0], ..., [0, 0, ..., 500]]

    Args:
        x (array): Arreglo espacial de pasos equidistantes
        y (array): Arreglo espacial de pasos equidistantes
        cmax (float): Variable de calor

    Returns:
        Z (array): Grilla con los valores asignados por las condiciones iniciales
    """
    Z = np.zeros_like(x)
    Z[:, 0] = Z[0, :] = Z[-1, :] = 0
    Z[:, -1] = cmax
    return Z


def act_calor(Z, k, dt, dx, dy):
    """ genera una malla Z_nuevo y calcula sus valores usando el método de diferencias finitas

    Examples:
        >>> a = 1
        >>> b = 2
        >>> m = 100
        >>> x = np.linspace(0,a,m)
        >>> y = np.linspace(0,b,m)
        >>> X, Y = np.meshgrid(x,y)
        >>> Z = (X, Y)
        >>> k = 1e-4
        >>> dt = 1e-4
        >>> dx = a / m
        >>> dy = b / m
        >>> act_calor(Z, k, dt, dx, dy)
        [[0, 0, ..., 0], [0, 1e-8, ..., 0], ..., [0, 0, ..., 0]]

    Args:
        Z (array): Grilla espacial con los valores actuales
        k (float): Constante de difusión
        dt (float): Paso del tiempo
        dx (float): Paso espacial en la coordenada x
        dy (float): Paso espacial en la coordenada y

    Returns:
        Z_nuevo (array): Grilla con los valores calculados usando Diferencias Finitas
    """
    m, n = Z.shape
    Z_nuevo = np.copy(Z)
    alpha_x = k * dt / dx ** 2
    alpha_y = k * dt / dy ** 2
    for i in prange(1, m - 1):
        for j in prange(1, n - 1):
            Z_nuevo[i, j] = Z[i, j] + alpha_x * (Z[i + 1, j] + Z[i - 1, j] - 2 * Z[i, j]) \
                                        + alpha_y * (Z[i, j + 1] + Z[i, j - 1] - 2 * Z[i, j])
    return Z_nuevo

def generarimagen(x, y, Z, t, vmax):
    """ genera una gráfica a partir de los datos suministrados

    Args:
        x (array): Arreglo espacial de pasos equidistantes
        y (array): Arreglo espacial de pasos equidistantes
        Z (array): Matriz que tiene los valores del calor para cada celda
        t (float): Tiempo en el que se tienen los valores de Z
        vmax (float): Calor máximo dado por la condición inicial

    Returns:
        imagen (graph): Gráfica generada a partir de los datos suministrados
    """
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    c = ax.contourf(x, y, Z, cmap='viridis', levels=20, vmin=0, vmax=vmax)
    fig.colorbar(c)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Onda de calor en t={:.2f}s'.format(t))
    fig.canvas.draw()
    imagen = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8').reshape(
        fig.canvas.get_width_height()[::-1] + (3,))
    ax.clear()
    plt.close(fig)
    return imagen


def generardatos(x, y, Z, k, dt, t_inicial, t_final, num_pasos, vmax, dx, dy):
    """ genera todas las imágenes a partir de los datos suministrados

    Args:
        x (array): Arreglo espacial de pasos equidistantes
        y (array): Arreglo espacial de pasos equidistantes
        Z (array): Matriz que tiene los valores del calor para cada celda
        dt (float): Paso de tiempo
        t_inicial (float): Tiempo en el que se empieza a generar las imágenes
        t_final (float): Tiempo en el que termina de generarse las imágenes
        num_pasos (float): Cantidad de imágenes a generar para el gif
        vmax (float): Calor máximo dado por la condición inicial
        dx (float): Paso espacial en la coordenada x
        dy (float): Paso espacial en la coordenada y

    Returns:
        imagenes (array): Gráfica generada a partir de los datos suministrados
    """
    ttotal = t_final - t_inicial
    iteraciones = int(ttotal / dt)
    j = int(iteraciones / num_pasos)
    imagenes = []
    for l in range(iteraciones):
        t = t_inicial + dt * l
        Z = act_calor(Z, k, dt, dx, dy)
        if (l % j) == 0:
            imagen = generarimagen(x, y, Z, t, vmax)
            imagenes.append(imagen)
            progreso = (l+j) * 100 // iteraciones
            progreso_var.set(progreso)
            vent.update_idletasks()
            print(f'Progreso: {progreso}%')
    return imagenes





























