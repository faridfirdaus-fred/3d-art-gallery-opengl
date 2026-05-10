import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from utils import draw_box, draw_text_3d, draw_cylinder

# ─────────────────────────────────────────────
#  LUKISAN — semua full procedural
# ─────────────────────────────────────────────

# Definisi lukisan: (fungsi_gambar, judul, posisi, rotasi_Y, ukuran_W, ukuran_H, deskripsi)
PAINTINGS = [
    # Dinding belakang
    ('starry_night',      "Starry Night",
     (-5.5, 2.5, -7.85), 0,   1.4, 1.0,
     "Terinspirasi dari karya van Gogh.\nLangit malam dengan bintang-bintang berputar\ndan pohon cemara yang megah."),
    ('mountain_landscape', "Mountain Landscape",   (0.0, 2.5, -7.85), 0,   1.6, 1.1,
     "Pemandangan alam dengan gunung-gunung\nyang indah saat matahari terbenam."),
    ('abstract_city',     "Abstract City",
     (5.5, 2.5, -7.85), 0,   1.4, 1.0,
     "Kota malam dengan gedung-gedung modern\ndan jendela-jendela yang bersinar."),
    # Dinding kiri
    ('cubist_portrait',   "Cubist Portrait",      (-7.85, 2.5, 0.0), 90,  1.2, 1.4,
     "Wajah manusia dalam gaya kubisme\ndengan poligon-poligon berwarna cerah."),
    # Dinding kanan
    ('ocean_waves',       "Ocean Waves",
     (7.85, 2.5, 0.0), -90,  1.4, 1.0,
     "Ombak laut yang bergejolak dengan perahu\nkecil di tengah kesukaran alam."),
]


def draw_all_paintings():
    for (style, title, pos, rot_y, pw, ph, desc) in PAINTINGS:
        x, y, z = pos
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(rot_y, 0, 1, 0)

        _draw_frame(pw, ph)
        _draw_canvas(pw, ph)

        glPushMatrix()
        glTranslatef(0, 0, 0.03)   # sedikit di depan kanvas
        {
            'starry_night':       _paint_starry_night,
            'mountain_landscape': _paint_mountain_landscape,
            'abstract_city':      _paint_abstract_city,
            'cubist_portrait':    _paint_cubist_portrait,
            'ocean_waves':        _paint_ocean_waves,
        }[style](pw, ph)
        glPopMatrix()

        # Label / plakat
        _draw_label(title, pw, ph)

        glPopMatrix()


def get_painting(idx):
    """Ambil data painting berdasarkan index."""
    if 0 <= idx < len(PAINTINGS):
        style, title, pos, rot_y, pw, ph, desc = PAINTINGS[idx]
        return {
            'title': title, 'pos': pos, 'rot': rot_y,
            'width': pw, 'height': ph, 'desc': desc, 'style': style
        }
    return None


# ── Frame ─────────────────────────────────────
def _draw_frame(w, h):
    fw = 0.10   # lebar frame
    fd = 0.05   # kedalaman frame

    from lighting import set_material_wood
    set_material_wood()
    glColor3f(0.45, 0.28, 0.08)

    # Atas
    draw_box(0,          h/2 + fw/2, -fd/2, w + 2*fw, fw, fd)
    # Bawah
    draw_box(0,         -h/2 - fw/2, -fd/2, w + 2*fw, fw, fd)
    # Kiri
    draw_box(-w/2 - fw/2, 0,         -fd/2, fw, h, fd)
    # Kanan
    draw_box(w/2 + fw/2, 0,         -fd/2, fw, h, fd)

    # Sudut-sudut frame (sedikit lebih menonjol)
    glColor3f(0.38, 0.22, 0.05)
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            draw_box(sx*(w/2+fw/2), sy*(h/2+fw/2), -fd/2, fw, fw, fd+0.01)

    from lighting import set_material_default
    set_material_default()


def _draw_canvas(w, h):
    """Permukaan kanvas putih gading."""
    glColor3f(0.97, 0.96, 0.91)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-w/2, -h/2, 0.0)
    glVertex3f(w/2, -h/2, 0.0)
    glVertex3f(w/2,  h/2, 0.0)
    glVertex3f(-w/2,  h/2, 0.0)
    glEnd()


