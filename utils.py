import math
from OpenGL.GL import *
from OpenGL.GLUT import *


def draw_quad(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, nx=0, ny=1, nz=0):
    glBegin(GL_QUADS)
    glNormal3f(nx, ny, nz)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y2, z2)
    glVertex3f(x3, y3, z3)
    glVertex3f(x4, y4, z4)
    glEnd()


def draw_box(cx, cy, cz, w, h, d):
    """Kotak solid dengan normal per muka (untuk lighting benar)."""
    hw, hh, hd = w/2, h/2, d/2
    x0, x1 = cx-hw, cx+hw
    y0, y1 = cy-hh, cy+hh
    z0, z1 = cz-hd, cz+hd

    faces = [
        # normal,         4 vertex
        ((0, 0, 1),  [(x0, y0, z1), (x1, y0, z1),
         (x1, y1, z1), (x0, y1, z1)]),  # depan
        ((0, 0, -1), [(x1, y0, z0), (x0, y0, z0),
         (x0, y1, z0), (x1, y1, z0)]),  # belakang
        ((1, 0, 0),  [(x1, y0, z1), (x1, y0, z0),
         (x1, y1, z0), (x1, y1, z1)]),  # kanan
        ((-1, 0, 0), [(x0, y0, z0), (x0, y0, z1),
         (x0, y1, z1), (x0, y1, z0)]),  # kiri
        ((0, 1, 0),  [(x0, y1, z1), (x1, y1, z1),
         (x1, y1, z0), (x0, y1, z0)]),  # atas
        ((0, -1, 0), [(x0, y0, z0), (x1, y0, z0),
         (x1, y0, z1), (x0, y0, z1)]),  # bawah
    ]
    for (nx, ny, nz), verts in faces:
        glBegin(GL_QUADS)
        glNormal3f(nx, ny, nz)
        for v in verts:
            glVertex3f(*v)
        glEnd()


def draw_cylinder(base_r, top_r, height, slices=16, capped=True):
    """Silinder / cone di origin, memanjang ke +Y."""
    step = 2*math.pi / slices
    # Selimut
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(slices+1):
        a = i * step
        ca, sa = math.cos(a), math.sin(a)
        # Normal miring sesuai taper
        slope = (base_r - top_r) / height
        nx = ca / math.sqrt(1 + slope*slope)
        nz = sa / math.sqrt(1 + slope*slope)
        ny = slope / math.sqrt(1 + slope*slope)
        glNormal3f(nx, ny, nz)
        glVertex3f(base_r*ca, 0,      base_r*sa)
        glVertex3f(top_r*ca,  height, top_r*sa)
    glEnd()
    if capped:
        # Tutup bawah
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, -1, 0)
        glVertex3f(0, 0, 0)
        for i in range(slices+1):
            a = -i*step
            glVertex3f(base_r*math.cos(a), 0, base_r*math.sin(a))
        glEnd()
        # Tutup atas
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 1, 0)
        glVertex3f(0, height, 0)
        for i in range(slices+1):
            a = i*step
            glVertex3f(top_r*math.cos(a), height, top_r*math.sin(a))
        glEnd()


def draw_sphere_manual(r, slices=18, stacks=18):
    """Sphere manual tanpa glutSolidSphere untuk kontrol warna per vertex."""
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + i/stacks)
        lat1 = math.pi * (-0.5 + (i+1)/stacks)
        z0, zr0 = math.sin(lat0), math.cos(lat0)
        z1, zr1 = math.sin(lat1), math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices+1):
            lng = 2*math.pi * j/slices
            c, s = math.cos(lng), math.sin(lng)
            glNormal3f(c*zr0, z0, s*zr0)
            glVertex3f(r*c*zr0, r*z0, r*s*zr0)
            glNormal3f(c*zr1, z1, s*zr1)
            glVertex3f(r*c*zr1, r*z1, r*s*zr1)
        glEnd()


def draw_torus(inner_r, outer_r, sides=20, rings=30):
    """Torus manual."""
    for i in range(rings):
        glBegin(GL_QUAD_STRIP)
        for j in range(sides+1):
            for k in range(2):
                s = (i + k) % rings
                t = j % sides
                a_s = 2*math.pi * s / rings
                a_t = 2*math.pi * t / sides
                cs, ss = math.cos(a_s), math.sin(a_s)
                ct, st = math.cos(a_t), math.sin(a_t)
                x = (outer_r + inner_r*ct) * cs
                y = inner_r * st
                z = (outer_r + inner_r*ct) * ss
                nx = ct*cs
                ny = st
                nz = ct*ss
                glNormal3f(nx, ny, nz)
                glVertex3f(x, y, z)
        glEnd()


def draw_text_3d(x, y, z, text, scale=0.001):
    """Render string GLUT bitmap di posisi 3D."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)
    for ch in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
    glPopMatrix()


def draw_bitmap_text(x, y, text, font=None):
    """Teks 2D di koordinat window (untuk HUD)."""
    if font is None:
        font = GLUT_BITMAP_HELVETICA_18
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
