"""
Simple Solar System Simulation: User interface module
"""
from model import planets, timestep

import platform
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
        self.show_legend = True
        self.unit = 0

    def on_press(self, event):
        one_day = 3600 * 24
        if event.key.isspace():
            self.pause ^= True
        elif event.key == "enter":
            self.show_labels ^= True
        elif event.key == "t":
            self.show_legend ^= True
        elif event.key == "u":
            self.unit = (self.unit + 1) % len(units)
            r = get_viz_r()
            ax.set_xlim([-1.1 * r, 1.1 * r])
            ax.set_ylim([-1.1 * r, 1.1 * r])
        elif event.key == "left" or event.key == "down":
            if self.dt > one_day / 4.0:
                self.dt -= one_day / 4.0
        elif event.key == "right" or event.key == "up":
            if self.dt < 7 * one_day:
                self.dt += one_day / 4.0


def update(i, lines):
    for t in ax.texts:
        t.remove()
    if ctrl.show_labels:
        ax.text(0, 0, "sun")
    dt = ctrl.dt
    if ctrl.pause:
        dt = 0
    timestep(dt)
    ctrl.datetime = ctrl.datetime + TimeDelta(dt, format="sec")
    n = 1
    lines[0].set_data(0, 0)
    vel = f"{'sun':7}: {0:4.2e} m/s"
    lines[0].set_label(vel)
    for name in planets.keys():
        lines[n].set_data(
            planets[name].x[0] / units[ctrl.unit]["scale"],
            planets[name].x[1] / units[ctrl.unit]["scale"],
        )
        vel = f"{name:7}: {norm(planets[name].v):4.2e} m/s"
        lines[n].set_label(vel)
        if ctrl.show_labels:
            t = ax.text(
                planets[name].x[0] / units[ctrl.unit]["scale"],
                planets[name].x[1] / units[ctrl.unit]["scale"],
                name,
            )
        n += 1
    date = ctrl.datetime.to_value("iso", subfmt="date")
    plt.title(f"Date: {date}, dt: {ctrl.dt/24/3600:.2f} days")
    ax.set_xlabel(units[ctrl.unit]["name"])
    ax.set_ylabel(units[ctrl.unit]["name"])

    if ctrl.show_legend:
        ax.legend(
            loc="lower center", prop={"family": "monospace"}, ncol=3,
        )
    elif ax.get_legend():
        ax.get_legend().remove()

    return (lines,)


def get_viz_r():
    r = 0
    for p in planets.keys():
        pr = norm(planets[p].x) / units[ctrl.unit]["scale"]
        if r < pr:
            r = pr
    return r


if __name__ == "__main__":

    print(platform.system())

    plt.style.use("dark_background")

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot()
    ax.set_xlabel("AU")
    ax.set_ylabel("AU")

    ctrl = Controller()

    lines = []
    (line,) = ax.plot([0], [0], ".", color="y", label="sun")
    texts = ax.text(0, 0, "sun")
    lines.append(line)
    for name in planets.keys():
        (line,) = ax.plot(planets[name].x, ".", label=name)
        texts = ax.text(0, 0, name)
        lines.append(line)
    r = get_viz_r()
    ax.set_xlim([-1.1 * r, 1.1 * r])
    ax.set_ylim([-1.1 * r, 1.1 * r])

    fig.canvas.mpl_connect("key_press_event", ctrl.on_press)

    blit = True
    if platform.system() == "Darwin":
        blit = False
    ani = FuncAnimation(
        fig, update, blit=blit, interval=5, repeat=False, fargs=(lines,)
    )

    plt.show()
