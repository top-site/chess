import chess
import chess.engine
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import time

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Python Chess GUI")
        self.root.configure(bg='#2c3e50')
        
        # Chess board and engines
        self.board = chess.Board()
        self.engine_white = None
        self.engine_black = None
        # self.engine_path = "komodo"  # Update this to your Komodo engine path
        self.engine_path = "stockfish"  # Update this to your stockfish engine path
        self.engine_thinking = False
        self.engine_time_limit = 2.0  # seconds
        self.engine_battle_active = False
        
        # Enhanced visual settings
        self.board_size = 480
        self.square_size = self.board_size // 8
        self.light_square_color = "#f0d9b5"
        self.dark_square_color = "#b58863"
        self.highlight_color = "#ffff00"
        self.last_move_color = "#90ee90"
        self.selected_color = "#87ceeb"
        
        # GUI elements
        self.create_widgets()
        self.draw_board()
        
        # Start engines in separate threads
        self.start_engines()

    def create_widgets(self):
        # Configure window style
        self.root.geometry("1100x600")
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Move history
        self.history_frame = tk.Frame(self.main_frame, bg='#34495e', relief=tk.RAISED, bd=3)
        self.history_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # History title
        self.history_title = tk.Label(
            self.history_frame, 
            text="Move History", 
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.history_title.pack(pady=(10, 5))
        
        # Move list with scrollbar
        self.move_list_frame = tk.Frame(self.history_frame, bg='#34495e')
        self.move_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.move_list = tk.Listbox(
            self.move_list_frame, 
            height=25,
            width=20,
            font=("Consolas", 10),
            bg='#ecf0f1',
            fg='#2c3e50',
            selectbackground='#3498db',
            relief=tk.FLAT,
            bd=1
        )
        
        self.move_scrollbar = tk.Scrollbar(self.move_list_frame, orient=tk.VERTICAL)
        self.move_list.config(yscrollcommand=self.move_scrollbar.set)
        self.move_scrollbar.config(command=self.move_list.yview)
        
        self.move_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.move_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Save/Load buttons frame
        self.save_load_frame = tk.Frame(self.history_frame, bg='#34495e')
        self.save_load_frame.pack(fill=tk.X, padx=5, pady=(5, 10))
        
        self.save_btn = tk.Button(
            self.save_load_frame,
            text="💾 Save Game",
            command=self.save_game,
            font=("Arial", 10, "bold"),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        self.save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.load_btn = tk.Button(
            self.save_load_frame,
            text="📂 Load Game",
            command=self.load_game,
            font=("Arial", 10, "bold"),
            bg='#2ecc71',
            fg='white',
            activebackground='#27ae60',
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        self.load_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)
        
        # Middle - Chess board
        self.board_frame = tk.Frame(self.main_frame, bg='#34495e', relief=tk.RAISED, bd=3)
        self.board_frame.pack(side=tk.LEFT, padx=10)
        
        # Board title
        self.board_title = tk.Label(
            self.board_frame, 
            text="Chess Board", 
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.board_title.pack(pady=(10, 5))
        
        # Chess board canvas with border
        self.canvas_frame = tk.Frame(self.board_frame, bg='#2c3e50', bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(padx=10, pady=10)
        
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=self.board_size, 
            height=self.board_size,
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        
        # Right side - Control panel
        self.control_frame = tk.Frame(self.main_frame, bg='#34495e', relief=tk.RAISED, bd=3)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control panel title
        self.control_title = tk.Label(
            self.control_frame, 
            text="Game Controls", 
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.control_title.pack(pady=(15, 10))
        
        # Engine status with better styling
        self.status_frame = tk.Frame(self.control_frame, bg='#34495e')
        self.status_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.engine_status = tk.Label(
            self.status_frame, 
            text="Engines: Disconnected",
            font=("Arial", 10, "bold"),
            bg='#e74c3c',
            fg='white',
            relief=tk.RAISED,
            bd=1,
            padx=10,
            pady=5
        )
        self.engine_status.pack(fill=tk.X)
        
        # Button frame with improved styling
        self.button_frame = tk.Frame(self.control_frame, bg='#34495e')
        self.button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Enhanced buttons
        button_style = {
            'font': ("Arial", 10, "bold"),
            'relief': tk.RAISED,
            'bd': 2,
            'padx': 10,
            'pady': 5,
            'cursor': 'hand2'
        }
        
        self.new_game_btn = tk.Button(
            self.button_frame, 
            text="🔄 New Game", 
            command=self.new_game,
            bg='#27ae60',
            fg='white',
            activebackground='#2ecc71',
            **button_style
        )
        self.new_game_btn.pack(fill=tk.X, pady=2)
        
        self.undo_btn = tk.Button(
            self.button_frame, 
            text="↶ Undo Move", 
            command=self.undo_move,
            bg='#f39c12',
            fg='white',
            activebackground='#e67e22',
            **button_style
        )
        self.undo_btn.pack(fill=tk.X, pady=2)
        
        # Engine battle controls
        self.battle_btn = tk.Button(
            self.button_frame, 
            text="▶ Start Engine Battle", 
            command=self.toggle_engine_battle,
            bg='#9b59b6',
            fg='white',
            activebackground='#8e44ad',
            **button_style
        )
        self.battle_btn.pack(fill=tk.X, pady=2)
        
        # Engine settings with improved layout
        self.engine_settings_frame = tk.LabelFrame(
            self.control_frame, 
            text="Engine Settings", 
            font=("Arial", 10, "bold"),
            bg='#34495e',
            fg='#ecf0f1',
            relief=tk.GROOVE,
            bd=2
        )
        self.engine_settings_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Time limit setting
        self.time_frame = tk.Frame(self.engine_settings_frame, bg='#34495e')
        self.time_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            self.time_frame, 
            text="Time Limit (s):", 
            bg='#34495e', 
            fg='#ecf0f1',
            font=("Arial", 9)
        ).pack(side=tk.LEFT)
        
        self.time_limit = tk.DoubleVar(value=self.engine_time_limit)
        self.time_limit_spin = tk.Spinbox(
            self.time_frame, 
            from_=0.1, 
            to=60, 
            increment=0.1,
            textvariable=self.time_limit, 
            width=8,
            font=("Arial", 9),
            relief=tk.SUNKEN,
            bd=1
        )
        self.time_limit_spin.pack(side=tk.RIGHT)
        
        # Game mode selection
        self.mode_frame = tk.Frame(self.engine_settings_frame, bg='#34495e')
        self.mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.game_mode = tk.StringVar(value="player_vs_engine")
        
        tk.Radiobutton(
            self.mode_frame, 
            text="Player vs Engine", 
            variable=self.game_mode,
            value="player_vs_engine",
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50',
            font=("Arial", 9),
            command=self.on_mode_change
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            self.mode_frame, 
            text="Player vs Player", 
            variable=self.game_mode,
            value="player_vs_player",
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50',
            font=("Arial", 9),
            command=self.on_mode_change
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            self.mode_frame, 
            text="Engine vs Engine", 
            variable=self.game_mode,
            value="engine_vs_engine",
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50',
            font=("Arial", 9),
            command=self.on_mode_change
        ).pack(anchor=tk.W)
        
        # Engine strength
        self.strength_frame = tk.Frame(self.engine_settings_frame, bg='#34495e')
        self.strength_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        tk.Label(
            self.strength_frame, 
            text="Engine Strength:", 
            bg='#34495e', 
            fg='#ecf0f1',
            font=("Arial", 9)
        ).pack()
        
        self.engine_level = tk.IntVar(value=20)
        self.level_slider = tk.Scale(
            self.strength_frame, 
            from_=1, 
            to=20, 
            orient=tk.HORIZONTAL,
            variable=self.engine_level,
            bg='#34495e',
            fg='#ecf0f1',
            highlightthickness=0,
            font=("Arial", 8)
        )
        self.level_slider.pack(fill=tk.X)

    def save_game(self):
        """Save the current game to a text file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Game"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w') as f:
                # Save the move history
                for move in self.board.move_stack:
                    f.write(f"{move.uci()}\n")
            messagebox.showinfo("Success", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game: {str(e)}")

    def load_game(self):
        """Load a game from a text file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Load Game"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r') as f:
                moves = [line.strip() for line in f.readlines() if line.strip()]
                
            # Reset the board
            self.board.reset()
            self.move_list.delete(0, tk.END)
            if hasattr(self, 'selected_square'):
                delattr(self, 'selected_square')
            
            # Replay all moves
            for move_uci in moves:
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in self.board.legal_moves:
                        self.board.push(move)
                        self.update_move_list()
                    else:
                        raise ValueError(f"Illegal move: {move_uci}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load move {move_uci}: {str(e)}")
                    return
                    
            self.draw_board()
            messagebox.showinfo("Success", "Game loaded successfully!")
            
            # If in engine mode and it's engine's turn
            if (self.game_mode.get() == "player_vs_engine" and
                not self.board.is_game_over() and
                self.board.turn == chess.BLACK):
                self.engine_move()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {str(e)}")

    def on_mode_change(self):
        """Handle changes in game mode"""
        if self.engine_battle_active:
            self.toggle_engine_battle()
        
        if self.game_mode.get() == "engine_vs_engine":
            self.battle_btn.config(state=tk.NORMAL)
        else:
            self.battle_btn.config(state=tk.DISABLED)
            
        if (self.game_mode.get() == "player_vs_engine" and 
            self.engine_black and not self.engine_thinking and
            self.board.turn == chess.BLACK):
            self.engine_move()

    def toggle_engine_battle(self):
        """Start or stop the engine vs engine battle"""
        if not self.engine_battle_active:
            # Start the battle
            if not (self.engine_white and self.engine_black):
                messagebox.showerror("Error", "Engines not ready")
                return
                
            self.engine_battle_active = True
            self.battle_btn.config(text="⏸ Pause Engine Battle")
            self.new_game_btn.config(state=tk.DISABLED)
            self.undo_btn.config(state=tk.DISABLED)
            
            # Start the first move if it's white's turn
            if self.board.turn == chess.WHITE:
                self.engine_move()
        else:
            # Stop the battle
            self.engine_battle_active = False
            self.battle_btn.config(text="▶ Start Engine Battle")
            self.new_game_btn.config(state=tk.NORMAL)
            self.undo_btn.config(state=tk.NORMAL)

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw squares with improved colors
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = (7 - row) * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                color = self.light_square_color if (row + col) % 2 == 0 else self.dark_square_color
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill=color, 
                    outline='#8b4513', 
                    width=1,
                    tags=f"square_{row}_{col}"
                )
                
                # Draw enhanced pieces
                piece = self.board.piece_at(chess.square(col, row))
                if piece:
                    piece_symbol = self.get_enhanced_piece_symbol(piece)
                    text_color = '#1a1a1a' if piece.color == chess.WHITE else '#8b0000'
                    shadow_color = '#d3d3d3' if piece.color == chess.WHITE else '#4d0000'
                    
                    # Draw shadow for depth effect
                    self.canvas.create_text(
                        x1 + self.square_size // 2 + 1, 
                        y1 + self.square_size // 2 + 1,
                        text=piece_symbol, 
                        font=("Arial", 32, "bold"),
                        fill=shadow_color,
                        tags=f"piece_shadow_{row}_{col}"
                    )
                    
                    # Draw main piece
                    self.canvas.create_text(
                        x1 + self.square_size // 2, 
                        y1 + self.square_size // 2,
                        text=piece_symbol, 
                        font=("Arial", 32, "bold"),
                        fill=text_color,
                        tags=f"piece_{row}_{col}"
                    )
        
        # Highlight last move with better colors
        if self.board.move_stack:
            last_move = self.board.peek()
            self.highlight_square(last_move.from_square, self.last_move_color)
            self.highlight_square(last_move.to_square, self.last_move_color)
        
        # Highlight selected square
        if hasattr(self, 'selected_square'):
            self.highlight_square(self.selected_square, self.selected_color)
        
        # Draw coordinates with better styling
        for i in range(8):
            # Files (a-h)
            self.canvas.create_text(
                (i + 0.5) * self.square_size, 
                self.board_size - 10,
                text=chr(97 + i), 
                font=("Arial", 12, "bold"),
                fill='#2c3e50'
            )
            
            # Ranks (1-8)
            self.canvas.create_text(
                10, 
                (7 - i + 0.5) * self.square_size,
                text=str(i + 1), 
                font=("Arial", 12, "bold"),
                fill='#2c3e50'
            )

    def get_enhanced_piece_symbol(self, piece):
        # Enhanced Unicode chess symbols
        white_symbols = {
            chess.PAWN: "♙",
            chess.KNIGHT: "♘", 
            chess.BISHOP: "♗",
            chess.ROOK: "♖",
            chess.QUEEN: "♕",
            chess.KING: "♔"
        }
        
        black_symbols = {
            chess.PAWN: "♟",
            chess.KNIGHT: "♞",
            chess.BISHOP: "♝", 
            chess.ROOK: "♜",
            chess.QUEEN: "♛",
            chess.KING: "♚"
        }
        
        if piece.color == chess.WHITE:
            return white_symbols.get(piece.piece_type, "")
        else:
            return black_symbols.get(piece.piece_type, "")

    def highlight_square(self, square, color):
        row = chess.square_rank(square)
        col = chess.square_file(square)
        x1 = col * self.square_size
        y1 = (7 - row) * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        
        self.canvas.create_rectangle(
            x1 + 3, y1 + 3, x2 - 3, y2 - 3, 
            outline=color, 
            width=4,
            tags=f"highlight_{row}_{col}"
        )

    def on_square_clicked(self, event):
        if self.engine_thinking or self.game_mode.get() == "engine_vs_engine":
            return
        
        col = event.x // self.square_size
        row = 7 - (event.y // self.square_size)
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        square = chess.square(col, row)
        
        if hasattr(self, 'selected_square'):
            # Try to make a move
            move = chess.Move(self.selected_square, square)
            
            # Check for pawn promotion
            if (self.board.piece_at(self.selected_square) and 
                self.board.piece_at(self.selected_square).piece_type == chess.PAWN and
                (chess.square_rank(square) in [0, 7])):
                move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            
            if move in self.board.legal_moves:
                self.make_move(move)
                delattr(self, 'selected_square')
                
                # If player vs engine and it's engine's turn
                if (self.game_mode.get() == "player_vs_engine" and
                    not self.board.is_game_over() and
                    self.board.turn == chess.BLACK):
                    self.engine_move()
            else:
                # Select a different piece
                if (self.board.piece_at(square) and 
                    self.board.color_at(square) == self.board.turn):
                    self.selected_square = square
                else:
                    delattr(self, 'selected_square')
        else:
            # Select a piece
            if (self.board.piece_at(square) and 
                self.board.color_at(square) == self.board.turn):
                self.selected_square = square
        
        self.draw_board()

    def make_move(self, move):
        self.board.push(move)
        self.update_move_list()
        self.draw_board()
        
        # Check for game over
        if self.board.is_game_over():
            result = self.board.result()
            if result == "1-0":
                messagebox.showinfo("Game Over", "White wins! 🎉")
                if self.engine_battle_active:
                    self.toggle_engine_battle()
            elif result == "0-1":
                messagebox.showinfo("Game Over", "Black wins! 🎉")
                if self.engine_battle_active:
                    self.toggle_engine_battle()
            elif result == "1/2-1/2":
                messagebox.showinfo("Game Over", "Draw! 🤝")
                if self.engine_battle_active:
                    self.toggle_engine_battle()
        elif self.engine_battle_active and not self.engine_thinking:
            # Continue the engine battle
            self.engine_move()

    def update_move_list(self):
        move_count = len(self.board.move_stack)
        
        if move_count % 2 == 1:
            move_number = f"{move_count // 2 + 1}."
            self.move_list.insert(tk.END, move_number)
        
        if move_count > 0:
            last_move = self.board.peek()
            self.move_list.insert(tk.END, f"  {last_move.uci()}")
        
        self.move_list.see(tk.END)

    def engine_move(self):
        if self.engine_thinking or self.board.is_game_over():
            return
        
        current_engine = self.engine_white if self.board.turn == chess.WHITE else self.engine_black
        if not current_engine:
            return
        
        self.engine_thinking = True
        self.engine_status.config(
            text=f"Engine ({'White' if self.board.turn == chess.WHITE else 'Black'}): Thinking...", 
            bg='#f39c12',
            fg='white'
        )
        
        def engine_thread():
            try:
                # Set engine level if supported
                if hasattr(current_engine, 'configure'):
                    try:
                        current_engine.configure({"Skill Level": self.engine_level.get()})
                    except chess.engine.EngineError:
                        pass
                
                result = current_engine.play(
                    self.board,
                    chess.engine.Limit(time=self.time_limit.get()),
                    info=chess.engine.INFO_ALL
                )
                
                self.root.after(0, self.on_engine_move_received, result.move)
            except Exception as e:
                self.root.after(0, self.on_engine_error, str(e))
        
        threading.Thread(target=engine_thread, daemon=True).start()

    def on_engine_move_received(self, move):
        self.engine_thinking = False
        self.engine_status.config(
            text="Engines: Ready", 
            bg='#27ae60',
            fg='white'
        )
        
        if move in self.board.legal_moves:
            self.make_move(move)
        else:
            messagebox.showerror("Error", "Engine returned illegal move")
            if self.engine_battle_active:
                self.toggle_engine_battle()

    def on_engine_error(self, error):
        self.engine_thinking = False
        self.engine_status.config(
            text="Engine: Error", 
            bg='#e74c3c',
            fg='white'
        )
        messagebox.showerror("Engine Error", error)
        if self.engine_battle_active:
            self.toggle_engine_battle()

    def start_engines(self):
        def engine_init_thread():
            try:
                # Start white engine
                self.engine_white = chess.engine.SimpleEngine.popen_uci(self.engine_path)
                
                # Start black engine (same executable, separate process)
                self.engine_black = chess.engine.SimpleEngine.popen_uci(self.engine_path)
                
                self.root.after(0, self.on_engines_ready)
            except Exception as e:
                self.root.after(0, self.on_engine_init_error, str(e))
        
        threading.Thread(target=engine_init_thread, daemon=True).start()

    def on_engines_ready(self):
        self.engine_status.config(
            text="Engines: Ready", 
            bg='#27ae60',
            fg='white'
        )
        
        if (self.game_mode.get() == "player_vs_engine" and
            self.board.turn == chess.BLACK):
            self.engine_move()
        elif (self.game_mode.get() == "engine_vs_engine" and
              self.engine_battle_active and
              self.board.turn == chess.WHITE):
            self.engine_move()

    def on_engine_init_error(self, error):
        self.engine_status.config(
            text="Engines: Failed to start", 
            bg='#e74c3c',
            fg='white'
        )
        messagebox.showerror("Engine Error", f"Failed to start engines: {error}")
        self.game_mode.set("player_vs_player")

    def new_game(self):
        self.board.reset()
        self.move_list.delete(0, tk.END)
        if hasattr(self, 'selected_square'):
            delattr(self, 'selected_square')
        self.draw_board()
        
        if (self.game_mode.get() == "player_vs_engine" and
            self.board.turn == chess.BLACK and
            self.engine_black and not self.engine_thinking):
            self.engine_move()
        elif (self.game_mode.get() == "engine_vs_engine" and
              self.engine_battle_active and
              self.board.turn == chess.WHITE and
              self.engine_white and not self.engine_thinking):
            self.engine_move()

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            
            # Remove the last move from the list
            if self.move_list.size() > 0:
                last_item = self.move_list.get(self.move_list.size() - 1)
                self.move_list.delete(self.move_list.size() - 1)
                
                # If it was just a move (not a move number), check if we need to remove the move number too
                if not last_item.strip().endswith('.') and self.move_list.size() > 0:
                    prev_item = self.move_list.get(self.move_list.size() - 1)
                    if prev_item.strip().endswith('.'):
                        self.move_list.delete(self.move_list.size() - 1)
            
            if hasattr(self, 'selected_square'):
                delattr(self, 'selected_square')
            self.draw_board()

    def __del__(self):
        if self.engine_white:
            try:
                self.engine_white.quit()
            except:
                pass
        if self.engine_black:
            try:
                self.engine_black.quit()
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    chess_gui = ChessGUI(root)
    root.mainloop()