import pygame
import random

# Inisialisasi pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 500
BG_COLOR = (173, 216, 230)  # Warna biru muda (mirip air)
FISH_COLOR = (255, 165, 0)  # Warna ikan (orange)
LINE_COLOR = (0, 0, 0)  # Warna kail (hitam)
LINE_SPEED = 10  # Kecepatan gerakan kail
WINNING_SCORE = 10  # Skor untuk menang
TIME_LIMIT = 30  # Waktu permainan dalam detik

# Membuat jendela game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishing Game")

# Font
font = pygame.font.Font(None, 36)

def reset_game():
    """Reset permainan ke kondisi awal."""
    global score, time_left, game_over, fish_x, fish_y, fish_speed, hook_x, hook_y, start_ticks
    score = 0
    time_left = TIME_LIMIT
    game_over = False
    fish_x = random.randint(50, WIDTH - 50)
    fish_y = random.randint(100, HEIGHT - 200)
    fish_speed = 5
    hook_x = WIDTH // 2
    hook_y = HEIGHT - 50
    start_ticks = pygame.time.get_ticks()  # Restart timer

reset_game()  # Mulai dengan game baru

def draw_objects():
    """Menggambar objek permainan di layar"""
    screen.fill(BG_COLOR)

    # Gambar ikan (hanya jika belum game over)
    if not game_over:
        pygame.draw.circle(screen, FISH_COLOR, (fish_x, fish_y), 10)

    # Gambar kail
    pygame.draw.line(screen, LINE_COLOR, (hook_x, HEIGHT - 50), (hook_x, hook_y), 3)

    # Tampilkan skor
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Tampilkan waktu
    timer_text = font.render(f"Time: {time_left}", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH - 120, 10))

    # Jika game over, tampilkan pesan
    if game_over:
        msg = "You Win!" if score >= WINNING_SCORE else "Game Over!"
        game_over_text = font.render(msg, True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))

        # Tombol Mulai Ulang
        restart_text = font.render("Press 'R' to Restart", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - 80, HEIGHT // 2 + 40))

        # Tombol Exit
        exit_text = font.render("Press 'E' to Exit", True, (0, 0, 0))
        screen.blit(exit_text, (WIDTH // 2 - 70, HEIGHT // 2 + 80))

running = True
while running:
    pygame.time.delay(30)  # FPS 30

    # Hitung waktu yang tersisa
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, TIME_LIMIT - seconds)

    # Jika waktu habis atau menang, game over
    if time_left == 0 or score >= WINNING_SCORE:
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jika game over, tekan 'R' untuk restart atau 'E' untuk keluar
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_e:
                running = False

    # Gerakan ikan otomatis (hanya jika belum game over)
    if not game_over:
        fish_x += fish_speed
        if fish_x <= 50 or fish_x >= WIDTH - 50:
            fish_speed = -fish_speed

    # Kontrol kail dengan keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and hook_x > 50:
        hook_x -= LINE_SPEED
    if keys[pygame.K_RIGHT] and hook_x < WIDTH - 50:
        hook_x += LINE_SPEED
    if keys[pygame.K_UP] and hook_y > 50:
        hook_y -= LINE_SPEED
    if keys[pygame.K_DOWN] and hook_y < HEIGHT - 50:
        hook_y += LINE_SPEED

    # Cek apakah kail menangkap ikan
    if abs(hook_x - fish_x) < 15 and abs(hook_y - fish_y) < 15 and not game_over:
        score += 1
        fish_x = random.randint(50, WIDTH - 50)
        fish_y = random.randint(100, HEIGHT - 200)

    # Gambar semua objek
    draw_objects()
    
    # Update layar
    pygame.display.flip()

pygame.quit()
