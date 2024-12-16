import pygame
import math
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kapal Terbang - Pergerakan dan Ledakan")

# Warna
WHITE = (255, 255, 255)

# Clock untuk mengatur kecepatan frame
clock = pygame.time.Clock()

# Load gambar latar belakang (pastikan path ke file benar)
try:
    background_image = pygame.image.load("C:\\Users\\matilde\\OneDrive\\Documents\\FF Semester 3\\Grafika Komputer Terapan\\TUBES REVISI\\projectFix\\gunaung.png")  # Ganti dengan path gambar latar belakang Anda
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Sesuaikan ukuran background
except pygame.error as e:
    print(f"Error loading background image: {e}")
    pygame.quit()
    exit()

# Load gambar kapal terbang (pastikan path ke file benar)
try:
    plane_image = pygame.image.load("C:\\Users\\matilde\\OneDrive\\Documents\\FF Semester 3\\Grafika Komputer Terapan\\TUBES REVISI\\projectFix\\kapal.png")  # Ganti dengan path gambar pesawat Anda
    plane_image = pygame.transform.scale(plane_image, (100, 60))  # Mengecilkan gambar pesawat (disesuaikan)
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

# Load gambar ledakan (pastikan path ke file benar)
try:
    explosion_image = pygame.image.load("C:\\Users\\matilde\\OneDrive\\Documents\\FF Semester 3\\Grafika Komputer Terapan\\TUBES REVISI\\projectFix\\boom.png")  # Ganti dengan path gambar ledakan Anda
    explosion_image = pygame.transform.scale(explosion_image, (100, 100))  # Sesuaikan ukuran ledakan
except pygame.error as e:
    print(f"Error loading explosion image: {e}")
    pygame.quit()
    exit()

# Load gambar kincir angin (pastikan path ke file benar)
try:
    windmill_image = pygame.image.load("C:\\Users\\matilde\\OneDrive\\Documents\\FF Semester 3\\Grafika Komputer Terapan\\TUBES REVISI\\projectFix\\kincir.png")  # Ganti dengan path gambar kincir angin Anda
    windmill_image = pygame.transform.scale(windmill_image, (150, 150))  # Sesuaikan ukuran kincir angin
except pygame.error as e:
    print(f"Error loading windmill image: {e}")
    pygame.quit()
    exit()

# Load gambar baru yang akan tumbuh (di kanan bawah)
try:
    growing_image = pygame.image.load("C:\\Users\\matilde\\OneDrive\\Documents\\FF Semester 3\\Grafika Komputer Terapan\\TUBES REVISI\\projectFix\\k.png")  # Ganti dengan path gambar baru Anda
    growing_image = pygame.transform.scale(growing_image, (50, 50))  # Ukuran awal kecil
except pygame.error as e:
    print(f"Error loading growing image: {e}")
    pygame.quit()
    exit()

# Posisi dan ukuran pesawat
def reset_plane_position():
    return plane_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Posisi mulai di tengah layar

plane_rect = reset_plane_position()

# Posisi kincir angin (di kiri bawah)
windmill_rect = windmill_image.get_rect(bottomleft=(0, SCREEN_HEIGHT))  # Kincir angin di kiri bawah

# Kecepatan pergerakan kapal terbang
move_speed = 3  # Kecepatan pergerakan kapal terbang

# Variabel untuk kontrol pergerakan
dy = -move_speed  # Pergerakan vertikal (naik)
dx = 0  # Pergerakan horizontal (ke kiri/kanan nanti)

# Status permainan
game_over = False
moving_left = False  # Kontrol pergerakan kiri/kanan

