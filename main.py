"""
지뢰찾기 게임 - Minesweeper
Python + Tkinter 기반
"""

import tkinter as tk
from tkinter import messagebox
import random

class Cell:
    """각 셀을 나타내는 클래스"""
    def __init__(self, row, col, parent, game):
        self.row = row
        self.col = col
        self.game = game  # 게임 인스턴스 참조
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.button = tk.Button(
            parent,
            width=2,
            height=1,
            font=('Arial', 14, 'bold'),
            relief=tk.RAISED,
            bg='#d3d3d3'
        )
        self.bind_events()
    
    def bind_events(self):
        """마우스 이벤트 바인딩"""
        self.button.bind('<Button-1>', lambda e: self.on_left_click())
        self.button.bind('<Button-3>', lambda e: self.on_right_click())
    
    def on_left_click(self):
        """좌클릭 이벤트"""
        if not self.is_revealed and not self.is_flagged:
            self.game.reveal_cell(self.row, self.col)
    
    def on_right_click(self):
        """우클릭 이벤트 (깃발)"""
        if not self.is_revealed:
            self.game.toggle_flag(self.row, self.col)
    
    def render(self):
        """셀 렌더링"""
        if self.is_revealed:
            if self.is_mine:
                self.button.config(
                    text='💣',
                    bg='#ff6b6b',
                    fg='black'
                )
            elif self.neighbor_mines > 0:
                colors = {
                    1: '#1976D2',  # 파란색
                    2: '#388E3C',  # 초록색
                    3: '#D32F2F',  # 빨간색
                    4: '#7B1FA2',  # 보라색
                    5: '#FF8F00',  # 주황색
                    6: '#00BCD4',  # 하늘색
                    7: '#000000',  # 검정색
                    8: '#757575'   # 회색
                }
                self.button.config(
                    text=str(self.neighbor_mines),
                    bg='#f5f5f5',
                    fg=colors.get(self.neighbor_mines, 'black')
                )
            else:
                self.button.config(
                    text='',
                    bg='#f5f5f5'
                )
            self.button.config(relief=tk.SUNKEN)
        elif self.is_flagged:
            self.button.config(
                text='🚩',
                bg='#d3d3d3'
            )
        else:
            self.button.config(
                text='',
                bg='#d3d3d3',
                relief=tk.RAISED
            )


class MinesweeperGame:
    """지뢰찾기 게임 클래스"""
    def __init__(self, root):
        self.root = root
        self.root.title("지뢰찾기")
        self.ROWS = 10
        self.COLS = 10
        self.MINES = 10
        self.cells = []
        self.game_over = False
        self.won = False
        self.flags_placed = 0
        
        self.create_widgets()
        self.new_game()
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 상단 정보 패널
        self.info_frame = tk.Frame(self.root, bg='#333', pady=10)
        self.info_frame.pack(fill=tk.X)
        
        # 지뢰 카운트
        self.mine_label = tk.Label(
            self.info_frame,
            text=f"💣 지뢰: {self.MINES}",
            font=('Arial', 14),
            bg='#333',
            fg='white'
        )
        self.mine_label.pack(side=tk.LEFT, padx=20)
        
        # 재시작 버튼
        restart_btn = tk.Button(
            self.info_frame,
            text="🔄 재시작",
            font=('Arial', 12),
            command=self.new_game
        )
        restart_btn.pack(side=tk.RIGHT, padx=20)
        
        # 게임 보드
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)
        
        # 상태 레이블
        self.status_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 14),
            pady=10
        )
        self.status_label.pack()
    
    def new_game(self):
        """새 게임 시작"""
        self.game_over = False
        self.won = False
        self.flags_placed = 0
        self.cells = []
        
        # 기존 위젯 제거
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.status_label.config(text="")
        self.mine_label.config(text=f"💣 지뢰: {self.MINES}")
        
        # 셀 생성 (game 인스턴스 전달)
        for row in range(self.ROWS):
            row_cells = []
            for col in range(self.COLS):
                cell = Cell(row, col, self.board_frame, self)
                cell.button.grid(row=row, column=col, padx=1, pady=1)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        # 지뢰 배치
        self.place_mines()
        
        # 숫자 계산
        self.calculate_numbers()
    
    def place_mines(self):
        """지뢰 무작위 배치"""
        positions = [(r, c) for r in range(self.ROWS) for c in range(self.COLS)]
        random.shuffle(positions)
        
        for i in range(self.MINES):
            row, col = positions[i]
            self.cells[row][col].is_mine = True
    
    def calculate_numbers(self):
        """각 셀의 인접 지뢰 개수 계산"""
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if not self.cells[row][col].is_mine:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < self.ROWS and 0 <= nc < self.COLS:
                                if self.cells[nr][nc].is_mine:
                                    count += 1
                    self.cells[row][col].neighbor_mines = count
    
    def reveal_cell(self, row, col):
        """셀 열기"""
        if self.game_over or self.cells[row][col].is_flagged:
            return
        
        cell = self.cells[row][col]
        cell.is_revealed = True
        cell.render()
        
        if cell.is_mine:
            self.game_lose()
        else:
            # 숫자가 0 인 경우 인접 셀도 열기
            if cell.neighbor_mines == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.ROWS and 0 <= nc < self.COLS:
                            if not self.cells[nr][nc].is_revealed:
                                self.reveal_cell(nr, nc)
            
            self.check_win()
    
    def toggle_flag(self, row, col):
        """깃발 꽂기/제거"""
        if self.game_over:
            return
        
        cell = self.cells[row][col]
        
        if cell.is_flagged:
            cell.is_flagged = False
            self.flags_placed -= 1
        else:
            cell.is_flagged = True
            self.flags_placed += 1
        
        cell.render()
        self.mine_label.config(text=f"💣 지뢰: {self.MINES - self.flags_placed}")
    
    def game_lose(self):
        """패배"""
        self.game_over = True
        self.won = False
        
        # 모든 지뢰 표시
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.cells[row][col].is_mine:
                    self.cells[row][col].is_revealed = True
                    self.cells[row][col].render()
        
        self.status_label.config(text="💥 게임 오버! 지뢰를 밟았습니다.", fg='red')
        messagebox.showerror("게임 오버", "지뢰를 밟았습니다!\n재시작해보세요.")
    
    def check_win(self):
        """승리 조건 확인"""
        if self.game_over:
            return
        
        revealed_count = 0
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.cells[row][col].is_revealed and not self.cells[row][col].is_mine:
                    revealed_count += 1
        
        if revealed_count == self.ROWS * self.COLS - self.MINES:
            self.game_over = True
            self.won = True
            self.status_label.config(text="🎉 축하합니다! 승리했습니다!", fg='green')
            messagebox.showinfo("승리", "축하합니다! 지뢰를 모두 피했습니다!")
    
    def render_all(self):
        """모든 셀 렌더링 (디버깅용)"""
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.cells[row][col].render()


def main():
    root = tk.Tk()
    root.resizable(False, False)
    game = MinesweeperGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