def _draw_label(title, w, h):
    """Plakat nama lukisan di bawah frame."""
    lw, lh = min(len(title)*0.065 + 0.2, w*0.9), 0.12
    ly = -h/2 - 0.18

    # Plakat
    glColor3f(0.92, 0.88, 0.78)
    draw_box(0, ly, -0.01, lw, lh, 0.02)

    # Border plakat
    glColor3f(0.55, 0.40, 0.15)
    glLineWidth(1.5)
    hw2, hh2 = lw/2, lh/2
    glBegin(GL_LINE_LOOP)
    glVertex3f(-hw2, ly-hh2, 0.001)
    glVertex3f(hw2, ly-hh2, 0.001)
    glVertex3f(hw2, ly+hh2, 0.001)
    glVertex3f(-hw2, ly+hh2, 0.001)
    glEnd()

    # Teks judul (stroke font, kecil)
    glColor3f(0.20, 0.15, 0.05)
    ts = 0.00055
    text_w = len(title) * 104.76 * ts   # estimasi lebar
    draw_text_3d(-text_w/2, ly - 0.025, 0.015, title, scale=ts)


# ─────────────────────────────────────────────
#  ISI LUKISAN
# ─────────────────────────────────────────────

def _paint_starry_night(w, h):
    """Lukisan langit malam a la Van Gogh — swirling stars."""
    hw, hh = w/2, h/2

    # Langit gradasi biru tua → biru tengah
    glBegin(GL_QUADS)
    glColor3f(0.02, 0.02, 0.18)
    glVertex3f(-hw, -hh, 0)
    glColor3f(0.02, 0.02, 0.18)
    glVertex3f(hw, -hh, 0)
    glColor3f(0.05, 0.08, 0.35)
    glVertex3f(hw,  hh, 0)
    glColor3f(0.05, 0.08, 0.35)
    glVertex3f(-hw,  hh, 0)
    glEnd()

    # Bukit bawah
    glColor3f(0.04, 0.10, 0.06)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(-hw, -hh, 0.001)
    for i in range(21):
        t = i / 20
        bx = -hw + t * w
        by = -hh + 0.15 + 0.12*math.sin(t * math.pi * 2.5)
        glVertex3f(bx, by, 0.001)
    glVertex3f(hw, -hh, 0.001)
    glEnd()

    # Pohon cemara kiri bawah
    _draw_pine(w, h, -hw*0.75, -hh+0.05, 0.18, 0.45)

    # Bulan (lingkaran berlapis — halo)
    moon_x, moon_y = hw*0.55, hh*0.55
    for ri, (r, alpha) in enumerate([(0.18, 0.15), (0.13, 0.35), (0.09, 0.80)]):
        if ri == 2:
            glColor3f(0.98, 0.96, 0.70)
        else:
            glColor3f(0.85, 0.82, 0.50)
        _circle(moon_x, moon_y, r, 0.002 + ri*0.001, 32)

    # Bintang-bintang (deterministik)
    rng = random.Random(777)
    for _ in range(55):
        sx = rng.uniform(-hw*0.85, hw*0.85)
        sy = rng.uniform(-hh*0.1, hh*0.88)
        sr = rng.uniform(0.012, 0.032)
        bright = rng.uniform(0.75, 1.0)
        glColor3f(bright, bright, rng.uniform(0.5, 0.85))
        _star_shape(sx, sy, sr, 0.003)

    # Pusaran angin (GL_LINE_STRIP lengkung)
    glLineWidth(2.0)
    glColor3f(0.25, 0.35, 0.70)
    for swirl_x, swirl_y, swirl_r in [(-0.1, 0.25, 0.25), (0.3, 0.1, 0.18)]:
        glBegin(GL_LINE_STRIP)
        for i in range(60):
            t = i / 60 * math.pi * 4
            decay = 1 - i/60
            sx2 = swirl_x + swirl_r * decay * math.cos(t)
            sy2 = swirl_y + swirl_r * decay * math.sin(t)
            glVertex3f(sx2, sy2, 0.004)
        glEnd()


