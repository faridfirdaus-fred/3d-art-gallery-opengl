import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from utils import draw_box, draw_cylinder, draw_torus, draw_sphere_manual, draw_text_3d

# ─────────────────────────────────────────────
#  PATUNG — semua full procedural (primitif OpenGL)
# ─────────────────────────────────────────────

# (nama, posisi, fungsi_draw, deskripsi)
SCULPTURES = [
    ("Venus",         (-4.5, 0, 1.5),  'draw_bust',
     "Dada wanita klasik dengan detail fitur manusia\nyang elegan dan proporsional."),
    ("Abstract Form", (0.0, 0, 1.5),  'draw_abstract',
     "Patung modern abstrak dengan torus, cone, dan sphere\nyang melayang dan berputar."),
    ("The Thinker",   (4.5, 0, 1.5),  'draw_thinker',
     "Seorang pria duduk sedang berpikir\ndengan postur yang penuh kontemplasi."),
]


def draw_all_sculptures(anim_angle):
    for (title, pos, style, desc) in SCULPTURES:
        x, y, z = pos
        glPushMatrix()
        glTranslatef(x, y, z)

        draw_pedestal()
        draw_pedestal_label(title)

        glTranslatef(0, 0.85, 0)   # naik ke atas pedestal

        # Patung abstrak berputar perlahan
        if style == 'draw_abstract':
            glRotatef(anim_angle, 0, 1, 0)

        {
            'draw_bust':     draw_bust,
            'draw_abstract': draw_abstract,
            'draw_thinker':  draw_thinker,
        }[style]()

        glPopMatrix()


def get_sculpture(idx):
    """Ambil data sculpture berdasarkan index."""
    if 0 <= idx < len(SCULPTURES):
        title, pos, style, desc = SCULPTURES[idx]
        return {
            'title': title, 'pos': pos, 'style': style, 'desc': desc
        }
    return None


# ── Alas (Pedestal) ───────────────────────────
def draw_pedestal():
    from lighting import set_material_marble
    set_material_marble()

    # Badan utama
    glColor3f(0.88, 0.86, 0.83)
    draw_box(0, 0.40, 0, 0.52, 0.80, 0.52)

    # Lis bawah
    glColor3f(0.78, 0.76, 0.73)
    draw_box(0, 0.06, 0, 0.60, 0.12, 0.60)

    # Lis atas
    glColor3f(0.78, 0.76, 0.73)
    draw_box(0, 0.80, 0, 0.58, 0.10, 0.58)

    # Lis kapital tengah
    glColor3f(0.82, 0.80, 0.77)
    draw_box(0, 0.84, 0, 0.55, 0.06, 0.55)

    from lighting import set_material_default
    set_material_default()


def draw_pedestal_label(title):
    """Ukiran nama di depan pedestal."""
    glColor3f(0.40, 0.38, 0.35)
    ts = 0.00042
    tw = len(title) * 104.76 * ts
    draw_text_3d(-tw/2, 0.35, 0.27, title, scale=ts)


# ── Patung 1: Dada / Bust ─────────────────────
def draw_bust():
    """Bust manusia klasik dari silinder + sphere."""
    from lighting import set_material_marble
    set_material_marble()
    glColor3f(0.90, 0.88, 0.85)

    # Bahu (silinder lebar pipih)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.28, 0.22, 0.18, 16)
    glPopMatrix()

    # Dada
    glPushMatrix()
    glTranslatef(0, 0.18, 0)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.20, 0.16, 0.22, 16)
    glPopMatrix()

    # Leher
    glPushMatrix()
    glTranslatef(0, 0.40, 0.02)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.085, 0.095, 0.20, 12)
    glPopMatrix()

    # Kepala (sphere sedikit oval)
    glPushMatrix()
    glTranslatef(0, 0.68, 0.02)
    glScalef(1.0, 1.15, 0.95)
    glutSolidSphere(0.19, 20, 20)
    glPopMatrix()

    # Hidung
    glPushMatrix()
    glTranslatef(0, 0.66, 0.20)
    glRotatef(-80, 1, 0, 0)
    draw_cylinder(0.022, 0.008, 0.07, 8)
    glPopMatrix()

    # Alis kiri
    _brow(-0.07, 0.76, 0.165, rot=8)
    # Alis kanan
    _brow(0.07, 0.76, 0.165, rot=-8)

    # Mata kiri (lekukan kecil)
    glPushMatrix()
    glTranslatef(-0.07, 0.68, 0.175)
    glColor3f(0.55, 0.52, 0.50)
    glutSolidSphere(0.025, 8, 8)
    glPopMatrix()

    # Mata kanan
    glPushMatrix()
    glTranslatef(0.07, 0.68, 0.175)
    glColor3f(0.55, 0.52, 0.50)
    glutSolidSphere(0.025, 8, 8)
    glPopMatrix()

    # Bibir (cylinder pipih)
    glColor3f(0.82, 0.79, 0.76)
    glPushMatrix()
    glTranslatef(0, 0.58, 0.175)
    glScalef(1.8, 0.5, 1)
    glutSolidSphere(0.025, 8, 8)
    glPopMatrix()

    # Telinga kiri
    glPushMatrix()
    glTranslatef(-0.185, 0.66, 0.02)
    glScalef(0.3, 0.7, 0.5)
    glutSolidSphere(0.08, 8, 8)
    glPopMatrix()
    # Telinga kanan
    glPushMatrix()
    glTranslatef(0.185, 0.66, 0.02)
    glScalef(0.3, 0.7, 0.5)
    glutSolidSphere(0.08, 8, 8)
    glPopMatrix()

    # Rambut (lapisan di atas kepala)
    glColor3f(0.82, 0.80, 0.77)
    glPushMatrix()
    glTranslatef(0, 0.78, -0.04)
    glScalef(1.0, 0.5, 1.05)
    glutSolidSphere(0.20, 16, 16)
    glPopMatrix()

    from lighting import set_material_default
    set_material_default()


