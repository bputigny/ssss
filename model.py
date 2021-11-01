#!env python

from solarsystem import planets, m_sun

from numpy.linalg import norm


G = 6.67408e-11


def fg(m, x):
    ux = x / norm(x)  # nomalized positional vector
    return -ux * G * m_sun * m / norm(x) ** 2


def accel(m, x):
    return fg(m, x) / m


def timestep(dt):
    """
    Update planets position and velocities after one time step (dt: sec)
    """
    for name in planets.keys():
        planets[name].v += accel(planets[name].m, planets[name].x) * dt
        planets[name].x += planets[name].v * dt
