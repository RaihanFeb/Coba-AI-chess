import chess

def display_board(board):
    piece_symbols = {
        chess.PAWN: "♙♟",
        chess.KNIGHT: "♘♞",
        chess.BISHOP: "♗♝",
        chess.ROOK: "♖♜",
        chess.QUEEN: "♕♛",
        chess.KING: "♔♚",
    }

    board_str = ""
    for rank in range(8, 0, -1):
        board_str += f"{rank} "
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = board.piece_at(square)
            if piece:
                symbol_index = 0 if piece.color == chess.WHITE else 1
                board_str += piece_symbols[piece.piece_type][symbol_index] + " "
            else:
                board_str += ". "
        board_str += "\n"
    board_str += "  a b c d e f g h\n"
    print(board_str)

def evaluate_board(board):
    material_count = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }
    score = 0
    for piece_type in material_count:
        score += len(board.pieces(piece_type, chess.WHITE)) * material_count[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * material_count[piece_type]
    return score

def minimax(board, depth, is_maximizing):
    # -+ = 
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if is_maximizing:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board, depth):
   
    best_move = None
    max_eval = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move

player_color = None
while player_color not in ["white", "black"]:
    player_color = input("Do you want to play as White or Black? (white/black): ").strip().lower()

# Difficulty
difficulty = None
while not isinstance(difficulty, int):
    try:
        difficulty = int(input("Choose AI difficulty level (1 - Easy, 2 - Medium, 3 - Hard): "))
        if difficulty not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Invalid input. Please choose 1, 2, or 3.")
        difficulty = None

# Elo
depth_map = {1: 1, 2: 2, 3: 3}
ai_depth = depth_map[difficulty]

# Board
board = chess.Board()
print("Initial Board:")
display_board(board)

while not board.is_game_over():
    if (board.turn == chess.WHITE and player_color == "white") or (board.turn == chess.BLACK and player_color == "black"):
        print("Your move (type 0 to quit):")
        user_move = input()
        if user_move == "0":
            print("Game ended by user.")
            break
        try:
            board.push_san(user_move)
        except ValueError:
            print("Invalid move. Try again.")
            continue
    else:
        print("Raibot v2 is thinking...")
        ai_move = find_best_move(board, depth=ai_depth)
        board.push(ai_move)
        print(f"Raibot v2 plays: {ai_move}")
    
    display_board(board)

# End
if board.is_game_over():
    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        print(f"Checkmate! {winner} wins!")
    elif board.is_stalemate():
        print("Stalemate! It's a draw!")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material!")
else:
    print("Game stopped. Here's the final board:")
    display_board(board)
