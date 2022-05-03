import os
import math
import pygame as pg
from settings import *


class Game:
    def __init__(self):
        pg.init()

        self.display = pg.Surface(WIN_SIZE)
        self.window = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption("2 Player Offline Chess")
        pg.display.set_icon(self.get_logo())

        self.chess_grid = self.get_chess_grid()
        self.capture_grids = self.get_capture_grids()

        self.pieces = []
        self.spawn_pieces()

        self.last_active_pos = None
        self.active_piece = None

        self.run = True

    # region DRAW

    def draw_chessboard(self):
        self.display.blit(self.chess_grid.sprite, self.chess_grid.rect)

    def draw_pieces(self):
        for p in self.pieces:
            self.display.blit(p.sprite, p.rect)

    def draw_display(self):
        self.display.fill((128, 0, 0))
        self.draw_chessboard()
        self.draw_pieces()
        self.window.blit(self.display, (0, 0))
        pg.display.update()

    # endregion

    # region GET OBJECTS

    def get_logo(self):
        res_folder = os.path.join(os.getcwd(), "resources")
        logo_path = os.path.join(res_folder, "logo.png")
        raw_img = self.get_image(logo_path)
        return raw_img

    def get_chess_grid(self):
        chess_grid = Chessboard(
            (WIN_WIDTH / 2 - 4 * TILE_SIZE, WIN_HEIGHT),
            (8, 8),
            self.get_chessboard_image(),
        )
        return chess_grid

    def get_capture_grids(self):
        white_capture_grid = CaptureGrid(
            (WIN_WIDTH / 2 - 6 * TILE_SIZE, WIN_HEIGHT), (2, 8), "left"
        )
        black_capture_grid = CaptureGrid(
            (WIN_WIDTH / 2 + 4 * TILE_SIZE, WIN_HEIGHT), (2, 8), "right"
        )

        capture_grids = {}
        capture_grids["white"] = white_capture_grid
        capture_grids["black"] = black_capture_grid

        return capture_grids

    def spawn_pieces(self):
        res_folder = os.path.join(os.getcwd(), "resources")
        pieces_folder = os.path.join(res_folder, "pieces")

        for x in range(8):
            for y in range(8):
                tile_pos = (x, y)

                if not PIECES_ORDER.get(tile_pos):
                    continue

                piece_name = PIECES_ORDER.get(tile_pos)
                image_path = os.path.join(pieces_folder, f"{piece_name}.png")
                image = self.get_image(image_path)
                size = PAWN_SIZE if piece_name.endswith("pawn") else PIECE_SIZE
                resized_image = self.scale_with_ratio(image, size)

                p = Piece(
                    piece_name, resized_image, self.chess_grid.tile_to_pos((x, y))
                )

                self.pieces.append(p)

    def get_chessboard_image(self):
        res_folder = os.path.join(os.getcwd(), "resources")
        chessboard_path = os.path.join(res_folder, "chessboard.png")
        raw_img = self.get_image(chessboard_path)
        chessboard_img = pg.transform.scale(raw_img, (WIN_HEIGHT, WIN_HEIGHT))
        return chessboard_img

    # endregion

    # region MOVEMENT

    def move_active_piece(self):
        self.active_piece.rect.center = pg.mouse.get_pos()

    def drop_active_piece(self):

        if not self.active_piece:
            return

        closest_pos = self.get_closest_pos()

        self.handle_drop_situation(closest_pos)

    def handle_drop_situation(self, pos):
        piece_at_pos = self.get_piece_at_pos(pos)

        if piece_at_pos:
            if piece_at_pos.color == self.active_piece.color:
                if self.chess_grid.is_hovering(self.last_active_pos):
                    self.active_piece.rect.center = self.last_active_pos
                else:
                    self.capture(self.active_piece)
            else:
                self.capture(piece_at_pos)
                self.active_piece.rect.center = pos
        else:
            self.active_piece.rect.center = pos

        self.active_piece = None
        self.last_active_pos = None

    def capture(self, piece):
        capture_grid = self.capture_grids[piece.color]
        capture_grid.captured_pieces.append(piece)
        capture_grid.update_positions()

    def free(self, piece):
        capture_grid = self.capture_grids[piece.color]

        if piece not in capture_grid.captured_pieces:
            return

        capture_grid.captured_pieces.remove(piece)
        capture_grid.update_positions()

    # endregion

    # region CHECK

    def check_pieces_hover(self):
        for p in self.pieces:

            if p.rect.collidepoint((pg.mouse.get_pos())):
                self.active_piece = p
                self.last_active_pos = p.rect.center
                self.free(p)

                return

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.check_pieces_hover()
            elif event.type == pg.MOUSEBUTTONUP:
                self.drop_active_piece()

    # endregion

    # region MISC

    def get_closest_pos(self):
        distances_dict = {}

        for x in range(8):
            for y in range(8):
                pos = self.chess_grid.tile_to_pos((x, y))
                dist = self.distance(pg.mouse.get_pos(), pos)

                distances_dict[dist] = (x, y)

        distances_keys = list(distances_dict.keys())
        min_dist = min(distances_keys)
        closest_pos = self.chess_grid.tile_to_pos(distances_dict[min_dist])

        return closest_pos

    def get_piece_at_pos(self, pos):
        for p in self.pieces:
            if p.rect.center == pos:
                return p
        return None

    @staticmethod
    def scale_with_ratio(image, size):
        width = image.get_width()
        height = image.get_height()
        mult_factor = size / max(width, height)
        scaled_image = pg.transform.scale(
            image, (width * mult_factor, height * mult_factor)
        )
        return scaled_image

    @staticmethod
    def get_image(filepath):
        raw_img = pg.image.load(filepath)
        return raw_img

    @staticmethod
    def distance(pos1, pos2):
        dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        return dist

    def draw_text(self, text, size, pos, color=(255, 255, 255)):
        font_name = pg.font.get_default_font()
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topright = pos
        self.display.blit(text_surface, text_rect)

    # endregion

    def main_loop(self):
        while self.run:
            self.check_events()

            if self.active_piece:
                self.move_active_piece()

            self.draw_display()


