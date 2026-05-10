# 🎨 3D Art Gallery — Galeri Seni 3D Interaktif

Sebuah aplikasi galeri seni 3D yang dibangun dengan Python dan OpenGL untuk mata kuliah Grafika Komputer di Universitas Siliwangi.

## 📋 Deskripsi Proyek

**3D Art Gallery** adalah simulasi galeri seni 3D yang memungkinkan pengunjung untuk:
- 🚶 **Jelajahi ruangan galeri** dengan navigasi first-person
- 🖼️ **Lihat lukisan procedural** yang dibuat secara real-time
- 🗿 **Lihat patung 3D** dengan animasi
- 💡 **Interaksi dinamis** dengan lighting dan visual effects
- 🗺️ **Navigasi dengan minimap** untuk orientasi
- ⌨️ **Kontrol penuh** dengan keyboard dan mouse

### Fitur Utama

- **Grafis 3D Prosedural**: Semua lukisan dan patung dibuat secara procedural menggunakan OpenGL primitif
- **5 Lukisan Unik**: Starry Night, Mountain Landscape, Abstract City, Cubist Portrait, Ocean Waves
- **3 Patung Interaktif**: Venus, Abstract Form, The Thinker
- **Ruangan Galeri Realistis**: Lantai, dinding, langit-langit, pilar, kursi, dan pencahayaan
- **Sistem Kamera First-Person**: Navigasi smooth dengan mouse look
- **Efek Lighting Dinamis**: Toggle antara light on/off
- **HUD & Minimap**: Tampilan informasi dan peta mini
- **Mode Fullscreen**: Pengalaman immersive penuh


## 🛠️ Instalasi

### Prasyarat
- **Python 3.8+** sudah terinstall
- **pip** (Package manager untuk Python)
- **Windows 10/11** atau OS lain yang mendukung OpenGL

### Langkah-Langkah Instalasi

#### 1. Clone Repository
```bash
git clone <repository-url>
cd 3dgalery
```

#### 2. Buat Virtual Environment
```bash
# Untuk Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Untuk Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

# Untuk macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install secara manual:
```bash
pip install PyOpenGL PyOpenGL-accelerate
pip install pyopengl_accelerate
```

#### 4. Jalankan Aplikasi
```bash
python main.py
```

## 📁 Struktur Proyek

```
3dgalery/
├── main.py              # Entry point aplikasi
├── camera.py            # Sistem kamera first-person
├── gallery.py           # Rendering ruangan galeri
├── paintings.py         # Definisi dan rendering lukisan
├── sculptures.py        # Definisi dan rendering patung
├── lighting.py          # Sistem pencahayaan
├── utils.py             # Utility functions (drawing primitives)
├── readme.md            # File ini
├── requirements.txt     # Dependencies proyek
├── .gitignore           # Git ignore file
└── .venv/               # Virtual environment (jangan commit)
```

## 📦 Dependencies

- **PyOpenGL** - Binding Python untuk OpenGL
- **PyOpenGL-accelerate** - Akselerasi untuk PyOpenGL (opsional tapi direkomendasikan)
- **GLUT** - OpenGL Utility Toolkit (biasanya terintegrasi dengan PyOpenGL)

## 🚀 Cara Menggunakan

### Menjalankan Aplikasi
```bash
# Pastikan virtual environment sudah aktif
python main.py
```


## 🎯 Fitur Teknis

### Sistem Rendering
- OpenGL 2.0+ compatibility
- Vertex transformation dengan view/projection matrix
- Material dan lighting calculations
- Texture coordinates (untuk future enhancement)

### Sistem Kamera
- First-person perspective
- Mouse-based rotation (yaw/pitch)
- Smooth movement dengan vector math
- Collision detection dengan boundaries ruangan

### Sistem Animasi
- Animated rotation untuk patung
- Smooth frame-based animation
- Framerate independent movement

## 🐛 Troubleshooting

### Error: "OpenGL is not available"
- Install driver GPU terbaru dari manufacturer (NVIDIA/AMD/Intel)
- Pastikan PyOpenGL terinstall dengan benar: `pip install --upgrade PyOpenGL`

### Error: "No module named OpenGL"
- Aktifkan virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Aplikasi berjalan lambat
- Cek pengaturan quality/resolution
- Update driver GPU
- Tutup aplikasi background yang menggunakan GPU

### Mouse/Keyboard tidak merespon
- Tekan ESC terlebih dahulu
- Klik ulang pada window aplikasi
- Restart aplikasi jika perlu

## 📝 Catatan Pengembangan

Proyek ini menggunakan pendekatan **full procedural generation** untuk semua objek 3D, artinya:
- Semua geometri dibuat secara runtime menggunakan OpenGL primitif
- Tidak menggunakan external 3D models atau textures
- Semua animasi bersifat procedural

## 🎓 Referensi

- [OpenGL Documentation](https://www.opengl.org/documentation/)
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/)
- [Universitas Siliwangi - Informatika](https://unsil.ac.id)

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis mata kuliah Grafika Komputer.

## 👨‍💻 Author

Dibuat untuk Universitas Siliwangi - Program Studi Informatika

---