# Fungsi untuk menggambar kapal terbang tanpa rotasi
def draw_plane(screen, plane_image, x, y):
    # Gambar pesawat tanpa rotasi
    screen.blit(plane_image, (x - plane_image.get_width() // 2, y - plane_image.get_height() // 2))

# Fungsi untuk menggambar ledakan
def draw_explosion(screen, explosion_image, x, y):
    # Gambar ledakan pada posisi x, y
    screen.blit(explosion_image, (x - explosion_image.get_width() // 2, y - explosion_image.get_height() // 2))

# Fungsi untuk menggambar kincir angin tanpa rotasi
def draw_windmill(screen, windmill_image, x, y):
    # Gambar kincir angin tanpa rotasi
    screen.blit(windmill_image, (x - windmill_image.get_width() // 2, y - windmill_image.get_height() // 2))

# Fungsi untuk menggambar gambar yang tumbuh
def draw_growing_image(screen, growing_image, x, y, scale_factor):
    # Skalakan gambar untuk membuatnya tumbuh
    new_width = int(growing_image.get_width() * scale_factor)
    new_height = int(growing_image.get_height() * scale_factor)
    scaled_image = pygame.transform.scale(growing_image, (new_width, new_height))
    screen.blit(scaled_image, (x - new_width // 2, y - new_height // 2))

# Fungsi untuk pergerakan kapal terbang
def move_plane(x, y, dx, dy):
    x += dx
    y += dy
    
    # Membatasi pergerakan agar objek tidak keluar dari layar
    if x < 0:  # Jika pesawat melewati tepi kiri
        x = 0
    if x > SCREEN_WIDTH:  # Jika pesawat melewati tepi kanan
        x = SCREEN_WIDTH
    if y < 0:  # Jika pesawat melewati tepi atas
        y = 0
    if y > SCREEN_HEIGHT:  # Jika pesawat melewati tepi bawah
        y = SCREEN_HEIGHT
    
    return x, y

# Kecepatan rotasi kincir angin
rotation_speed = 2  # Kecepatan rotasi baling-baling kincir angin
angle = 0  # Sudut rotasi kincir angin

# Variabel untuk kontrol gambar yang tumbuh
growing_scale_factor = 1  # Faktor skala untuk gambar yang tumbuh
growing_scale_speed = 0.01  # Kecepatan pertumbuhan gambar
start_time = pygame.time.get_ticks()  # Waktu mulai

# Loop utama game
running = True
while running:
    screen.fill(WHITE)  # Membersihkan layar

    # Gambar background terlebih dahulu
    screen.blit(background_image, (0, 0))

    # Cek event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Menghitung waktu berlalu (dalam milidetik)
    elapsed_time = pygame.time.get_ticks() - start_time

    # Jika gambar sudah tumbuh selama 7 detik (7000 ms), reset skala gambar
    if elapsed_time > 7000:
        start_time = pygame.time.get_ticks()  # Reset waktu
        growing_scale_factor = 1  # Reset skala gambar

    # Jika gambar belum mencapai waktu 7 detik, tumbuhkan gambar
    elif elapsed_time <= 7000:
        growing_scale_factor += growing_scale_speed  # Tumbuhkan gambar

    # Pergerakan otomatis pesawat
    # Pertama pesawat naik
    if plane_rect.centery > 100:  # Pesawat bergerak naik
        plane_rect.centerx, plane_rect.centery = move_plane(plane_rect.centerx, plane_rect.centery, dx, dy)
    else:
        # Setelah mencapai bagian atas, pesawat mulai bergerak ke kiri dan kanan
        if not moving_left:
            dx = move_speed  # Gerak ke kanan
        else:
            dx = -move_speed  # Gerak ke kiri

        # Menggerakkan pesawat ke kiri/kanan
        plane_rect.centerx, plane_rect.centery = move_plane(plane_rect.centerx, plane_rect.centery, dx, 0)

        # Setelah pesawat mencapai sisi kiri atau kanan, ubah arah gerakan
        if plane_rect.centerx >= SCREEN_WIDTH - 50:
            moving_left = True  # Mulai bergerak ke kiri
        elif plane_rect.centerx <= 50:  # Deteksi jika pesawat mencapai ujung kiri
            moving_left = False  # Mulai bergerak ke kanan
            game_over = True  # Pesawat meledak dan game selesai

    # Menggambar kapal terbang yang bergerak
    draw_plane(screen, plane_image, plane_rect.centerx, plane_rect.centery)

    # Menggambar kincir angin yang diam
    draw_windmill(screen, windmill_image, windmill_rect.centerx, windmill_rect.centery)

    # Menggambar gambar yang tumbuh di kanan bawah
    draw_growing_image(screen, growing_image, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, growing_scale_factor)

    # Update layar
    pygame.display.flip()

    # Atur kecepatan frame
    clock.tick(60)