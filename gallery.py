import math
from OpenGL.GL import *
from utils import draw_box, draw_cylinder

# ─────────────────────────────────────────────
#  RUANGAN GALERI
# ─────────────────────────────────────────────

ROOM_W = 16.0   # lebar total
ROOM_H = 5.2   # tinggi
ROOM_D = 16.0   # kedalaman


def draw_room():
    _draw_floor()
    _draw_ceiling()
    _draw_walls()
    _draw_pillars()
    _draw_benches()
    _draw_entrance_arch()
    _draw_ceiling_lights()
    _draw_baseboard()


# ── Lantai ────────────────────────────────────
def _draw_floor():
    hw = ROOM_W/2
    hd = ROOM_D/2
    tile = 1.0   # ukuran ubin

    for xi in range(int(-hw), int(hw)):
        for zi in range(int(-hd), int(hd)):
            # Pola chequerboard parquet
            if (xi + zi) % 2 == 0:
                glColor3f(0.52, 0.36, 0.18)
            else:
                glColor3f(0.44, 0.30, 0.13)
            x0, x1 = xi*tile, (xi+1)*tile
            z0, z1 = zi*tile, (zi+1)*tile
            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0)
            glVertex3f(x0, 0, z0)
            glVertex3f(x1, 0, z0)
            glVertex3f(x1, 0, z1)
            glVertex3f(x0, 0, z1)
            glEnd()

    # Garis nat ubin (tipis, sedikit di atas lantai)
    glColor3f(0.30, 0.22, 0.10)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    for xi in range(int(-hw), int(hw)+1):
        glVertex3f(xi, 0.001, -hd)
        glVertex3f(xi, 0.001,  hd)
    for zi in range(int(-hd), int(hd)+1):
        glVertex3f(-hw, 0.001, zi)
        glVertex3f(hw, 0.001, zi)
    glEnd()


# ── Langit-langit ─────────────────────────────
def _draw_ceiling():
    hw = ROOM_W/2
    hd = ROOM_D/2
    h = ROOM_H

    # Panel utama
    glColor3f(0.92, 0.90, 0.87)
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-hw, h, -hd)
    glVertex3f(hw, h, -hd)
    glVertex3f(hw, h,  hd)
    glVertex3f(-hw, h,  hd)
    glEnd()

    # Lis langit-langit (border panel)
    glColor3f(0.80, 0.78, 0.75)
    _draw_ceiling_molding(hw, hd, h)


def _draw_ceiling_molding(hw, hd, h):
    t = 0.15  # tebal lis
    d = 0.12
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    # Lis 4 sisi (segitiga kecil di pojok langit-langit)
    strips = [
        [(-hw, h-d, -hd), (hw, h-d, -hd), (hw, h, -hd+t), (-hw, h, -hd+t)],
        [(-hw, h-d,  hd), (hw, h-d,  hd), (hw, h,  hd-t), (-hw, h,  hd-t)],
        [(-hw, h-d, -hd), (-hw, h-d,  hd), (-hw+t, h,  hd), (-hw+t, h, -hd)],
        [(hw, h-d, -hd), (hw, h-d,  hd), (hw-t, h,  hd), (hw-t, h, -hd)],
    ]
    for s in strips:
        for v in s:
            glVertex3f(*v)
    glEnd()


