"""
Simple Solar System Simulation: User interface module
"""
from model import planets, timestep

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from astropy.time import Time, TimeDelta

from numpy.linalg import norm


class Controller:
    def __init__(self):
        self.datetime = Time.now()
        self.dt = 5e4
        self.pause = True
        self.show_labels = True

    def on_press(self, event):
        if event.key.isspace():
            self.pause ^= True
        elif event.key == "enter":
            self.show_labels ^= True
        elif event.key == "left" or event.key == "down":
            if self.dt > 1e4:
                self.dt -= 1e4
        elif event.key == "right" or event.key == "up":
            if self.dt < 5e5:
                self.dt += 1e4


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
        xs.append(planets[name].x[0])
        ys.append(planets[name].x[1])
        if ctrl.show_labels:
            t = ax.text(planets[name].x[0], planets[name].x[1], name)
    line.set_data(xs, ys)
    date = ctrl.datetime.to_value("iso", subfmt="date")
    plt.title(f"{date}, dt: {ctrl.dt/24/3600:.2f} days")
    return (line,)


if __name__ == "__main__":

    plt.style.use("dark_background")

    fig = plt.figure()
    ax = fig.add_subplot()
    # ax.axis("off")
    (line,) = ax.plot([0], [0], ".", color="w")
    texts = ax.text(0, 0, "Sun")
    r = 0
    for p in planets.keys():
        pr = norm(planets[p].x)
        if r < pr:
            r = pr
    plt.xlim([-1.1 * r, 1.1 * r])
    plt.ylim([-1.1 * r, 1.1 * r])

    ctrl = Controller()

    fig.canvas.mpl_connect("key_press_event", ctrl.on_press)

    ani = FuncAnimation(fig, update, blit=False, interval=5, repeat=False)

    plt.show()
