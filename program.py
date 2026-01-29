import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# --- DATA OBJEK ---
# Vertices Kubus 3D
cube_vertices = [
    [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],
    [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1]
]
cube_edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,7), (7,6), (6,4), (0,4), (1,5), (2,7), (3,6)]

# Vertices Persegi 2D
square_vertices = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]

# --- STATE TRANSFORMASI ---
# Objek 1: Kubus 3D (Sisi Kiri)
c_pos = [-2.0, 0.0, -7.0]
c_rot = [0, 0, 0]
c_scale = 1.0

# Objek 2: Persegi 2D (Sisi Kanan)
s_pos = [2.0, 0.0, -7.0]
s_rot = 0
s_scale = 1.0
s_shear = 0.0
s_reflect_x = 1.0 

def draw_cube():
    glPushMatrix()
    # Transformasi: Translasi, Rotasi, Skala (Poin 14-16)
    glTranslatef(*c_pos)
    glRotatef(c_rot[0], 1, 0, 0)
    glRotatef(c_rot[1], 0, 1, 0)
    glScalef(c_scale, c_scale, c_scale)
    
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0) # Putih
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()
    glPopMatrix()

def draw_square():
    glPushMatrix()
    # Transformasi: Translasi, Rotasi, Skala (Poin 19-21)
    glTranslatef(*s_pos)
    glRotatef(s_rot, 0, 0, 1)
    # Refleksi (Poin 24) menggunakan Scale negatif
    glScalef(s_scale * s_reflect_x, s_scale, 1.0) 
    
    # Shearing (Poin 22) menggunakan matriks manual
    shear_matrix = [1.0, 0.0, 0.0, 0.0,
                    s_shear, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0]
    glMultMatrixf(shear_matrix)
    
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0) # Hijau sesuai contoh gambar soal
    for vertex in square_vertices:
        glVertex2fv(vertex)
    glEnd()
    glPopMatrix()

def main():
    global c_scale, s_scale, s_rot, s_shear, s_reflect_x
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    print("=== KONTROL KUBUS 3D (KIRI) ===")
    print("W/S: Naik/Turun | A/D: Rotasi | Q/E: Skala")
    print("\n=== KONTROL PERSEGI 2D (KANAN) ===")
    print("I/K: Naik/Turun | J/L: Rotasi | U/O: Skala | H/N: Shear | R: Refleksi")

    while True:
        keys = pygame.key.get_pressed()
        
        # --- KONTROL KUBUS (3D) ---
        if keys[K_w]: c_pos[1] += 0.05
        if keys[K_s]: c_pos[1] -= 0.05
        if keys[K_a]: c_rot[1] -= 2
        if keys[K_d]: c_rot[1] += 2
        if keys[K_q]: c_scale += 0.02
        if keys[K_e]: c_scale = max(0.1, c_scale - 0.02)

        # --- KONTROL PERSEGI (2D) ---
        if keys[K_i]: s_pos[1] += 0.05
        if keys[K_k]: s_pos[1] -= 0.05
        if keys[K_j]: s_rot += 2
        if keys[K_l]: s_rot -= 2
        if keys[K_u]: s_scale += 0.02
        if keys[K_o]: s_scale = max(0.1, s_scale - 0.02)
        if keys[K_h]: s_shear += 0.02 
        if keys[K_n]: s_shear -= 0.02

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_r: # Poin 24: Refleksi
                    s_reflect_x *= -1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()   # Sisi Kiri
        draw_square() # Sisi Kanan
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()