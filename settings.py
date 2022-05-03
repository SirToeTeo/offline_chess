# WINDOW SETTINGS

WIN_WIDTH = 800 * 1.5
WIN_HEIGHT = 450 * 1.5
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

# GAME SETTINGS

TILE_SIZE = WIN_HEIGHT / 8
PIECE_SIZE = TILE_SIZE * 0.8
PAWN_SIZE = TILE_SIZE * 0.7

# GAME DATA

PIECES_ORDER = {
    (0, 0): "white_rook",
    (1, 0): "white_knight",
    (2, 0): "white_bishop",
    (3, 0): "white_queen",
    (4, 0): "white_king",
    (5, 0): "white_bishop",
    (6, 0): "white_knight",
    (7, 0): "white_rook",
    (0, 1): "white_pawn",
    (1, 1): "white_pawn",
    (2, 1): "white_pawn",
    (3, 1): "white_pawn",
    (4, 1): "white_pawn",
    (5, 1): "white_pawn",
    (6, 1): "white_pawn",
    (7, 1): "white_pawn",
    (0, 7): "black_rook",
    (1, 7): "black_knight",
    (2, 7): "black_bishop",
    (3, 7): "black_queen",
    (4, 7): "black_king",
    (5, 7): "black_bishop",
    (6, 7): "black_knight",
    (7, 7): "black_rook",
    (0, 6): "black_pawn",
    (1, 6): "black_pawn",
    (2, 6): "black_pawn",
    (3, 6): "black_pawn",
    (4, 6): "black_pawn",
    (5, 6): "black_pawn",
    (6, 6): "black_pawn",
    (7, 6): "black_pawn",
}
