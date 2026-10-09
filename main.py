
import sys
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSlider, QLabel
)
from PySide6.QtCore import Qt
import numpy as np


class Esfera:
    def __init__(self, x, y, z, radio, color = "royalblue"):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.nucleo = pv.Sphere(radius=radio, center=(x, y, z))
        self.actor = None


    def render(self,viewer):
        self.actor = viewer.add_mesh(self.nucleo, color=self.color)

def nivel_electrones(electrones):
    orbitales = [
        (1, 's', 2),
        (2, 's', 2),
        (2, 'p', 6),
        (3, 's', 2),
        (3, 'p', 6),
        (4, 's', 2),
        (3, 'd', 10),
        (4, 'p', 6),
        (5, 's', 2),
        (4, 'd', 10),
        (5, 'p', 6),
        (6, 's', 2),
        (4, 'f', 14),
        (5, 'd', 10),
        (6, 'p', 6),
        (7, 's', 2),
        (5, 'f', 14),
        (6, 'd', 10),
        (7, 'p', 6)
    ]

    niveles = {}

    for n, tipo, capacidad in orbitales:
        if electrones == 0:
            break

        cantidad = min(electrones, capacidad)

        niveles[n] = niveles.get(n, 0) + cantidad
        electrones -= cantidad

    return dict(sorted(niveles.items()))


def fibo_sphere(center, radius, n):
    cx, cy, cz = center

    i = np.arange(0, n)

    z = radius * (1 - (2 * i + 1) / n)

    r_at_z = np.sqrt(radius ** 2 - z ** 2)

    golden_angle = np.pi * (3 - np.sqrt(5))
    phi = i * golden_angle

    x = r_at_z * np.cos(phi)
    y = r_at_z * np.sin(phi)

    points = np.column_stack((x + cx, y + cy, z + cz))

    return points


class Atomo:
    def __init__(self, x, y, z, numero_atomico, radio, distancia):
        self.x = x
        self.y = y
        self.z = z
        self.numero_atomico = numero_atomico
        self.radio = radio
        self.radio_electrones = distancia

    def render(self,viewer):
        Esfera(self.x,self.y,self.z, self.radio+self.radio_electrones//2).render(viewer)
        niveles = nivel_electrones(self.numero_atomico)
        for i in niveles:
            for idx, p in enumerate(fibo_sphere((self.x, self.y, self.z), self.radio_electrones * i +self.radio, niveles[i])):
                Esfera(p[0],p[1] ,p[2] , self.radio,color = [1.0 - i/7,0.0,0.0]).render(viewer)



app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("3D Visualization")
window.resize(1100, 700)

central = QWidget()
layout = QHBoxLayout(central)

# 3D viewport
# Viewport 3D
viewer = QtInteractor(central)
layout.addWidget(viewer.interactor, 4)


Atomo(0,0,0,118,50,900).render(viewer)


viewer.add_axes()
viewer.reset_camera()

# UI controls
panel = QWidget()
controls = QVBoxLayout(panel)

controls.addWidget(QLabel("Sphere Size"))

#slider = QSlider(Qt.Horizontal)
#slider.setRange(10, 300)
#slider.setValue(100)

# def update_size(value):
#     actor.SetScale(value / 100)
#     viewer.render()
#
# slider.valueChanged.connect(update_size)
#controls.addWidget(slider)
#controls.addStretch()

layout.addWidget(panel, 1)

window.setCentralWidget(central)
window.show()

sys.exit(app.exec())
