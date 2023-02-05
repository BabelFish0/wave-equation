# Simple wave equation simulation

## Maths


The displacement of a point on the string at the next timestep is calculated as:

$$
y(x_i, t_{j+1}) = \frac{(\Delta t)^2v^2}{(\Delta x)^2}\left[y(x_{i+1}, t_j)-2y(x_i, t_j)+y(x_i, t_{j+1})\right]-y(x_i, t_{j+1})+2y(x_i, t_j).
$$

The initial position of the string is defined as some function $f(x)$ such as $ae^{-(bx-c)^2}$. The initial velocies are also specified by some other function $g(x)$.

$$ y(x_i, t_0)=f(x_i) $$

$$ \dot{y}(x_i, t_0)=g(x_i) $$

$$ = \frac{y(x_i, t_0)-y(x_i, t_{-1})}{\Delta t} $$

$$ \implies y(x_i, t_{-1}) = f(x_i)-\Delta t g(x_i) $$

In this way a timestep $t_{-1}$ is inferred from the specified initial position and velocity functions. This is used to initialise the first two timesteps in the model and subsequently timesteps have enough information to be calculated normally.

## Images

![Looping animation of single wave](/images/wave_anim_loop.gif)

![Graph version of above example](/images/graph_wave.png)

## Code

- modelling is mostly handled in [simple_wave.py](/src/simple_wave.py)
- matplotlib animation is handled in [animated_wave.py](/src/animated_wave.py)
- various initial position and velocity functions are kept in [pos_vel_init.py](/src/pos_vel_init.py)

[simple_wave.py](/src/simple_wave.py) will generate a plot of all the timesteps if run standalone; however, it is intended to be used as a module for [animated_wave.py](/src/animated_wave.py), where its functions are used to update the model state for each frame. This is what is run to obtain the final output of a realtime or saved animation. In the animated version, the code only stores 3 timesteps at a time as it displays them immediately.