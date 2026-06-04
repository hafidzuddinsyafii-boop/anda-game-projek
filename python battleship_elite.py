# =========================================================
# BATTLESHIP ELITE V2 - NEON TACTICAL EDITION
# =========================================================
#
# FEATURES
# ✅ Futuristic Neon UI
# ✅ Ship Hover Preview
# ✅ Weak Point System
# ✅ Destroy All Ships To Win
# ✅ Smart AI Hunt + Target
# ✅ Scoreboard
# ✅ Rotate Ship
# ✅ Continue Turn On HIT
# ✅ Restart Game
# ✅ Clean OOP Structure
#
# RUN:
# python battleship_elite_v2.py
#
# =========================================================
#        orang 1 start -> tempat kapal
# =========================================================


import tkinter as tk
from tkinter import messagebox
import random

# =========================================================
# CONFIG
# =========================================================

SIZE = 10
SHIP_SIZES = [5, 4, 3, 2]

BG = "#07111f"
PANEL = "#0d1b2a"
GRID = "#12324a"

NEON_BLUE = "#00d4ff"
NEON_RED = "#ff3c78"
NEON_GREEN = "#00ff99"
NEON_YELLOW = "#ffe066"

WEAK_POINT_COLOR = "#ff00ff"   # kepala kapal
TEXT = "#eaf6ff"

# =========================================================
# MAIN CLASS
# =========================================================

class BattleshipElite:

    def __init__(self, root):

        self.root = root

        self.root.title("Battleship Elite V2")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ===============================
        # GAME VARIABLES
        # ===============================

        self.orientation = "H" # Menentukan orientasi awal penempatan kapal (Horizontal)

        self.player_turn = False # Status awal giliran pemain (False karena harus menempatkan kapal dulu)

        self.placing_index = 0 # Menelusuri indeks kapal mana yang sedang ditempatkan dari daftar SHIP_SIZES

        self.player_hits = 0
        self.ai_hits = 0

        self.player_destroyed = 0
        self.ai_destroyed = 0

        self.hunt_targets = [] # Menyimpan koordinat target buruan AI saat berhasil mengenai kapal pemain

        self.difficulty = tk.StringVar(value="Medium") # Menyimpan tingkat kesulitan AI menggunakan variabel string Tkinter

        # boards
        # Membuat representasi papan 10x10 berupa list dua dimensi berisi karakter "~" (air)
        self.player_board = [["~"] * SIZE for _ in range(SIZE)]
        self.ai_board = [["~"] * SIZE for _ in range(SIZE)]

        self.player_ships = []
        self.ai_ships = []

        # ===============================
        # UI
        # ===============================

        self.create_ui()

        # generate AI ships
        self.generate_ai_ships()
