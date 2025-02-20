import tkinter as tk
import random


WIDTH, HEIGHT = 1500, 500
FISH_COLOR = "orange"
LINE_COLOR = "black"
BG_COLOR = "pink"
LINE_SPEED = 20  # Kecepatan gerakan kail
WINNING_SCORE = 10  # Skor untuk menang
TIME_LIMIT = 30  # Waktu permainan dalam detik

class FishingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Game")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        
        # Canvas permainan
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()
        
        # Tombol Mulai
        self.start_button = tk.Button(self.root, text="Mulai", command=self.start_game)
        self.start_button.pack()
        
        # Tombol Keluar
        self.exit_button = tk.Button(self.root, text="Keluar", command=self.root.quit)
        self.exit_button.pack()

        # Label skor
        self.score = 0
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack()

        # Label Timer
        self.time_left = TIME_LIMIT
        self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}")
        self.timer_label.pack()
        
        # Variabel permainan
        self.fishing_line = self.canvas.create_line(WIDTH//2, HEIGHT-50, WIDTH//2, HEIGHT-150, width=3, fill=LINE_COLOR)
        self.fish = self.canvas.create_oval(WIDTH//2 - 10, HEIGHT//2 - 10, WIDTH//2 + 10, HEIGHT//2 + 10, fill=FISH_COLOR)
        self.fish_moving = False
        self.game_over = False  

        # Bind tombol panah untuk menggerakkan kail
        self.root.bind("<Up>", self.move_line_up)
        self.root.bind("<Down>", self.move_line_down)
        self.root.bind("<Left>", self.move_line_left)
        self.root.bind("<Right>", self.move_line_right)
        
    def start_game(self):
        """Memulai permainan dan mengatur ulang variabel"""
        self.fish_moving = True
        self.game_over = False
        self.score = 0
        self.time_left = TIME_LIMIT
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.canvas.delete("game_message")  # Hapus pesan sebelumnya jika ada
        self.move_fish()
        self.update_timer()

    def move_fish(self):
        """Menggerakkan ikan secara acak ke kiri atau kanan setiap 500ms"""
        if self.fish_moving and not self.game_over:
            self.canvas.move(self.fish, random.choice([-10, 10]), 0)
            self.root.after(500, self.move_fish)

    def move_line_up(self, event):
        """Menggerakkan kail ke atas"""
        if not self.game_over:
            x1, y1, x2, y2 = self.canvas.coords(self.fishing_line)
            if y2 > 50:
                self.canvas.coords(self.fishing_line, x1, y1 - LINE_SPEED, x2, y2 - LINE_SPEED)
            self.check_catch()

    def move_line_down(self, event):
        """Menggerakkan kail ke bawah"""
        if not self.game_over:
            x1, y1, x2, y2 = self.canvas.coords(self.fishing_line)
            if y2 < HEIGHT - 50:
                self.canvas.coords(self.fishing_line, x1, y1 + LINE_SPEED, x2, y2 + LINE_SPEED)
            self.check_catch()

    def move_line_left(self, event):
        """Menggerakkan kail ke kiri"""
        if not self.game_over:
            x1, y1, x2, y2 = self.canvas.coords(self.fishing_line)
            if x1 > 50:
                self.canvas.coords(self.fishing_line, x1 - LINE_SPEED, y1, x2 - LINE_SPEED, y2)
            self.check_catch()

    def move_line_right(self, event):
        """Menggerakkan kail ke kanan"""
        if not self.game_over:
            x1, y1, x2, y2 = self.canvas.coords(self.fishing_line)
            if x1 < WIDTH - 50:
                self.canvas.coords(self.fishing_line, x1 + LINE_SPEED, y1, x2 + LINE_SPEED, y2)
            self.check_catch()

    def check_catch(self):
        """Cek apakah kail menangkap ikan"""
        if self.game_over:
            return

        fish_coords = self.canvas.coords(self.fish)
        line_coords = self.canvas.coords(self.fishing_line)

        if fish_coords[1] <= line_coords[3] <= fish_coords[3] and fish_coords[0] <= line_coords[0] <= fish_coords[2]:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

            # Jika mencapai skor kemenangan
            if self.score >= WINNING_SCORE:
                self.end_game("Selamat! Anda Menang!")
                return

            # Pindahkan ikan ke lokasi acak
            new_x = random.randint(50, WIDTH - 50)
            new_y = random.randint(50, HEIGHT - 50)
            self.canvas.coords(self.fish, new_x - 10, new_y - 10, new_x + 10, new_y + 10)

    def update_timer(self):
        """Mengurangi waktu permainan setiap detik"""
        if self.time_left > 0 and not self.game_over:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and not self.game_over:
            self.end_game("Game Over!")

    def end_game(self, message):
        """Mengakhiri permainan dengan menampilkan pesan"""
        self.game_over = True
        self.fish_moving = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=message, font=("Arial", 16, "bold"), fill="red", tags="game_message")


if __name__ == "__main__":
    root = tk.Tk()
    game = FishingGame(root)
    root.mainloop()
