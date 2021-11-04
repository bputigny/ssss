#!env python

from astropy.time import Time, TimeDelta
from astropy.coordinates import get_body, HeliocentricTrueEcliptic
import numpy as np
from numpy.linalg import norm
import yaml


def get_body_coord(name, t):
    """
    Return body position (in heliocentric cartesian coordinates) at time t (query astropy)
    """
    body = get_body(name, t)
    body = body.transform_to(HeliocentricTrueEcliptic())
    lon = body.lon
    lat = body.lat
    R = body.distance

    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)

    return np.asarray([x.m, y.m, z.m], dtype=np.float64)


def get_body_vel(name, t):
    """
    Return body velocity vector with finite difference (dt = 1sec)
    """
    x0 = get_body_coord(name, t)
    x1 = get_body_coord(name, t + TimeDelta(1, format="sec"))
    return x1 - x0


t = Time.now()

with open("masses.yaml") as f:
    masses = yaml.safe_load(f)


class Planet:
    def __init__(self, x, v, m):
        self.x = x
        self.v = v
        self.m = m


class Body:
    def __init__(self, name, mass, t=None):
        if t is None:
            t = Time.now()
        self.name = name
        self.mass = mass
        self.x = get_body_coord(name, t)
        self.v = get_body_vel(name, t)
        # Force sun to center and 0 out velocity
        if name == "sun":
            self.x[:] = np.zeros((3))
            self.v[:] = np.zeros((3))
        print(
            f"{name:10}: mass: {self.mass:10.2e} kg, velocity: {norm(self.v):10.2e} m/s"
        )


solarsystem = {}
for b in masses.keys():
    solarsystem[b] = Body(b, float(masses[b]))


planets = {}
for name in solarsystem.keys():
    if name != "sun":
        x = solarsystem[name].x
        v = solarsystem[name].v
        m = solarsystem[name].mass
        planets[name] = Planet(x, v, m)

m_sun = solarsystem["sun"].mass