# =========================================================
#       orang 1 end -> tempat kapal
# =========================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# =========================================================
#    orang 2 start -> UI
# =========================================================
    def create_ui(self):

        title = tk.Label(
            self.root,
            text="⚓ BATTLESHIP ELITE V2 ⚓",
            font=("Arial", 28, "bold"),
            bg=BG,
            fg=NEON_BLUE
        )

        title.pack(pady=10)

        # ===============================
        # TOP BAR
        # ===============================

        top = tk.Frame(self.root, bg=BG)
        top.pack()

        self.info_label = tk.Label(
            top,
            text="Place ship size 5",
            font=("Arial", 14, "bold"),
            bg=BG,
            fg=TEXT
        )

        self.info_label.pack(side=tk.LEFT, padx=10)

        rotate_btn = tk.Button(
            top,
            text="ROTATE",
            bg=NEON_BLUE,
            fg="black",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.rotate_ship # Menghubungkan tombol ke fungsi pengubah rotasi kapal
        )

        rotate_btn.pack(side=tk.LEFT, padx=5)

        difficulty_menu = tk.OptionMenu(
            top,
            self.difficulty,
            "Easy",
            "Medium",
            "Hard"
        )

        difficulty_menu.pack(side=tk.LEFT, padx=5)

        restart_btn = tk.Button(
            top,
            text="RESTART",
            bg=NEON_RED,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.reset_game # Menghubungkan tombol untuk mereset permainan ke awal
        )

        restart_btn.pack(side=tk.LEFT, padx=5)

        # ===============================
        # SCOREBOARD
        # ===============================

        self.score_frame = tk.Frame(
            self.root,
            bg=PANEL,
            bd=2,
            relief="ridge"
        )

        self.score_frame.pack(pady=10)

        self.player_score = tk.Label(
            self.score_frame,
            text="PLAYER HITS : 0",
            font=("Arial", 12, "bold"),
            bg=PANEL,
            fg=NEON_GREEN
        )

        self.player_score.grid(row=0, column=0, padx=20, pady=5)

        self.ai_score = tk.Label(
            self.score_frame,
            text="AI HITS : 0",
            font=("Arial", 12, "bold"),
            bg=PANEL,
            fg=NEON_RED
        )

        self.ai_score.grid(row=0, column=1, padx=20)

        self.player_destroy_label = tk.Label(
            self.score_frame,
            text="YOU DESTROYED : 0",
            font=("Arial", 11),
            bg=PANEL,
            fg=TEXT
        )

        self.player_destroy_label.grid(row=1, column=0)

        self.ai_destroy_label = tk.Label(
            self.score_frame,
            text="AI DESTROYED : 0",
            font=("Arial", 11),
            bg=PANEL,
            fg=TEXT
        )

        self.ai_destroy_label.grid(row=1, column=1)

        # ===============================
        # MAIN BOARDS
        # ===============================

        boards = tk.Frame(self.root, bg=BG)
        boards.pack(pady=15)

        # player
        left = tk.Frame(boards, bg=BG)
        left.grid(row=0, column=0, padx=20)

        tk.Label(
            left,
            text="PLAYER",
            font=("Arial", 18, "bold"),
            bg=BG,
            fg=TEXT
        ).pack()

        self.player_grid = tk.Frame(left, bg=BG)
        self.player_grid.pack()

        # AI
        right = tk.Frame(boards, bg=BG)
        right.grid(row=0, column=1, padx=20)

        tk.Label(
            right,
            text="ENEMY",
            font=("Arial", 18, "bold"),
            bg=BG,
            fg=TEXT
        ).pack()

        self.ai_grid = tk.Frame(right, bg=BG)
        self.ai_grid.pack()

        self.player_buttons = []
        self.ai_buttons = []

        self.create_buttons()
# ========================================================
#              orang 2 end -> UI
# ========================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ========================================================
#              orang 3 start -> BUTTONS
# ========================================================
    def create_buttons(self):

        for r in range(SIZE):

            row_buttons = []

            for c in range(SIZE):

                btn = tk.Button(
                    self.player_grid,
                    width=2,
                    height=1,
                    font=("Arial", 14, "bold"),
                    bg=GRID,
                    fg="white",
                    relief="flat",
                    activebackground=NEON_BLUE,
                    command=lambda r=r, c=c:
                    self.place_player_ship(r, c) # Fungsi penempatan kapal dipicu saat tombol papan player diklik
                )

                btn.grid(row=r, column=c, padx=1, pady=1)

                btn.bind(
                    "<Enter>", # Event trigger ketika kursor mouse masuk ke area tombol
                    lambda e, r=r, c=c:
                    self.preview_ship(r, c)
                )

                btn.bind(
                    "<Leave>", # Event trigger ketika kursor mouse keluar meninggalkan area tombol
                    lambda e:
                    self.clear_preview()
                )

                row_buttons.append(btn)

            self.player_buttons.append(row_buttons)

        for r in range(SIZE):

            row_buttons = []

            for c in range(SIZE):

                btn = tk.Button(
                    self.ai_grid,
                    width=2,
                    height=1,
                    font=("Arial", 14, "bold"),
                    bg=GRID,
                    fg="white",
                    relief="flat",
                    activebackground=NEON_RED,
                    command=lambda r=r, c=c:
                    self.player_shoot(r, c) # Fungsi menembak dipicu saat tombol papan musuh diklik
                )

                btn.grid(row=r, column=c, padx=1, pady=1)

                row_buttons.append(btn)

            self.ai_buttons.append(row_buttons)

    # =====================================================
    # ROTATE
    # =====================================================

    def rotate_ship(self):

        # Mengubah nilai orientasi bolak-balik antara Horizontal (H) dan Vertical (V)
        if self.orientation == "H":
            self.orientation = "V"
        else:
            self.orientation = "H"

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview_ship(self, row, col):

        if self.placing_index >= len(SHIP_SIZES): # Jika semua kapal sudah ditaruh, hentikan proses preview
            return

        self.clear_preview()

        size = SHIP_SIZES[self.placing_index]

        valid = self.valid_ship(
            self.player_board,
            row,
            col,
            size,
            self.orientation
        )

        # Memberi warna NEON_GREEN jika posisi aman ditaruh, atau NEON_RED jika menabrak/keluar batas papan
        color = NEON_GREEN if valid else NEON_RED

        for i in range(size):

            rr = row
            cc = col

            if self.orientation == "H":
                cc += i
            else:
                rr += i

            if 0 <= rr < SIZE and 0 <= cc < SIZE:

                if self.player_board[rr][cc] == "~":

                    self.player_buttons[rr][cc].config(
                        bg=color
                    )

    def clear_preview(self):

        for r in range(SIZE):
            for c in range(SIZE):

                if self.player_board[r][c] == "~": # Mengembalikan warna petak kosong kembali ke warna grid standar

                    self.player_buttons[r][c].config(
                        bg=GRID
                    )
