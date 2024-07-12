# Ecuación de Calor en Dos Dimensiones 

La ecuación de calor es una ecuación en derivadas parciales, la cual describe cómo la temperatura evoluciona y se distribuye en el tiempo, en nuestro caso de estudio, en una región bidimensional.  Es utilizada en física e ingeniería para modelar la transferencia de calor y describe la teoría de la difusión térmica. La difusión térmica describe cómo se transfiere el calor dentro de un material, debido a diferencias de temperatura del mismo, mediante la conducción térmica, debido a un gradiente de temperatura el cual, con base en la Ley de Fourier, es proporcional a la tasa de flujo de calor en un material.
Además, la difusión térmica se da debido a que el calor tiende a moverse de regiones de mayor temperatura a regiones de baja temperatura, esto para alcanzar el equilibrio térmico.
Viene dada por la siguiente ecuación:

\begin{align}
\frac{\partial u}{\partial x} = c^{2}\left[ \frac{\partial^{2} u}{\partial x^{2}}+ \frac{\partial^{2}u }{\partial y^{2}}\right]
\end{align}


Para resolver la ecuación de Calor es necesario contar con condiciones de contorno y condiciones iniciales:

### Condiciones de Contorno:
 Fijan la temperatura o el flujo de calor en los bordes de la placa.

### Condiciones Iniciales:
Se refiere a la función que representa cómo se distribuye la temperatura en el tiempo $t = 0$, es decir: $u(x,y,t) = f(x,y)$

### ¿Cómo se interpreta físicamente?
Puede imaginar una placa metálica acotada por las regiones x $\epsilon$ $[0, a]$ y x $\epsilon$ $[0, b]$  bajo condiciones ideales; es decir sin fuentes de energía externa, capacidad calorífica uniforme y aislamiento perfecto. Si al inicio la placa tiene una temperatura no uniforme, la ecuación de calor nos permite predecir cómo la temperatura alcanzará el estado de equilibrio

