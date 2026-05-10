from OpenGL.GL import *
import math

# ─────────────────────────────────────────────
#  LIGHTING SETUP
# ─────────────────────────────────────────────

# Posisi spotlight per lukisan (di atas tiap frame)
PAINTING_LIGHTS = [
    # (GL_LIGHT, posisi)
    (GL_LIGHT1, [-5.5, 4.6, -7.8, 1.0]),   # lukisan kiri dinding depan
    (GL_LIGHT2, [0.0, 4.6, -7.8, 1.0]),   # lukisan tengah dinding depan
    (GL_LIGHT3, [5.5, 4.6, -7.8, 1.0]),   # lukisan kanan dinding depan
    (GL_LIGHT4, [-7.8, 4.6,  0.0, 1.0]),   # lukisan dinding kiri
    (GL_LIGHT5, [7.8, 4.6,  0.0, 1.0]),   # lukisan dinding kanan
]


def setup_lighting():
    """Inisialisasi semua cahaya dalam galeri."""

    # Ambient global redup — suasana galeri malam
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.12, 0.10, 0.08, 1.0])
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

    # GL_LIGHT0 — lampu langit-langit utama (point light, hangat)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 4.8, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.80, 0.75, 0.65, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.50, 0.50, 0.50, 1.0])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION,  1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION,    0.04)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.005)

    # GL_LIGHT1–5 — spotlight per lukisan
    for light, pos in PAINTING_LIGHTS:
        glEnable(light)
        glLightfv(light, GL_POSITION,       pos)
        glLightfv(light, GL_DIFFUSE,        [1.0, 0.96, 0.82, 1.0])
        glLightfv(light, GL_SPECULAR,       [0.6, 0.6, 0.5, 1.0])
        glLightfv(light, GL_SPOT_DIRECTION, [0.0, -1.0, 0.05])
        glLightf(light, GL_SPOT_CUTOFF,    28.0)
        glLightf(light, GL_SPOT_EXPONENT,  12.0)
        glLightf(light, GL_CONSTANT_ATTENUATION,  1.0)
        glLightf(light, GL_LINEAR_ATTENUATION,    0.05)
        glLightf(light, GL_QUADRATIC_ATTENUATION, 0.01)


def set_material_marble():
    """Material marmer untuk patung."""
    glMaterialfv(GL_FRONT, GL_AMBIENT,   [0.20, 0.19, 0.18, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   [0.85, 0.83, 0.80, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR,  [0.70, 0.70, 0.68, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 60.0)


def set_material_bronze():
    """Material perunggu untuk patung abstrak."""
    glMaterialfv(GL_FRONT, GL_AMBIENT,   [0.21, 0.13, 0.05, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   [0.71, 0.43, 0.18, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR,  [0.39, 0.27, 0.17, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 25.0)


def set_material_wood():
    """Material kayu untuk frame dan furnitur."""
    glMaterialfv(GL_FRONT, GL_AMBIENT,   [0.15, 0.09, 0.03, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   [0.55, 0.35, 0.10, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR,  [0.20, 0.15, 0.08, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 8.0)


def set_material_default():
    """Reset ke material default."""
    glMaterialfv(GL_FRONT, GL_AMBIENT,   [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR,  [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
