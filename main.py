"""
3D ART GALLERY — Grafika Komputer
Universitas Siliwangi — Informatika

KONTROL:
  Klik kiri      — lock cursor & aktifkan mouse look
  ESC            — unlock cursor
  Mouse          — putar pandangan
  W / S          — maju / mundur
  A / D          — strafe kiri / kanan
  Arrow keys     — sama seperti WASD
  L              — toggle lighting
  M              — toggle minimap
  F              — fullscreen
  H              — toggle HUD
"""

import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from camera import Camera
from lighting import setup_lighting, set_material_default
from gallery import draw_room
from paintings import draw_all_paintings
from sculptures import draw_all_sculptures
from utils import draw_bitmap_text

# ── globals ───────────────────────────────────
cam = Camera()
anim_angle = 0.0
WIN_W, WIN_H = 1200, 700
show_map = True
show_hud = True
light_on = True
is_full = False

# Interaction state
interaction_mode = "normal"  # "normal", "painting_view", "sculpture_view"
selected_painting = None
selected_sculpture = None
sculpture_focus_yaw = 0.0  # untuk rotasi saat view 3D patung

# ── init ──────────────────────────────────────


def init():
    glClearColor(0.02, 0.02, 0.04, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    setup_lighting()
    set_material_default()

# ── reshape ───────────────────────────────────


def reshape(w, h):
    global WIN_W, WIN_H
    WIN_W, WIN_H = w, max(h, 1)
    cam.set_center(w, h)
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, w/h, 0.05, 80.0)
    glMatrixMode(GL_MODELVIEW)

# ── interaction helpers ───────────────────────


def find_closest_artwork():
    """Cari lukisan/patung terdekat dari posisi kamera."""
    min_dist = 2.0  # threshold jarak interaksi
    closest_painting = None
    closest_sculpture = None
    closest_dist = float('inf')

    # Check paintings
    from paintings import PAINTINGS
    for i, (_, _, pos, _, _, _, _) in enumerate(PAINTINGS):
        px, py, pz = pos
        dist = math.sqrt((cam.x - px)**2 + (cam.z - pz)**2)
        if dist < closest_dist and dist < min_dist:
            closest_dist = dist
            closest_painting = i
            closest_sculpture = None

    # Check sculptures
    from sculptures import SCULPTURES
    for i, (_, pos, _, _) in enumerate(SCULPTURES):
        px, py, pz = pos
        dist = math.sqrt((cam.x - px)**2 + (cam.z - pz)**2)
        if dist < closest_dist and dist < min_dist:
            closest_dist = dist
            closest_sculpture = i
            closest_painting = None

    return closest_painting, closest_sculpture


# ── scene ─────────────────────────────────────


def draw_scene():
    glLoadIdentity()
    
    if interaction_mode == "normal":
        cam.apply()
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 4.8, 0, 1])
        draw_room()
        draw_all_paintings()
        draw_all_sculptures(anim_angle)
    
    elif interaction_mode == "painting_view" and selected_painting is not None:
        # Focus pada lukisan: camera zoom in di depan lukisan
        from paintings import get_painting
        pdata = get_painting(selected_painting)
        if pdata:
            px, py, pz = pdata['pos']
            rot = pdata['rot']
            # Position camera di depan lukisan
            cam_dist = 0.5
            cam_x = px - math.sin(math.radians(rot)) * cam_dist
            cam_z = pz + math.cos(math.radians(rot)) * cam_dist
            glRotatef(-0, 1, 0, 0)  # pitch
            glRotatef(-rot, 0, 1, 0)  # yaw sesuai orientasi painting
            glTranslatef(-cam_x, -py, -cam_z)
            glLightfv(GL_LIGHT0, GL_POSITION, [0, 4.8, 0, 1])
            draw_room()
            draw_all_paintings()
            draw_all_sculptures(anim_angle)
    
    elif interaction_mode == "sculpture_view" and selected_sculpture is not None:
        # Focus pada patung: camera zoom in, bisa rotate
        from sculptures import get_sculpture
        sdata = get_sculpture(selected_sculpture)
        if sdata:
            sx, sy, sz = sdata['pos']
            # Camera di depan patung, bisa rotate
            cam_dist = 1.0
            rad = math.radians(sculpture_focus_yaw)
            cam_x = sx - math.cos(rad) * cam_dist
            cam_z = sz + math.sin(rad) * cam_dist
            glRotatef(-0, 1, 0, 0)  # pitch
            glRotatef(-sculpture_focus_yaw, 0, 1, 0)
            glTranslatef(-cam_x, -sy, -cam_z)
            glLightfv(GL_LIGHT0, GL_POSITION, [0, 4.8, 0, 1])
            draw_room()
            draw_all_paintings()
            draw_all_sculptures(anim_angle)