# ── Dinding ───────────────────────────────────
def _draw_walls():
    hw = ROOM_W/2
    hd = ROOM_D/2
    h = ROOM_H

    # Warna dinding: krem hangat
    wall_color = (0.86, 0.83, 0.78)
    accent_color = (0.78, 0.74, 0.68)

    # Dinding belakang (Z = -hd)
    glColor3f(*wall_color)
    _wall_quad(-hw, 0, -hd,  hw, h, -hd, nx=0, nz=1)

    # Dinding depan (Z = +hd) — ada pintu masuk di tengah
    glColor3f(*wall_color)
    # Kiri pintu
    _wall_quad(-hw, 0,  hd, -1.5, h,  hd, nx=0, nz=-1)
    # Kanan pintu
    _wall_quad(1.5, 0, hd,  hw,  h,  hd, nx=0, nz=-1)
    # Atas pintu
    _wall_quad(-1.5, 2.8, hd, 1.5, h, hd, nx=0, nz=-1)

    # Dinding kiri (X = -hw)
    glColor3f(*accent_color)
    _wall_quad(-hw, 0, -hd, -hw, h,  hd, nx=1, nz=0)

    # Dinding kanan (X = +hw)
    glColor3f(*accent_color)
    _wall_quad(hw, 0, -hd,  hw, h,  hd, nx=-1, nz=0)

    # Dado (panel bawah dinding — warna lebih gelap)
    glColor3f(0.70, 0.64, 0.56)
    _draw_dado(hw, hd, h)


def _wall_quad(x1, y1, z1, x2, y2, z2, nx=0, nz=0):
    glBegin(GL_QUADS)
    glNormal3f(nx, 0, nz)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y1, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x1, y2, z1)
    glEnd()


def _draw_dado(hw, hd, h):
    """Panel bawah dinding setinggi 0.9m."""
    dado_h = 0.9
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    # Dinding belakang
    glVertex3f(-hw, 0, -hd+0.02)
    glVertex3f(hw, 0, -hd+0.02)
    glVertex3f(hw, dado_h, -hd+0.02)
    glVertex3f(-hw, dado_h, -hd+0.02)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    # Dinding kiri
    glVertex3f(-hw+0.02, 0, -hd)
    glVertex3f(-hw+0.02, 0,  hd)
    glVertex3f(-hw+0.02, dado_h, hd)
    glVertex3f(-hw+0.02, dado_h, -hd)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    # Dinding kanan
    glVertex3f(hw-0.02, 0, -hd)
    glVertex3f(hw-0.02, 0,  hd)
    glVertex3f(hw-0.02, dado_h, hd)
    glVertex3f(hw-0.02, dado_h, -hd)
    glEnd()

    # Lis dado (strip tipis di atas dado)
    glColor3f(0.60, 0.55, 0.48)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex3f(-hw, dado_h, -hd+0.02)
    glVertex3f(hw, dado_h, -hd+0.02)
    glVertex3f(-hw+0.02, dado_h, -hd)
    glVertex3f(-hw+0.02, dado_h, hd)
    glVertex3f(hw-0.02, dado_h, -hd)
    glVertex3f(hw-0.02, dado_h, hd)
    glEnd()


# ── Pilar ─────────────────────────────────────
def _draw_pillars():
    """4 pilar dekoratif di sudut area tengah."""
    positions = [(-3.5, 0, -3.5), (3.5, 0, -3.5),
                 (-3.5, 0,  3.5), (3.5, 0,  3.5)]
    for px, py, pz in positions:
        glPushMatrix()
        glTranslatef(px, 0, pz)

        # Badan pilar
        glColor3f(0.88, 0.86, 0.82)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        draw_cylinder(0.18, 0.15, ROOM_H - 0.4, slices=12)
        glPopMatrix()

        # Kapital (kepala pilar)
        glColor3f(0.80, 0.78, 0.74)
        draw_box(0, ROOM_H-0.4, 0, 0.42, 0.4, 0.42)

        # Basis pilar
        glColor3f(0.80, 0.78, 0.74)
        draw_box(0, 0.1, 0, 0.42, 0.2, 0.42)

        glPopMatrix()


# ── Bangku pengunjung ─────────────────────────
def _draw_benches():
    bench_positions = [
        (0.0, 0,  0.0),   # tengah
        (-5.0, 0,  0.0),   # kiri
        (5.0, 0,  0.0),   # kanan
    ]
    for bx, by, bz in bench_positions:
        glPushMatrix()
        glTranslatef(bx, 0, bz)
        _draw_single_bench()
        glPopMatrix()


