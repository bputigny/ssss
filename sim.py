"""
Simple Solar System Simulation: User interface module
"""
from model import planets, timestep

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from astropy.time import Time, TimeDelta

from numpy.linalg import norm

units = []
units.append({"name": "UA", "scale": 149597870700.0})
units.append({"name": "m", "scale": 1.0})


class Controller:
    def __init__(self):
        self.datetime = Time.now()
        self.dt = 3600 * 24
        self.pause = True
        self.show_labels = True
        self.unit = 0

    def on_press(self, event):
        one_day = 3600 * 24
        if event.key.isspace():
            self.pause ^= True
        elif event.key == "enter":
            self.show_labels ^= True
        elif event.key == "u":
            self.unit = (self.unit + 1) % len(units)
            r = get_viz_r()
            plt.xlim([-1.1 * r, 1.1 * r])
            plt.ylim([-1.1 * r, 1.1 * r])
        elif event.key == "left" or event.key == "down":
            if self.dt > one_day / 4.0:
                self.dt -= one_day / 4.0
        elif event.key == "right" or event.key == "up":
            if self.dt < 7 * one_day:
                self.dt += one_day / 4.0


def update(i):
    xs = [0]
    ys = [0]
    for t in ax.texts:
        t.remove()
    if ctrl.show_labels:
        ax.text(0, 0, "sun")
    dt = ctrl.dt
    if ctrl.pause:
        dt = 0
    timestep(dt)
    ctrl.datetime = ctrl.datetime + TimeDelta(dt, format="sec")
    for name in planets.keys():
        xs.append(planets[name].x[0] / units[ctrl.unit]["scale"])
        ys.append(planets[name].x[1] / units[ctrl.unit]["scale"])
        if ctrl.show_labels:
            t = ax.text(
                planets[name].x[0] / units[ctrl.unit]["scale"],
                planets[name].x[1] / units[ctrl.unit]["scale"],
                name,
            )
    line.set_data(xs, ys)
    date = ctrl.datetime.to_value("iso", subfmt="date")
    plt.title(f"Date: {date}, dt: {ctrl.dt/24/3600:.2f} days")
    ax.set_xlabel(units[ctrl.unit]["name"])
    ax.set_ylabel(units[ctrl.unit]["name"])
    return (line,)


def get_viz_r():
    r = 0
    for p in planets.keys():
        pr = norm(planets[p].x) / units[ctrl.unit]["scale"]
        if r < pr:
            r = pr
    return r


if __name__ == "__main__":

    plt.style.use("dark_background")

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("AU")
    ax.set_ylabel("AU")
    # ax.axis("off")

    ctrl = Controller()

    (line,) = ax.plot([0], [0], ".", color="w")
    texts = ax.text(0, 0, "sun")
    r = get_viz_r()
    plt.xlim([-1.1 * r, 1.1 * r])
    plt.ylim([-1.1 * r, 1.1 * r])

    fig.canvas.mpl_connect("key_press_event", ctrl.on_press)

    ani = FuncAnimation(fig, update, blit=False, interval=2, repeat=False)

    plt.show()
