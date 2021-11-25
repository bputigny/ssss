#!env python

from solarsystem import planets, m_sun

from numpy.linalg import norm


G = 6.67408e-11


def timestep(dt):
    """
    Update planets position and velocities after one time step (dt: sec)
    """
    nt = 10
    dt = dt / float(nt)
    for name, planet in planets.items():
        for _ in range(nt):
            planet.v += accel(planet.m, planet.x) * dt
            planet.x += planet.v * dt


def fg(m, x):
    ux = x / norm(x)  # nomalized positional vector
    return -ux * G * m_sun * m / norm(x) ** 2


def accel(m, x):
    return fg(m, x) / m

