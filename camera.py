import math
from OpenGL.GLUT import *


class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 1.65
        self.z = 6.5
        self.yaw = 0.0    # 0 = lihat ke -Z (ke dalam gallery)
        self.pitch = 0.0

        self.speed = 0.08
        self.sens = 0.15
        self.BOUND = 7.2

        self.locked = False
        self.cx = 600   # center window, diupdate dari reshape
        self.cy = 350
        # jumlah warp yang masih pending (belum di-consume oleh callback)
        self.pending_warps = 0

        self.keys = set()

    # ─── window center ────────────────────────
    def set_center(self, w, h):
        self.cx = w // 2
        self.cy = h // 2

    # ─── lock / unlock ────────────────────────
    def lock(self):
        self.locked = True
        self.pending_warps = 0
        glutSetCursor(GLUT_CURSOR_NONE)
        self._warp()

    def unlock(self):
        self.locked = False
        glutSetCursor(GLUT_CURSOR_INHERIT)

    def _warp(self):
        """Paksa cursor ke tengah dan catat bahwa satu warp sedang pending."""
        self.pending_warps += 1
        glutWarpPointer(self.cx, self.cy)

    # ─── mouse motion ─────────────────────────
    def mouse_motion(self, x, y):
        if not self.locked:
            return

        # Kalau ini event dari warp, abaikan dan kurangi counter
        if self.pending_warps > 0:
            self.pending_warps -= 1
            return

        dx = x - self.cx
        dy = y - self.cy

        if dx == 0 and dy == 0:
            return

        # Mouse kanan (dx+) -> lihat kanan -> yaw naik
        # Konsisten dengan apply(): glRotatef(-yaw) -> yaw naik = lihat kanan
        self.yaw = (self.yaw + dx * self.sens) % 360.0

        # Mouse bawah (dy+) -> lihat bawah -> pitch naik
        self.pitch = max(-89.0, min(89.0, self.pitch + dy * self.sens))

        # Warp balik ke tengah
        self._warp()

    def mouse_click(self, btn, state, x, y):
        if btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.lock()

    # ─── keyboard ─────────────────────────────
    def key_down(self, k):  self.keys.add(k)
    def key_up(self, k):    self.keys.discard(k)
    def skey_down(self, k): self.keys.add(('s', k))
    def skey_up(self, k):   self.keys.discard(('s', k))

    # ─── update ───────────────────────────────
    def update(self):
        rad = math.radians(self.yaw)
        # forward = arah kamera lihat, konsisten dengan apply()
        # apply() gunakan glRotatef(-yaw), jadi forward = [-sin(yaw), 0, -cos(yaw)]
        fx = -math.sin(rad)   # yaw=90 -> fx=-1 (lihat -X) -> W maju -X
        fz = -math.cos(rad)   # yaw=0  -> fz=-1 (lihat -Z) -> W maju -Z
        # right = perpendicular ke forward: [cos(yaw), 0, -sin(yaw)]
        rx = math.cos(rad)
        rz = -math.sin(rad)

        mx, mz = 0.0, 0.0
        K = self.keys
        if b'w' in K or b'W' in K or ('s', GLUT_KEY_UP) in K:
            mx += fx
            mz += fz
        if b's' in K or b'S' in K or ('s', GLUT_KEY_DOWN) in K:
            mx -= fx
            mz -= fz
        if b'a' in K or b'A' in K or ('s', GLUT_KEY_LEFT) in K:
            mx -= rx
            mz -= rz
        if b'd' in K or b'D' in K or ('s', GLUT_KEY_RIGHT) in K:
            mx += rx
            mz += rz

        L = math.hypot(mx, mz)
        if L:
            self.x += mx / L * self.speed
            self.z += mz / L * self.speed

        self.x = max(-self.BOUND, min(self.BOUND, self.x))
        self.z = max(-self.BOUND, min(self.BOUND, self.z))

    # ─── apply ────────────────────────────────
    def apply(self):
        from OpenGL.GL import glRotatef, glTranslatef
        glRotatef(-self.pitch, 1, 0, 0)
        glRotatef(-self.yaw,   0, 1, 0)
        glTranslatef(-self.x, -self.y, -self.z)

    def info(self):
        return round(self.x, 1), round(self.z, 1), round(self.yaw, 1)
