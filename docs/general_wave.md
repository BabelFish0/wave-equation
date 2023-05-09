# General wave equation simulation

## Structure

[general_wave.py](/src/general_wave.py) is a module containing functions to create and run a 1D wave simulation.

[realtime_wave.py](/src/realtime_wave.py) is an example implementation of this to create a realtime animation of a propegating wave packet on a string. It also demonstrates a classical analogy for Anderson Localization, a dispersion effect in quantum physics.

## Init

Different initial position and velocity functions can be defined in the `Initializer` class. Each of these functions take some shape parameters, the string length, $\Delta x$, and the wave speed; they output an array of initial displacements and velocities for each point on the string at $t = 0$.

## Model

The `Model` class contains all the data and functions relating to the model, allowing it to be totally self contained (so multiple models can be set up and run at the same time).

## Params

To set up a new `Model` object, the `params` dict needs to be populated with parameters for the model and the `init_model()` function needs to be called.

- `useCustomParams()` allows you to specify all the details for the simulated space and the function to call for boundary conditions. It is necessary to manually fill `Model.init_pos` and `Model.init_vel` with the positions and velocities of each of the points on the string. This can be done by setting up an initializer and calling one of the init functions.

- `useDefaultParams()` will set up a default environment and a gaussian wave on the string. There is no need to separately fill `init_pos` or `init_vel`. Note that you can still edit parameters directly in the dict `params` before calling `init_model()`.

`init_model()` can then be called in either case to fill the first two timesteps with data for $t=0$ and implicit values for $t=-1$ (from velocities).

## Computation

This is much the same as in [simple_wave.py](/src/simple_wave.py), see [documentation](/docs/simple_wave.md).

The one addition to this version is tracking energy in the system. This is done simply by finding the extension of the string by looking at the lenth of each displaced segment and comparing it to the original length parameter. `ke()` returns the kinetic energy of a particular segment of string at a particular timestep (the mass of that segment is known and its velocity is obtained using the timestep before and the `delta_t` parameter).

## Extra

Some other functions are included, like $\frac{dy}{dx}, \frac{d^2y}{dx^2}, \frac{d^2y}{dt^2}$ at each $(i, j)$ and `generate_random_sections` and `generate_alternating_sections`, which produce an array with regular sections that either alternate or are random in value. This is used in the example to produce the dispersion on the right half of the figure.

There is also a trigger function, `has_wave_passed()`, which returns `True` when it detects a sign change in $\frac{dy}{dx}$ compared with the timestep before $j$.