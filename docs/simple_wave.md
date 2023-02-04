# Simple wave equation simulation

## Maths


The displacement of a point on the string at the next timestep is calculated as:

$$
y(x_i, t_{j+1}) = \frac{(\Delta t)^2v^2}{(\Delta x)^2}\left[y(x_{i+1}, t_j)-2y(x_i, t_j)+y(x_i, t_{j+1})\right]-y(x_i, t_{j+1})+2y(x_i, t_j).
$$

The initial position of the string is defined as some function $f(x)$ such as $ae^{-(bx-c)^2}$. The initial velocies are also specified by some other function $g(x)$.

\begin{align}
y(x_i, t=0)=f(x_i)\\
\dot{y}(x_i, t=0)=g(x_i)\\
= \frac{y(x_i, t=0)-y(x_i, t=-1)}{\Delta t}\\
\implies y(i, t=-1) = f(x_i)-\Delta t g(x_i)
\end{align}

In this way a timestep $t=-1$ is inferred from the specified initial position and velocity functions. This is used to initialise the first two timesteps in the model and subsequently timesteps have enough information to be calculated normally.

## Images

![Looping animation of single wave](/images/wave_anim_loop.gif)

![Graph version of above example](/images/graph_wave.png)