def _paint_mountain_landscape(w, h):
    """Pemandangan gunung dengan matahari terbenam."""
    hw, hh = w/2, h/2

    # Langit senja (gradasi oranye → merah → ungu)
    glBegin(GL_QUADS)
    glColor3f(0.90, 0.45, 0.10)
    glVertex3f(-hw, -hh,     0)
    glColor3f(0.90, 0.45, 0.10)
    glVertex3f(hw, -hh,     0)
    glColor3f(0.35, 0.15, 0.40)
    glVertex3f(hw,  hh,     0)
    glColor3f(0.35, 0.15, 0.40)
    glVertex3f(-hw,  hh,     0)
    glEnd()

    # Matahari terbenam
    glColor3f(1.0, 0.88, 0.30)
    _circle(0, 0.05, 0.14, 0.001, 32)
    glColor3f(1.0, 0.75, 0.20)
    _circle(0, 0.05, 0.10, 0.002, 32)

    # Gunung belakang (biru abu)
    glColor3f(0.35, 0.32, 0.48)
    _mountain(-hw, hh, 0.003, [
        (-hw, -hh*0.1), (-hw*0.5, hh*0.75), (0, hh*0.5),
        (hw*0.6, hh*0.82), (hw, -hh*0.1), (hw, -hh)
    ])

    # Gunung depan (gelap)
    glColor3f(0.15, 0.13, 0.20)
    _mountain(-hw, hh, 0.005, [
        (-hw, -hh*0.3), (-hw*0.7, hh*0.35), (-hw*0.2, hh*0.10),
        (0, hh*0.50), (hw*0.4, hh*0.22), (hw*0.8, hh*0.40),
        (hw, -hh*0.3), (hw, -hh)
    ])

    # Danau / refleksi (cermin di bawah)
    glColor3f(0.55, 0.35, 0.20)
    glBegin(GL_QUADS)
    glVertex3f(-hw*0.5, -hh, 0.006)
    glVertex3f(hw*0.5, -hh, 0.006)
    glVertex3f(hw*0.5, -hh*0.45, 0.006)
    glVertex3f(-hw*0.5, -hh*0.45, 0.006)
    glEnd()
    # Kilap danau
    glColor3f(0.90, 0.60, 0.25)
    glLineWidth(1.5)
    for yi in range(4):
        yl = -hh + yi * 0.05 + 0.02
        glBegin(GL_LINE_STRIP)
        for xi in range(8):
            xl = -hw*0.45 + xi * hw*0.13
            glVertex3f(xl, yl, 0.007)
            glVertex3f(xl+hw*0.05, yl+0.012, 0.007)
        glEnd()


def _paint_abstract_city(w, h):
    """Kota abstrak malam hari — gedung-gedung dengan jendela."""
    hw, hh = w/2, h/2

    # Langit malam kota (gradasi ungu gelap)
    glBegin(GL_QUADS)
    glColor3f(0.06, 0.04, 0.12)
    glVertex3f(-hw, -hh, 0)
    glColor3f(0.06, 0.04, 0.12)
    glVertex3f(hw, -hh, 0)
    glColor3f(0.15, 0.10, 0.28)
    glVertex3f(hw,  hh, 0)
    glColor3f(0.15, 0.10, 0.28)
    glVertex3f(-hw,  hh, 0)
    glEnd()

    # Gedung-gedung
    rng = random.Random(42)
    buildings = []
    x = -hw
    while x < hw:
        bw = rng.uniform(0.12, 0.22)
        bh = rng.uniform(0.25, hh*1.6)
        buildings.append((x, bw, bh))
        x += bw + 0.01
    buildings.append((x, hw*2, 0.1))  # pastikan tutup

    for bx, bw, bh in buildings:
        # Badan gedung
        r = rng.uniform(0.08, 0.22)
        g = rng.uniform(0.06, 0.18)
        b2 = rng.uniform(0.15, 0.35)
        glColor3f(r, g, b2)
        glBegin(GL_QUADS)
        glVertex3f(bx,     -hh,     0.002)
        glVertex3f(bx+bw,  -hh,     0.002)
        glVertex3f(bx+bw,  -hh+bh,  0.002)
        glVertex3f(bx,     -hh+bh,  0.002)
        glEnd()

        # Jendela (kuning / putih)
        for wy in range(int(bh/0.07)):
            for wx in range(int(bw/0.055)):
                if rng.random() > 0.35:
                    wxp = bx + wx*0.055 + 0.01
                    wyp = -hh + wy*0.07 + 0.04
                    ww, wh2 = 0.03, 0.035
                    lit = rng.random()
                    if lit > 0.7:
                        glColor3f(1.0, 0.95, 0.70)
                    elif lit > 0.4:
                        glColor3f(0.7, 0.85, 1.0)
                    else:
                        continue
                    glBegin(GL_QUADS)
                    glVertex3f(wxp,    wyp,     0.003)
                    glVertex3f(wxp+ww, wyp,     0.003)
                    glVertex3f(wxp+ww, wyp+wh2, 0.003)
                    glVertex3f(wxp,    wyp+wh2, 0.003)
                    glEnd()

    # Bulan abstrak
    glColor3f(0.80, 0.78, 0.90)
    _circle(hw*0.65, hh*0.65, 0.10, 0.009, 24)

    # Bintang
    rng2 = random.Random(99)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for _ in range(30):
        glColor3f(0.8, 0.8, 1.0)
        glVertex3f(rng2.uniform(-hw, hw), rng2.uniform(0, hh*0.85), 0.001)
    glEnd()