# =====================================================
#             orang 3 end -> BUTTONS
# =====================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ========================================================
#             orang 4 start -> VALID SHIP
# ========================================================
    def valid_ship(self, board, row, col, size, orient):

        if orient == "H":

            if col + size > SIZE: # Mengembalikan False jika panjang kapal melebihi batas kanan matriks papan
                return False

            for i in range(size):

                if board[row][col+i] != "~": # Mengembalikan False jika petak target sudah diisi kapal lain
                    return False

        else:

            if row + size > SIZE: # Mengembalikan False jika panjang kapal melebihi batas bawah matriks papan
                return False

            for i in range(size):

                if board[row+i][col] != "~": # Mengembalikan False jika petak target sudah diisi kapal lain
                    return False

        return True

    # =====================================================
    # PLACE SHIP
    # =====================================================

    def place_ship(self, board, ships, row, col, size, orient):

        positions = []

        if orient == "H":

            for i in range(size):

                board[row][col+i] = "S" # Menandai koordinat matriks internal dengan huruf "S" (Ship)

                positions.append((row, col+i))

        else:

            for i in range(size):

                board[row+i][col] = "S" # Menandai koordinat matriks internal dengan huruf "S" (Ship)

                positions.append((row+i, col))

        # weak point = kepala kapal
        weak = positions[0] # Menetapkan elemen koordinat pertama kapal sebagai titik kelemahan fatal

        ships.append({
            "positions": positions,
            "weak": weak,
            "destroyed": False
        })

    # =====================================================
    # GENERATE AI SHIPS
    # =====================================================

    def generate_ai_ships(self):

        self.ai_ships.clear()

        self.ai_board = [["~"] * SIZE for _ in range(SIZE)]

        for size in SHIP_SIZES:

            placed = False

            while not placed: # Terus melakukan acakan koordinat hingga kapal AI berhasil ditempatkan secara valid

                r = random.randint(0, SIZE-1)
                c = random.randint(0, SIZE-1)

                o = random.choice(["H", "V"])

                if self.valid_ship(
                    self.ai_board,
                    r,
                    c,
                    size,
                    o
                ):

                    self.place_ship(
                        self.ai_board,
                        self.ai_ships,
                        r,
                        c,
                        size,
                        o
                    )

                    placed = True

    # =====================================================
    # PLACE PLAYER SHIP
    # =====================================================

    def place_player_ship(self, row, col):

        if self.placing_index >= len(SHIP_SIZES):
            return

        size = SHIP_SIZES[self.placing_index]

        if not self.valid_ship(
            self.player_board,
            row,
            col,
            size,
            self.orientation
        ):
            return

        self.place_ship(
            self.player_board,
            self.player_ships,
            row,
            col,
            size,
            self.orientation
        )

        self.update_player_board()

        self.placing_index += 1

        self.clear_preview()

        if self.placing_index < len(SHIP_SIZES): # Memperbarui teks instruksi ukuran kapal berikutnya yang harus ditaruh

            self.info_label.config(
                text=f"Place ship size {SHIP_SIZES[self.placing_index]}"
            )

        else:

            self.player_turn = True # Mengubah giliran menjadi milik player karena semua kapal telah terpasang

            self.info_label.config(
                text="⚔ BATTLE STARTED!"
            )

    # =====================================================
    # UPDATE PLAYER BOARD
    # =====================================================

    def update_player_board(self):

        weak_points = {
            ship["weak"]
            for ship in self.player_ships
            if not ship["destroyed"]
        }

        for r in range(SIZE):
            for c in range(SIZE):

                val = self.player_board[r][c]
                btn = self.player_buttons[r][c]

                # SHIP
                if val == "S":

                    # kepala kapal
                    if (r, c) in weak_points: # Mewarnai kepala kapal dengan warna magenta dan simbol bintang

                        btn.config(
                            bg=WEAK_POINT_COLOR,
                            text="★"
                        )

                    # body kapal
                    else:

                        btn.config(
                            bg=NEON_BLUE,
                            text=""
                        )

                # HIT
                elif val == "X": # Menampilkan simbol kilatan kuning jika bagian kapal biasa tertembak

                    btn.config(
                        bg=NEON_YELLOW,
                        text="✦"
                    )

                # MISS
                elif val == "O": # Mengubah warna tombol menjadi abu-abu jika tembakan meleset ke laut

                    btn.config(
                        bg="#5c677d",
                        text=""
                    )

                # DESTROYED
                elif val == "D": # Mengubah warna menjadi merah neon bersimbol tengkorak jika seluruh bagian kapal hancur

                    btn.config(
                        bg=NEON_RED,
                        text="☠"
                    )