# ── 2D overlay helpers ────────────────────────


def begin_2d():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)


def end_2d():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def fill_rect(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()


def line_rect(x, y, w, h):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()


def panel(x, y, w, h):
    glColor4f(0.04, 0.04, 0.08, 0.82)
    fill_rect(x, y, w, h)
    glColor3f(0.40, 0.36, 0.28)
    glLineWidth(1.0)
    line_rect(x, y, w, h)

# ── minimap ───────────────────────────────────


def draw_minimap():
    if not show_map:
        return
    SZ = 150
    MX = WIN_W - SZ - 12
    MY = 12
    SCALE = SZ / 18.0
    cx = MX + SZ/2
    cy = MY + SZ/2

    begin_2d()

    # bg + border
    glColor4f(0.06, 0.06, 0.10, 0.88)
    fill_rect(MX-4, MY-4, SZ+8, SZ+8)
    glColor3f(0.22, 0.16, 0.10)
    fill_rect(MX, MY, SZ, SZ)
    glColor3f(0.52, 0.46, 0.34)
    glLineWidth(1.5)
    line_rect(MX, MY, SZ, SZ)

    # pilar
    glColor3f(0.48, 0.46, 0.42)
    for px, pz in [(-3.5, -3.5), (3.5, -3.5), (-3.5, 3.5), (3.5, 3.5)]:
        fill_rect(cx+px*SCALE-3, cy-pz*SCALE-3, 6, 6)

    # lukisan
    glColor3f(0.85, 0.70, 0.28)
    for px, pz in [(-5.5, -7.85), (0, -7.85), (5.5, -7.85), (-7.85, 0), (7.85, 0)]:
        fill_rect(cx+px*SCALE-5, cy-pz*SCALE-2, 10, 4)

    # patung
    glColor3f(0.68, 0.64, 0.60)
    for px, pz in [(-4.5, 1.5), (0, 1.5), (4.5, 1.5)]:
        mx2 = cx+px*SCALE
        my2 = cy-pz*SCALE
        glBegin(GL_TRIANGLES)
        glVertex2f(mx2, my2+6)
        glVertex2f(mx2-4, my2-4)
        glVertex2f(mx2+4, my2-4)
        glEnd()

    # kamera — titik + panah arah
    rad = math.radians(cam.yaw)
    camx = cx + cam.x * SCALE
    camy = cy - cam.z * SCALE
    alen = 12

    # FOV cone
    glColor4f(1.0, 1.0, 0.5, 0.18)
    glBegin(GL_TRIANGLES)
    glVertex2f(camx, camy)
    for sign in [-1, 1]:
        a = rad + sign * math.radians(35)
        glVertex2f(camx + math.sin(a)*alen*2, camy - math.cos(a)*alen*2)
    glEnd()

    # panah
    glColor3f(1.0, 0.30, 0.20)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(camx, camy)
    glVertex2f(camx + math.sin(rad)*alen, camy - math.cos(rad)*alen)
    glEnd()
    glColor3f(1.0, 0.60, 0.15)
    glPointSize(7.0)
    glBegin(GL_POINTS)
    glVertex2f(camx, camy)
    glEnd()

    glColor3f(0.70, 0.65, 0.55)
    draw_bitmap_text(MX, MY+SZ+5, "MINIMAP", GLUT_BITMAP_HELVETICA_10)

    end_2d()

# ── HUD ───────────────────────────────────────


def draw_hud():
    if not show_hud:
        return
    begin_2d()

    # panel atas kiri
    panel(8, WIN_H-100, 310, 94)
    glColor3f(0.95, 0.90, 0.72)
    draw_bitmap_text(16, WIN_H-22, "3D ART GALLERY", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.62, 0.60, 0.52)
    draw_bitmap_text(16, WIN_H-40, "Universitas Siliwangi — Grafika Komputer",
                     GLUT_BITMAP_HELVETICA_10)
    px, pz, yaw = cam.info()
    glColor3f(0.80, 0.80, 0.68)
    draw_bitmap_text(16, WIN_H-58, f"Pos ({px}, {pz})   Yaw {yaw}°",
                     GLUT_BITMAP_HELVETICA_12)

    if cam.locked:
        glColor3f(0.40, 0.90, 0.40)
        draw_bitmap_text(16, WIN_H-76,
                         "● MOUSE LOCKED   [ESC = unlock]",
                         GLUT_BITMAP_HELVETICA_10)
    else:
        glColor3f(0.90, 0.60, 0.20)
        draw_bitmap_text(16, WIN_H-76,
                         "○ klik kiri di window untuk lock mouse",
                         GLUT_BITMAP_HELVETICA_10)

    glColor3f(0.55, 0.60, 0.65)
    lit = "ON" if light_on else "OFF"
    draw_bitmap_text(16, WIN_H-92,
                     f"L:lighting[{lit}]  M:minimap  F:fullscreen  H:hud",
                     GLUT_BITMAP_HELVETICA_10)

    # crosshair (hanya saat locked)
    if cam.locked:
        cx2, cy2 = WIN_W//2, WIN_H//2
        glColor4f(1, 1, 1, 0.85)
        glLineWidth(1.5)
        glBegin(GL_LINES)
        glVertex2f(cx2-12, cy2)
        glVertex2f(cx2-4, cy2)
        glVertex2f(cx2+4,  cy2)
        glVertex2f(cx2+12, cy2)
        glVertex2f(cx2, cy2-12)
        glVertex2f(cx2, cy2-4)
        glVertex2f(cx2, cy2+4)
        glVertex2f(cx2, cy2+12)
        glEnd()
        glPointSize(2.5)
        glBegin(GL_POINTS)
        glVertex2f(cx2, cy2)
        glEnd()

    # panel kontrol bawah kiri
    panel(8, 8, 330, 68)
    glColor3f(0.58, 0.58, 0.50)
    draw_bitmap_text(16, 54, "Klik kiri: lock mouse | ESC: unlock",
                     GLUT_BITMAP_HELVETICA_10)
    draw_bitmap_text(16, 40, "W/S: maju-mundur   A/D: strafe kiri-kanan",
                     GLUT_BITMAP_HELVETICA_10)
    draw_bitmap_text(16, 26, "Mouse: putar pandangan (saat locked)",
                     GLUT_BITMAP_HELVETICA_10)
    draw_bitmap_text(16, 12, "Arrow keys: alternatif WASD",
                     GLUT_BITMAP_HELVETICA_10)

    end_2d()

# ── display ───────────────────────────────────


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    draw_scene()
    draw_minimap()
    draw_hud()
    glutSwapBuffers()

# ── idle ──────────────────────────────────────


def idle():
    global anim_angle
    anim_angle = (anim_angle + 0.35) % 360.0
    cam.update()
    glutPostRedisplay()

# ── keyboard ──────────────────────────────────


def on_key_down(key, x, y):
    global show_map, show_hud, light_on, is_full

    if key == b'\x1b':          # ESC = unlock
        cam.unlock()
        return

    if key in (b'm', b'M'):
        show_map = not show_map
    if key in (b'h', b'H'):
        show_hud = not show_hud
    if key in (b'l', b'L'):
        light_on = not light_on
        if light_on:
            glEnable(GL_LIGHTING)
        else:
            glDisable(GL_LIGHTING)
    if key in (b'f', b'F'):
        is_full = not is_full
        if is_full:
            glutFullScreen()
        else:
            glutReshapeWindow(WIN_W, WIN_H)
            glutPositionWindow(100, 80)

    cam.key_down(key)


def on_key_up(key, x, y):
    cam.key_up(key)


def on_skey_down(key, x, y):
    cam.skey_down(key)


def on_skey_up(key, x, y):
    cam.skey_up(key)

# ── mouse ─────────────────────────────────────


def on_mouse_click(btn, state, x, y):
    cam.mouse_click(btn, state, x, y)


def on_mouse_move(x, y):          # passive (no button)
    cam.mouse_motion(x, y)


def on_mouse_drag(x, y):          # active (button held)
    cam.mouse_motion(x, y)

# ── main ──────────────────────────────────────


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutInitWindowPosition(100, 80)
    glutCreateWindow(
        b"3D Art Gallery - Grafika Komputer | Universitas Siliwangi")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(on_key_down)
    glutKeyboardUpFunc(on_key_up)
    glutSpecialFunc(on_skey_down)
    glutSpecialUpFunc(on_skey_up)
    glutMouseFunc(on_mouse_click)
    glutPassiveMotionFunc(on_mouse_move)
    glutMotionFunc(on_mouse_drag)

    print("=" * 52)
    print("  3D ART GALLERY — Grafika Komputer")
    print("  Universitas Siliwangi — Informatika")
    print("=" * 52)
    print("  Klik kiri    : lock mouse (aktifkan FPS look)")
    print("  ESC          : unlock mouse")
    print("  W/S          : maju / mundur")
    print("  A/D          : strafe kiri / kanan")
    print("  Mouse        : putar pandangan")
    print("  Arrow        : alternatif WASD")
    print("  L/M/F/H      : lighting/minimap/fullscreen/hud")
    print("=" * 52)

    glutMainLoop()


if __name__ == '__main__':
    main()