def _paint_cubist_portrait(w, h):
    """Potret cubism — wajah dari poligon-poligon berwarna."""
    hw, hh = w/2, h/2

    # Background
    glColor3f(0.78, 0.68, 0.52)
    glBegin(GL_QUADS)
    glVertex3f(-hw, -hh, 0)
    glVertex3f(hw, -hh, 0)
    glVertex3f(hw, hh, 0)
    glVertex3f(-hw, hh, 0)
    glEnd()

    # Kepala (ellips kasar dari segitiga-segitiga)
    face_parts = [
        # (warna, list_vertex)
        # Wajah kiri (coklat muda)
        ((0.85, 0.65, 0.45), [(-0.22, -0.35),
         (0.02, -0.45), (0.02, 0.25), (-0.22, 0.30)]),
        # Wajah kanan (sedikit lebih terang)
        ((0.92, 0.75, 0.55), [(0.02, -0.45),
         (0.28, -0.35), (0.25, 0.30), (0.02, 0.25)]),
        # Dahi
        ((0.80, 0.62, 0.44), [(-0.22, 0.30), (0.02, 0.25),
         (0.25, 0.30), (0.05, 0.58), (-0.15, 0.60)]),
        # Mata kiri (segitiga biru)
        ((0.25, 0.35, 0.65), [(-0.18, 0.05), (-0.06, 0.10), (-0.12, 0.22)]),
        # Mata kanan (segitiga hijau)
        ((0.25, 0.55, 0.40), [(0.06, 0.08), (0.20, 0.05), (0.15, 0.22)]),
        # Hidung (segitiga oranye)
        ((0.75, 0.45, 0.20), [(-0.05, -0.05), (0.08, -0.02), (0.02, 0.08)]),
        # Bibir (merah)
        ((0.75, 0.22, 0.22), [(-0.14, -0.22),
         (0.18, -0.20), (0.10, -0.10), (-0.08, -0.12)]),
        # Rambut (gelap)
        ((0.22, 0.15, 0.08), [(-0.22, 0.30), (-0.15, 0.60),
         (0.05, 0.68), (0.25, 0.60), (0.25, 0.30)]),
        # Leher
        ((0.80, 0.62, 0.44), [(-0.10, -0.35),
         (0.12, -0.35), (0.10, -0.52), (-0.08, -0.52)]),
        # Baju (biru kubis)
        ((0.30, 0.42, 0.68), [(-0.35, -0.60), (0.35, -0.60), (0.30, -0.35), (0.12, -0.35),
                              (0.10, -0.52), (-0.08, -0.52), (-0.10, -0.35), (-0.30, -0.35)]),
    ]
    for color, verts in face_parts:
        glColor3f(*color)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1)
        for vx, vy in verts:
            glVertex3f(vx, vy, 0.001)
        glEnd()

    # Outline kubis
    glColor3f(0.15, 0.10, 0.05)
    glLineWidth(1.5)
    for _, verts in face_parts:
        glBegin(GL_LINE_LOOP)
        for vx, vy in verts:
            glVertex3f(vx, vy, 0.002)
        glEnd()


