import tkinter as tk
from tkinter import Toplevel
import time
import random


# generate sudokunya
def generate_full_board():
    board = [[0] * 9 for _ in range(9)]

    def is_safe(r, c, num):
        if num in board[r]:
            return False
        if num in [board[i][c] for i in range(9)]:
            return False
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range (br, br, + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == num:
                    return False
            return True
        
        def solve():
            for r in range(9):
                for c in range(9):
                    if board [r][c] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if is_safe(r, c, num):
                                board[r][c] = num
                                if solve():
                                    return True
                                board[r][c] = 0
                        return False
            return True
        solve()
        return board

def create_puzzle(solution, remove_count=45):
    puzzle = [row[:] for row in solution]
    removed = 0

    while removed < remove_count:
        r = random.radiant(0,8)
        c = random.radiant(0,8)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            removed += 1
        
    return puzzle

#===============================================================================
#                                   main game class
# ==================================================================================
class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("850x520")
        self.root.conigure(bg="#f0f0f0")

        self.cells = {}
        self.start_time = time.time()

        self.solution = generate_full_board()
        self.puzzle = create_puzzle(self.solution, remove_count=45)

        self.create_title()
        self.create_layout()
        self.update_timer()

# ====================================================================================
#                                        UI
# =====================================================================================
    def create_title(self):
        tk.Label(
            self.root, 
            text="Sudoku Game",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333"
        ).pack(pady=10)

    def create_layout(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=20)

        self.grid_frame = tk.Frame(main_frame, bg="#333")
        self.grid_frame.grid(row=0, column=0, padx=20)

        self.create_grid()

        side_panel = tk.Frame(main_frame, bg="#f0f0f0")
        side_panel.grid(row=0, column=1, sticky="n")

        self.timer_label = tk.Label(
            side_panel,
            text="Time: 00:00",
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="#333"
        )
        self.timer_label.pack(pady=20)

        self.create_buttons(side_panel)

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                bg_color = "#fff" if (row // 3 + col // 3) % 2 == 0 else "#eee"

                entry = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=("Arial", 18),
                    justify="center",
                    bg=bg_color,
                    relief="solid",
                    bd=1
                )

                entry.grid(row=row, column=col, padx=1, pady=1, ipadx=6, ipady=6)

                if self.puzzle[row][col] != 0:
                    entry.insert(0, self.puzzle[row][col])
                    entry.config(state="disabled", disabledforeground="#333")
                else:
                    entry.bind(
                        "<KeyRelease>",
                        lambda e, r=row, c=col: self.validate_cell(r, c)
                    )

                self.cells[(row, col)] = entry
            
    def create_buttons(self, parent):
        tk.Button(
            parent,
            text="check sudoku",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="#fff",
            width=15,
            command=self.check_solution
        ).pack(pady=10)

        tk.Button(
            parent,
            text="reset game",
            font=("Arial", 12),
            bg="#f44336",
            fg="#fff",
            width=15,
            command=self.reset_board
        ).pack(pady=10)

# ======================================================================================
#                                       timer
# ======================================================================================
def update_timer(self):
    elapsed = int(time.time() - self.start_time)
    minutes, seconds = divmod(elapsed, 60)
    self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
    self.root.after(1000, self.update_timer)


# ======================================================================================
#                                       validation
# ======================================================================================
def validate_cell(self, row, col):
    entry = self.cells[(row, col)]
    value = entry.get()

    if not value.isdigit() or not (1 <= int(value) <= 9):
        entry.config(bg="red")
        return

    if int(value) != self.solution[row][col]:
        entry.config(bg="red")
    else:
        entry.config(bg="white")


# =============================================================================================
#                                      game actions
# =============================================================================================
def check_solution(self):
    for r in range(9):
        for c in range(9):
            val = self.cells[(r, c)].get()
            if not val or not val.isdigit():
                self.show_message("❌ Incomplete", "Please fill all cells before checking.")
                return
            if int(val) != self.solution[r][c]:
                self.show_message("❌ Incorrect", "Some cells are incorrect. Keep trying!")
                return
    self.show_message("✅ Correct", "Congratulations! You solved the puzzle!")

def reset_board(self):
    self.start_time = time.time()
    self.solution = generate_full_board()
    self.puzzle = create_puzzle(self.solution, remove_count=45)

    for widget in self.grid_frame.winfo_children():
        widget.destroy()

    self.cells.clear()    
    self.create_grid()

# ==============================================================================================
#                                      message popup
# ==============================================================================================
def show_popup(self, title, message):
    popup = Toplevel(self.root)
    popup.title(title)
    popup.geometry("300x150")
    popup.configure(bg="#f0f0f0")

    tk.Label(
        popup,
        text=title, 
        font=("Arial", 14),
        bg="#f0f0f0",
    ).pack(pady=15)

    tk.Label(
        popup,
        text=message,
        font=("Arial", 12),
        bg="#f0f0f0",
    ).pack(pady=10)

    tk.Button(
        popup,
        text="OK",
        font=("Arial", 12),
        bg="#4CAF50",
        fg="#fff",
        width=10,
        command=popup.destroy
    ).pack(pady=10)

# ==============================================================================================
#                                      main entry point
# ==============================================================================================
if __name__ == "__main__":
    root = tk.Tk()
    SudokuGame(root)
    root.mainloop()