def _draw_single_bench():
    # Dudukan
    glColor3f(0.40, 0.25, 0.08)
    draw_box(0, 0.44, 0, 1.6, 0.08, 0.45)

    # 4 kaki
    leg_color = (0.30, 0.18, 0.06)
    glColor3f(*leg_color)
    for lx in [-0.65, 0.65]:
        for lz in [-0.15, 0.15]:
            draw_box(lx, 0.22, lz, 0.07, 0.44, 0.07)

    # Sandaran
    glColor3f(0.40, 0.25, 0.08)
    draw_box(0, 0.72, 0.17, 1.6, 0.08, 0.06)
    # Tiang sandaran
    for lx in [-0.65, 0.65]:
        glColor3f(*leg_color)
        draw_box(lx, 0.60, 0.17, 0.06, 0.36, 0.06)


# ── Pintu masuk ───────────────────────────────
def _draw_entrance_arch():
    hd = ROOM_D/2
    # Kusen
    glColor3f(0.55, 0.38, 0.18)
    # Atas
    draw_box(0, 3.05, hd, 3.2, 0.25, 0.18)
    # Kiri
    draw_box(-1.65, 1.4, hd, 0.18, 2.8, 0.18)
    # Kanan
    draw_box(1.65, 1.4, hd, 0.18, 2.8, 0.18)

    # Lengkungan arch (segmen)
    glColor3f(0.50, 0.34, 0.15)
    cx, cy = 0, 2.8
    r = 1.5
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, -1)
    glVertex3f(cx, cy, hd)
    for i in range(19):
        a = math.pi * i / 18
        glVertex3f(cx + r*math.cos(a), cy + r*0.4*math.sin(a), hd)
    glEnd()


# ── Armatur lampu langit-langit ───────────────
def _draw_ceiling_lights():
    """Armatur lampu dekoratif (visual saja, source cahaya di lighting.py)."""
    positions = [(-5.5, ROOM_H, -7.5), (0, ROOM_H, -7.5), (5.5, ROOM_H, -7.5),
                 (-7.5, ROOM_H, 0),    (7.5, ROOM_H, 0)]
    for lx, ly, lz in positions:
        glPushMatrix()
        glTranslatef(lx, ly, lz)
        # Dudukan di langit-langit
        glColor3f(0.7, 0.7, 0.7)
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        draw_cylinder(0.06, 0.06, 0.12, 8)
        glPopMatrix()
        # Kepala lampu (kerucut terbalik)
        glColor3f(0.85, 0.84, 0.80)
        glPushMatrix()
        glTranslatef(0, -0.12, 0)
        glRotatef(90, 1, 0, 0)
        draw_cylinder(0.14, 0.06, 0.18, 12)
        glPopMatrix()
        # Titik cahaya (bola kecil kuning)
        glColor3f(1.0, 0.98, 0.85)
        glPushMatrix()
        glTranslatef(0, -0.3, 0)
        from OpenGL.GLUT import glutSolidSphere
        glutSolidSphere(0.05, 8, 8)
        glPopMatrix()
        glPopMatrix()


# ── Alas dinding (baseboard) ──────────────────
def _draw_baseboard():
    hw = ROOM_W/2
    hd = ROOM_D/2
    glColor3f(0.65, 0.58, 0.50)
    h = 0.12
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-hw, 0, -hd+0.01)
    glVertex3f(hw, 0, -hd+0.01)
    glVertex3f(hw,  h, -hd+0.01)
    glVertex3f(-hw, h, -hd+0.01)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glVertex3f(-hw+0.01, 0, -hd)
    glVertex3f(-hw+0.01, 0,  hd)
    glVertex3f(-hw+0.01, h,  hd)
    glVertex3f(-hw+0.01, h, -hd)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glVertex3f(hw-0.01, 0, -hd)
    glVertex3f(hw-0.01, 0,  hd)
    glVertex3f(hw-0.01, h,  hd)
    glVertex3f(hw-0.01, h, -hd)
    glEnd()
