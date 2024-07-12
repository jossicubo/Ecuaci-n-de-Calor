# Métodos numéricos
Para poder resolver la ecuación de Calor es necesario especificar tanto las condicones iniciales como las condiciones de frontera, de lo contrario la solución de la ecuación no está determinada por lo que conocer estas condiciones es necesario para obtener la solución completa y única.

## Series de Fourier 
La ecuación de calor es posible resolverla mediante series de fourier debido a que las series de Fourier pueden descomponer funciones complejas en funciones sinusoidales más sencillas. Además, como la ecuación de calor es una ecuación diferencial parcial (EDP) lineal, quiere decir que sus soluciones individuales, pueden ser sumadas de manera que también sean una solución.

Para entender mejor la solución de la ecuación de calor es importante mencionar algunas propiedades que tienen las funciones Sinusoidales: seno y coseno

* Son soluciones propias de la ecuación homogénea:

\begin{align}
\frac{d^{2}X }{dx^{2}}=-\lambda X
\end{align}

* Son ortogonales, est facilita la descomposición de funciones complejas en sumas de estas funciones.

### Tomemos el siguiente ejemplo: 
Consideremos una placa rectangular delgada, con longitud a y anchura b cuya tempe-
ratura viene dada por la función $u(x, y, t)$ que depende del tiempo $t ≥ 0$ y de la posición
$(x, y)$. Buscamos determinar la solución $u(x, y, t)$ del problema inicial de frontera de la temperatura de la placa rectangular, que viene dado por el siguiente problema de la ecuación del
calor:
\begin{aligned}
u_{t}=k\nabla ^{2}u & 0 \le x \le  a, & 0\le y \le b   & t\gt 0
\end{aligned}
\begin{aligned}
u(x,y,0) = f(x,y) & 0 \le x \le  a, & 0\le y \le b
\end{aligned}
\begin{aligned}
u_{x}(0,y,t) = 0 & u_{x}(a,y,t) = 0
\end{aligned}

Primero buscamos soluciones no triviales de la parte homogénea del problema inicial de la forma:
$U(x,y,t)=U(x,y)T(t)$ y al sustituir en $u_{t}=k\nabla ^{2}u$  observamos que existe un $\lambda \epsilon\mathbb{R}$ tal que $U(x,y)$ y $T(t)$ satisfacen:

\begin{aligned}
T'+\lambda kT=0
\end{aligned}

\begin{aligned}
\nabla ^{2}+\lambda U =0
\end{aligned}

\begin{aligned}
U_{x}(0,y)=U_{x}(a,y)=0 & & (1)
\end{aligned}

\begin{aligned}
U(x,0)=U(x,b)=0
\end{aligned}


Posteriormente buscamos los valores de $\lambda\epsilon\mathbb{R}$ para los cuales la ecuación (1) tiene soluciones no nulas- Lo que resulta en las EDO:

\begin{aligned}
X''-\mu X = 0, & X'(a)=0
\end{aligned}
\begin{aligned}
Y' + (\lambda + \mu)Y =0 ; & Y(0)=Y(b)=0
\end{aligned}
Posteriormente se realiza:

* Se buscan las soluciones no triviales

* Se aplican las condiciones de frontera dadas al inicio

* Se determina el valor de $\mu$ para las soluciones no nulas

* Con las soluciones de $\mu$ se determinan los $\lambda$ para  las soluciones no nulas, obteniendo que una solución no nula asociada a $\lambda$ = $\lambda_{mn}$ está dada por:
\begin{aligned}
U_{mn}=X_{m}(x)Y_{n}(y) = cos(\frac{m\pi}{a}x)sen(\frac{m\pi}{b}y)
\end{aligned}