class Grid:
    def __init__(self, bl_pos, size_in_tiles):
        self.bl_pos = bl_pos
        self.size_in_tiles = size_in_tiles
        self.width_in_tiles = size_in_tiles[0]
        self.height_in_tiles = size_in_tiles[1]
        self.width = self.width_in_tiles * TILE_SIZE
        self.height = self.height_in_tiles * TILE_SIZE

    def pos_to_tile(self, pos):
        tile_x = (pos[0] - self.bl_pos[0]) // TILE_SIZE
        tile_y = (WIN_HEIGHT - pos[1]) // TILE_SIZE
        return (tile_x, tile_y)

    def tile_to_pos(self, tile_pos):
        x = tile_pos[0] * TILE_SIZE + TILE_SIZE / 2 + self.bl_pos[0]
        y = WIN_HEIGHT - (tile_pos[1] * TILE_SIZE + TILE_SIZE / 2)
        return (int(x), int(y))

    def is_hovering(self, pos):
        if self.bl_pos[0] < pos[0] < self.bl_pos[0] + self.width:
            return True
        return False


class Chessboard(Grid):
    def __init__(self, bl_pos, size_in_tiles, sprite):
        super().__init__(bl_pos, size_in_tiles)
        self.sprite = sprite
        self.rect = self.sprite.get_rect()

        self.rect.bottomleft = self.bl_pos


class CaptureGrid(Grid):
    def __init__(self, bl_pos, size_in_tiles, side):
        super().__init__(bl_pos, size_in_tiles)
        self.side = side
        self.captured_pieces = []

    def index_to_tile(self, index):
        tile_x = (
            (self.width_in_tiles - 1) - (index // self.height_in_tiles)
            if self.side == "left"
            else (index // self.height_in_tiles)
        )

        tile_y = (self.height_in_tiles - 1) - (index % self.height_in_tiles)

        return (tile_x, tile_y)

    def index_to_pos(self, index):
        tile_pos = self.index_to_tile(index)
        pos = self.tile_to_pos(tile_pos)
        return pos

    def update_positions(self):
        for i, p in enumerate(self.captured_pieces):
            p.rect.center = self.index_to_pos(i)


class Piece:
    def __init__(self, name, sprite, pos):
        self.sprite = sprite
        self.rect = sprite.get_rect()
        self.color = name.split("_")[0]

        self.rect.center = pos