def _brow(x, y, z, rot=0):
    glColor3f(0.75, 0.72, 0.69)
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    glScalef(2.0, 0.3, 0.5)
    glutSolidSphere(0.03, 8, 8)
    glPopMatrix()


# ── Patung 2: Abstrak Modern ──────────────────
def draw_abstract():
    """Patung abstrak — torus + cone + sphere melayang (bronze)."""
    from lighting import set_material_bronze
    set_material_bronze()
    glColor3f(0.72, 0.48, 0.22)

    # Torus bawah (miring)
    glPushMatrix()
    glRotatef(25, 1, 0, 0)
    draw_torus(0.07, 0.32, 16, 28)
    glPopMatrix()

    # Torus tengah (tegak, lebih kecil)
    glPushMatrix()
    glTranslatef(0.1, 0.38, 0)
    glRotatef(65, 0, 0, 1)
    draw_torus(0.05, 0.20, 12, 24)
    glPopMatrix()

    # Batang vertikal
    glPushMatrix()
    glTranslatef(0, 0.10, 0)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(0.06, 0.04, 0.55, 10)
    glPopMatrix()

    # Cone di puncak (terbalik)
    glPushMatrix()
    glTranslatef(0, 0.65, 0)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.00, 0.14, 0.30, 12)
    glPopMatrix()

    # Sphere kecil melayang di samping
    for ox, oy, oz, r in [(-0.28, 0.30, 0.05, 0.06),
                          (0.25, 0.50, -0.08, 0.04),
                          (-0.15, 0.65,  0.10, 0.05)]:
        glPushMatrix()
        glTranslatef(ox, oy, oz)
        glutSolidSphere(r, 12, 12)
        glPopMatrix()

    from lighting import set_material_default
    set_material_default()


# ── Patung 3: The Thinker ─────────────────────
def draw_thinker():
    """Patung pria duduk sedang berpikir (stilisasi dari primitif)."""
    from lighting import set_material_marble
    set_material_marble()
    glColor3f(0.78, 0.75, 0.72)

    # Batu tempat duduk
    glColor3f(0.58, 0.55, 0.52)
    draw_box(0, -0.02, 0, 0.38, 0.14, 0.32)

    glColor3f(0.78, 0.75, 0.72)

    # Paha kiri (silinder horizontal miring)
    glPushMatrix()
    glTranslatef(-0.09, 0.08, 0)
    glRotatef(20, 0, 0, 1)
    glRotatef(10, 1, 0, 0)
    glScalef(0.5, 1.0, 0.5)
    draw_cylinder(0.10, 0.09, 0.32, 10)
    glPopMatrix()

    # Paha kanan
    glPushMatrix()
    glTranslatef(0.09, 0.08, 0)
    glRotatef(-20, 0, 0, 1)
    glRotatef(10, 1, 0, 0)
    glScalef(0.5, 1.0, 0.5)
    draw_cylinder(0.10, 0.09, 0.32, 10)
    glPopMatrix()

    # Betis kiri (menggantung ke bawah-depan)
    glPushMatrix()
    glTranslatef(-0.09, -0.10, 0.18)
    glRotatef(-60, 1, 0, 0)
    glScalef(0.5, 1.0, 0.5)
    draw_cylinder(0.08, 0.07, 0.28, 10)
    glPopMatrix()

    # Betis kanan
    glPushMatrix()
    glTranslatef(0.09, -0.10, 0.18)
    glRotatef(-60, 1, 0, 0)
    glScalef(0.5, 1.0, 0.5)
    draw_cylinder(0.08, 0.07, 0.28, 10)
    glPopMatrix()

    # Torso / badan
    glPushMatrix()
    glTranslatef(0, 0.28, -0.05)
    glRotatef(25, 1, 0, 0)   # condong ke depan
    glScalef(1.0, 1.4, 0.8)
    glutSolidSphere(0.18, 16, 16)
    glPopMatrix()

    # Lengan kiri (disangga di lutut)
    glPushMatrix()
    glTranslatef(-0.08, 0.26, 0.12)
    glRotatef(-65, 1, 0, 0)
    glRotatef(15, 0, 0, 1)
    glScalef(0.4, 1.0, 0.4)
    draw_cylinder(0.07, 0.06, 0.32, 10)
    glPopMatrix()

    # Tangan / kepalan (sphere pipih)
    glPushMatrix()
    glTranslatef(-0.06, 0.32, 0.34)
    glScalef(1.1, 0.7, 0.8)
    glutSolidSphere(0.075, 10, 10)
    glPopMatrix()

    # Lengan kanan (menggantung)
    glPushMatrix()
    glTranslatef(0.12, 0.22, 0.05)
    glRotatef(-30, 1, 0, 0)
    glRotatef(-10, 0, 0, 1)
    glScalef(0.4, 1.0, 0.4)
    draw_cylinder(0.07, 0.06, 0.28, 10)
    glPopMatrix()

    # Kepala (menunduk)
    glPushMatrix()
    glTranslatef(-0.03, 0.60, 0.10)
    glRotatef(15, 1, 0, 0)    # menunduk
    glRotatef(-8,  0, 0, 1)   # sedikit miring
    glutSolidSphere(0.13, 16, 16)

    # Detail kepala: dahi menonjol
    glPushMatrix()
    glTranslatef(0, 0.05, 0.10)
    glScalef(1.0, 0.6, 0.5)
    glutSolidSphere(0.08, 10, 10)
    glPopMatrix()
    glPopMatrix()

    from lighting import set_material_default
    set_material_default()