Ahora integramos $T'+\lambda kT=0$ para obtener una solución no nula para $\lambda$=$\lambda_{mn}$, así:
\begin{aligned}
T'=-\lambda kT, & \frac{T'}{T}=-\lambda k, & \int_{}^{}\frac{T'}{T}dt =\int_{}^{}-\lambda k dt
\\
ln\left| t \right|=-\lambda kT
\end{aligned}


Y una solución no nula del problema es
\begin{aligned}
T(t)=e^{-\lambda _{mn}kt}
\end{aligned}

Por tanto, la solución del problema es de la forma:
\begin{aligned}
u(x,y,t) = \sum_{m=0}^{\infty }\sum_{n=1}^{\infty }b_{mn}e^{-(\frac{m^{2}}{a^{2}}+\frac{n^{2}}{b^{2}})\pi^{2}kt}cos(\frac{m\pi}{a}x)sen(\frac{n\pi}{b}y)
\end{aligned}

donde las constantes $b_{mn}$ deben escogerse de manera que se cumpla la condición inicial homogénea $u(x,y,0)$=$f(x,y)$ es decir:
\begin{aligned}
f(x,y) = \sum_{m=0}^{\infty }\sum_{n=1}^{\infty }b_{mn}cos(\frac{m\pi}{a}x)sen(\frac{n\pi}{b}y)
\end{aligned}
Y para este caso los coeficientes de la serie de Fourier doble vienen dados por:
\begin{aligned}
b_{0n}& =\frac{4}{ab}\int_{0}^{a}\int_{0}^{b}f(x,y)\operatorname{sen}\Big(\frac{n\pi}{b}y\Big)dxdy, & \mathrm{para~}m=0;
\end{aligned}

\begin{aligned}
b_{mn}&=\frac{4}{ab}\int_{0}^{a}\int_{0}^{b}f(x,y)\cos\left(\frac{m\pi}{a}x\right)\mathrm{sen}\left(\frac{n\pi}{b}y\right)dxdy, & \mathrm{para~}m\geq1. 
\end{aligned}

Y la solución para la placa rectangular es: 
\begin{aligned}
u(x,y,t)=& \frac{1}{2}\sum_{n=1}^{\infty}b_{0n}\mathrm{e}^{-(n^{2}/b^{2})\pi^{2}kt}\operatorname{sen}\left(\frac{n\pi}{b}y\right)+\sum_{m=1}^{\infty}\sum_{n=1}^{\infty}b_{mn}\mathrm{e}^{-(m^{2}/a^{2}+n^{2}/b^{2})\pi^{2}kt}\cos\left(\frac{m\pi}{a}x\right)\mathrm{sen}\left(\frac{n\pi}{b}y\right),
\end{aligned}

Para el ejemplo anterior se utilizó la siguiente referencia:
Martínez, C. V. (s/f). La ecuación del calor. Usc.es. Recuperado el 12 de julio de 2024, de https://minerva.usc.es/xmlui/bitstream/handle/10347/26503/Villar_Mart%C3%ADnez_Cecilia.pdf



## Diferencias Finitas Centrales para la segunda derivada

En la clase de Diferencias Finitas; consideramos derivadas de primer orden, sus errores asociados y distintas metodologías. Podemos utilizar diferencias centrales para aproximar también segundas derivadas. El resultado se obtiene al considerar las diferencias centrales para la primera derivada en el punto $x+(h/2)$ y en el punto $x - (h/2)$:

$$
f'(x + h/2) \approx \frac{f(x + h) - f(x)}{h}, \quad f'(x - h/2) \approx \frac{f(x) - f(x - h)}{h}.
$$

Podemos aplicar diferencias centrales una vez más en en la segunda derivada para obtener nuestra aproximación
\begin{align}
f''(x) &\approx \frac{f'(x + h/2) - f'(h - h/2)}{h} \\
&= \frac{[f(x+h) - f(x)]/h - [f(x) - f(x - h)]/h}{h} \\
&= \frac{f(x + h) - 2f(x) + f(x - h)}{h^2}.
\end{align}