# ========================================================
#             orang 4 end -> VALID SHIP
# ========================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ========================================================
#            orang 5 start -> scoring
# ========================================================
# =====================================================
    # SCOREBOARD
    # =====================================================

    def update_scoreboard(self):

        self.player_score.config(
            text=f"PLAYER HITS : {self.player_hits}"
        )

        self.ai_score.config(
            text=f"AI HITS : {self.ai_hits}"
        )

        self.player_destroy_label.config(
            text=f"YOU DESTROYED : {self.player_destroyed}"
        )

        self.ai_destroy_label.config(
            text=f"AI DESTROYED : {self.ai_destroyed}"
        )

    # =====================================================
    # DESTROY SHIP
    # =====================================================

    def destroy_ship(
        self,
        board,
        ships,
        buttons,
        row,
        col
    ):

        for ship in ships:

            if ship["destroyed"]:
                continue

            if ship["weak"] == (row, col): # Memeriksa apakah koordinat peluru tepat mengenai titik kelemahan (kepala) kapal

                ship["destroyed"] = True

                for r, c in ship["positions"]:

                    board[r][c] = "D" # Mengubah status seluruh bagian kapal tersebut menjadi "D" (Destroyed) secara instan

                    buttons[r][c].config(
                        bg=NEON_RED,
                        text="☠"
                    )

                return len(ship["positions"]) # Mengembalikan total ukuran kapal untuk kalkulasi hit instan

        return 0

    # =====================================================
    # CHECK WIN
    # =====================================================

    def all_destroyed(self, ships):

        return all(ship["destroyed"] for ship in ships) # Mengembalikan True jika seluruh objek kapal di dalam list berstatus hancur

    # =====================================================
    # PLAYER SHOOT
    # =====================================================

    def player_shoot(self, row, col):

        if not self.player_turn: # Mencegah player menembak saat giliran AI sedang berjalan
            return

        val = self.ai_board[row][col]

        if val in ["X", "O", "D"]: # Mengabaikan tembakan jika player mengklik kotak yang sudah pernah ditembak sebelumnya
            return

        # weak point
        destroyed = self.destroy_ship(
            self.ai_board,
            self.ai_ships,
            self.ai_buttons,
            row,
            col
        )

        if destroyed > 0:

            self.player_hits += destroyed
            self.player_destroyed += 1

            self.update_scoreboard()

            self.info_label.config(
                text="☠ ENEMY SHIP DESTROYED!"
            )

            if self.all_destroyed(self.ai_ships): # Validasi apakah semua kapal AI musuh telah rata dihancurkan

                self.game_over(True)

            return

        # normal hit
        if val == "S":

            self.ai_board[row][col] = "X"

            self.ai_buttons[row][col].config(
                bg=NEON_YELLOW,
                text="✦"
            )

            self.player_hits += 1

            self.update_scoreboard()

            self.info_label.config(
                text="💥 HIT! YOUR TURN AGAIN"
            )

        # miss
        else:

            self.ai_board[row][col] = "O"

            self.ai_buttons[row][col].config(
                bg="#5c677d"
            )

            self.player_turn = False

            self.info_label.config(
                text="🤖 AI TURN"
            )

            self.root.after(700, self.ai_turn) # Menjalankan giliran AI secara otomatis setelah jeda waktu 700 milidetik

    # =====================================================
    # AI TURN
    # =====================================================

    def ai_turn(self):

        while True:

            # EASY
            if self.difficulty.get() == "Easy":

                row = random.randint(0, SIZE-1)
                col = random.randint(0, SIZE-1)

            # MEDIUM / HARD
            else:

                if self.hunt_targets: # Jika daftar koordinat berburu terisi, AI akan memprioritaskan menembak area sekitar ledakan tersebut

                    row, col = self.hunt_targets.pop(0)

                else:

                    possible = []

                    for r in range(SIZE):
                        for c in range(SIZE):

                            if (r+c) % 2 == 0: # Menggunakan algoritma pola papan catur (Parity Hunt) untuk efisiensi pencarian acak

                                if self.player_board[r][c] in ["~", "S"]:

                                    possible.append((r, c))

                    row, col = random.choice(possible)

            if self.player_board[row][col] in ["~", "S"]:
                break

        # weak point destroy
        destroyed = self.destroy_ship(
            self.player_board,
            self.player_ships,
            self.player_buttons,
            row,
            col
        )

        if destroyed > 0:

            self.ai_hits += destroyed
            self.ai_destroyed += 1

            self.update_scoreboard()

            self.update_player_board()

            self.info_label.config(
                text="☠ AI DESTROYED YOUR SHIP!"
            )

            if self.all_destroyed(self.player_ships): # Validasi jika semua kapal milik player telah berhasil dihancurkan oleh AI

                self.game_over(False)
                return

            self.root.after(700, self.ai_turn)

            return

        # normal hit
        if self.player_board[row][col] == "S":

            self.player_board[row][col] = "X"

            self.ai_hits += 1

            neighbors = [
                (row+1, col),
                (row-1, col),
                (row, col+1),
                (row, col-1)
            ]

            for nr, nc in neighbors:

                if 0 <= nr < SIZE and 0 <= nc < SIZE:

                    if self.player_board[nr][nc] in ["~", "S"]:

                        if (nr, nc) not in self.hunt_targets:

                            self.hunt_targets.append((nr, nc)) # Menambahkan koordinat sekitar ke daftar buruan AI selanjutnya

            self.update_player_board()

            self.update_scoreboard()

            self.info_label.config(
                text="🤖 AI HIT!"
            )

            self.root.after(700, self.ai_turn)

        # miss
        else:

            self.player_board[row][col] = "O"

            self.update_player_board()

            self.player_turn = True

            self.info_label.config(
                text="🎯 YOUR TURN"
            )

    # =====================================================
    # RESET GAME
    # =====================================================

    def reset_game(self):

        self.player_board = [["~"] * SIZE for _ in range(SIZE)]
        self.ai_board = [["~"] * SIZE for _ in range(SIZE)]

        self.player_ships.clear()
        self.ai_ships.clear()

        self.hunt_targets.clear()

        self.player_hits = 0
        self.ai_hits = 0

        self.player_destroyed = 0
        self.ai_destroyed = 0

        self.player_turn = False

        self.placing_index = 0

        self.orientation = "H"

        for r in range(SIZE):
            for c in range(SIZE):

                self.player_buttons[r][c].config(
                    bg=GRID,
                    text=""
                )

                self.ai_buttons[r][c].config(
                    bg=GRID,
                    text=""
                )

        self.generate_ai_ships()

        self.update_scoreboard()

        self.info_label.config(
            text="Place ship size 5"
        )

    # =====================================================
    # GAME OVER
    # =====================================================

    def game_over(self, win):

        if win: # Kondisi percabangan untuk memunculkan notifikasi box dialog sesuai status akhir permainan (Menang/Kalah)

            result = messagebox.askyesno(
                "VICTORY",
                "🎉 YOU WIN!\n\nPlay Again?"
            )

        else:

            result = messagebox.askyesno(
                "DEFEAT",
                "💀 AI WINS!\n\nPlay Again?"
            )

        if result: # Jika user memilih opsi 'Yes' (True) pada kotak dialog, seluruh game akan di-reset ulang

            self.reset_game()

        else:

            self.root.destroy() # Jika user memilih opsi 'No' (False), window aplikasi utama Tkinter akan ditutup secara aman


# =========================================================
# START GAME
# =========================================================

root = tk.Tk()

game = BattleshipElite(root)

root.mainloop()