def _paint_ocean_waves(w, h):
    """Laut dengan ombak (sine wave) — seperti karya Hokusai."""
    hw, hh = w/2, h/2

    # Langit biru cerah
    glBegin(GL_QUADS)
    glColor3f(0.50, 0.72, 0.92)
    glVertex3f(-hw,  0.0, 0)
    glColor3f(0.50, 0.72, 0.92)
    glVertex3f(hw,  0.0, 0)
    glColor3f(0.85, 0.93, 1.00)
    glVertex3f(hw,  hh,  0)
    glColor3f(0.85, 0.93, 1.00)
    glVertex3f(-hw,  hh,  0)
    glEnd()

    # Awan (ellips putih)
    for cx, cy, cr in [(-hw*0.5, hh*0.7, 0.18), (hw*0.2, hh*0.85, 0.22), (hw*0.65, hh*0.6, 0.14)]:
        glColor3f(1.0, 1.0, 1.0)
        _cloud(cx, cy, cr, 0.002)

    # Lapisan ombak (dari belakang ke depan)
    wave_layers = [
        (0.20, 0.42, 0.75,  0.0,  0.15, 0.6, 1.5),
        (0.10, 0.35, 0.70, -0.10, 0.22, 0.5, 2.0),
        (0.05, 0.28, 0.65, -0.22, 0.28, 0.4, 2.5),
        (0.02, 0.20, 0.58, -0.35, 0.35, 0.35, 3.0),
    ]
    for r, g, b2, base_y, amp, freq_mult, z_off in wave_layers:
        glColor3f(r, g, b2)
        N = 80
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(N+1):
            t = i / N
            x = -hw + t * w
            y_top = base_y + amp * math.sin(t * math.pi * freq_mult * 2)
            glVertex3f(x, y_top,    z_off*0.001 + 0.001)
            glVertex3f(x, -hh,      z_off*0.001 + 0.001)
        glEnd()

        # Puncak ombak putih (busa)
        glColor3f(0.95, 0.98, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        for i in range(N+1):
            t = i / N
            x = -hw + t * w
            y_top = base_y + amp * math.sin(t * math.pi * freq_mult * 2)
            glVertex3f(x, y_top, z_off*0.001 + 0.002)
        glEnd()

    # Perahu kecil (silhouette)
    glColor3f(0.12, 0.08, 0.05)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.05, -0.28, 0.010)
    glVertex3f(0.18, -0.28, 0.010)
    glVertex3f(0.07, -0.22, 0.010)
    glEnd()
    # Layar
    glColor3f(0.92, 0.88, 0.80)
    glBegin(GL_TRIANGLES)
    glVertex3f(0.07, -0.22, 0.011)
    glVertex3f(0.07,  0.05, 0.011)
    glVertex3f(0.22, -0.22, 0.011)
    glEnd()


# ─────────────────────────────────────────────
#  HELPER BENTUK
# ─────────────────────────────────────────────

def _circle(cx, cy, r, z, segments):
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, 1)
    glVertex3f(cx, cy, z)
    for i in range(segments+1):
        a = 2*math.pi * i / segments
        glVertex3f(cx + math.cos(a)*r, cy + math.sin(a)*r, z)
    glEnd()


def _star_shape(cx, cy, r, z):
    """Bintang 5 titik kecil."""
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(cx, cy, z)
    for i in range(11):
        a = math.pi/2 + i * 2*math.pi/10
        ri = r if i % 2 == 0 else r*0.4
        glVertex3f(cx + math.cos(a)*ri, cy + math.sin(a)*ri, z)
    glEnd()


def _mountain(lx, ly, z, points):
    glBegin(GL_POLYGON)
    glNormal3f(0, 0, 1)
    for px, py in points:
        glVertex3f(px, py, z)
    glEnd()


def _draw_pine(w, h, px, py, pw, ph):
    """Pohon cemara dari segitiga bertumpuk."""
    glColor3f(0.04, 0.12, 0.06)
    for level in range(3):
        lw = pw * (1 - level*0.25)
        lh = ph * 0.45
        ly = py + level * ph * 0.30
        glBegin(GL_TRIANGLES)
        glVertex3f(px - lw, ly,       0.003)
        glVertex3f(px + lw, ly,       0.003)
        glVertex3f(px,       ly + lh, 0.003)
        glEnd()


def _cloud(cx, cy, r, z):
    """Awan dari beberapa lingkaran."""
    for ox, oy, or2 in [(0, 0, 1.0), (0.35, 0.05, 0.75), (-0.35, 0.0, 0.70), (0.15, 0.18, 0.65)]:
        _circle(cx + ox*r, cy + oy*r, r*or2*0.7, z, 20)
