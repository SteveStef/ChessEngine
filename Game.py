from Constants import *
from Tile import Tile
import random
import pygame

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

class Minesweeper:
    def __init__(self):
        self.board = [[Tile(0, True) for _ in range(COLS)] for _ in range(ROWS)]
        self.flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.canBreak = True
        self.gameover = False
        self.set_board()

    def set_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if random.randint(1, 100) <= MINE_PERCENTAGE:
                    self.board[row][col].value = "X"

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col].value != "X":
                    count = 0
                    for i in range(max(0, row-1), min(row+2, ROWS)):
                        for j in range(max(0, col-1), min(col+2, COLS)):
                            if self.board[i][j].value == "X":
                                count += 1
                    self.board[row][col].value = count

    def draw_board(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                cell_rect = pygame.Rect(
                    col * (CELL_SIZE + MARGIN) + MARGIN,
                    row * (CELL_SIZE + MARGIN) + MARGIN,
                    CELL_SIZE,
                    CELL_SIZE
                )
                green = GREEN1 if (row+col)%2==0 else GREEN2
                color = green if not self.flags[row][col] else RED2
                if color == RED2:
                    color = RED if (row+col)%2==0 else RED2

                if self.board[row][col].value == "X":
                    if self.board[row][col].hidden: pygame.draw.rect(window, color, cell_rect)
                    else: 
                        pygame.draw.rect(window, RED, cell_rect)
                        font = pygame.font.SysFont(None, CELL_SIZE//2)
                        t = self.board[row][col].value
                        text = font.render("B", True, BLACK)
                        text_rect = text.get_rect(center=cell_rect.center)
                        window.blit(text, text_rect)
                else:
                    if not self.board[row][col].hidden:
                        tmp = "#E5AA70" if (row+col) % 2 == 0 else "#C19A6B"
                        pygame.draw.rect(window, tmp, cell_rect)
                        font = pygame.font.SysFont(None, CELL_SIZE//2)
                        t = self.board[row][col].value
                        text = font.render(str(t), True, COLOR_NUMS.get(self.board[row][col].value))
                        text_rect = text.get_rect(center=cell_rect.center)
                        window.blit(text, text_rect)
                    else:
                        pygame.draw.rect(window, color, cell_rect)
        pygame.display.update()

    def get_clicked_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        for row in range(ROWS):
            for col in range(COLS):
                cell_x = col * (CELL_SIZE + MARGIN) + MARGIN
                cell_y = row * (CELL_SIZE + MARGIN) + MARGIN
                cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                if cell_rect.collidepoint(mouse_x, mouse_y):
                    return row, col
        return None

    def make_break(self, row, col):
        for i in range(max(0, row-1), min(ROWS, row+2)):
            for j in range(max(0, col-1), min(COLS, col+2)):
                if isinstance(self.board[i][j].value, int) and self.board[i][j].value == 0 and self.board[i][j].hidden:
                    self.board[i][j].hidden = False
                    self.make_break(i, j)
                elif isinstance(self.board[i][j].value, int) and self.board[i][j].hidden:
                    self.board[i][j].hidden = False

    def display_game_over(self, window):
        font = pygame.font.SysFont(None, 64)
        text = font.render("YOU LOST!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        window.blit(text, text_rect)
        pygame.display.update()

    def display_win(self, window):
        font = pygame.font.SysFont(None, 64)
        text = font.render("YOU WIN!", True, GREEN1)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        window.blit(text, text_rect)
        pygame.display.update()


    def display_board_in_terminal(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j],end=" ")
            print()

    def check_win(self):
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.board[row][col].value, int) and self.board[row][col].hidden:
                    return False
        return True
    
    def left_click(self, mouse_pos):
        clicked_cell = self.get_clicked_cell(mouse_pos)
        if clicked_cell:
            row, col = clicked_cell
            if self.flags[row][col]: return
            self.board[row][col].hidden = False
            #print(f"Left-clicked cell: row={row}, col={col}")
            if self.board[row][col].value == "X":
                self.board[row][col].hidden = False
                self.gameover = True
            if self.canBreak:
                self.make_break(row,col)
                self.canBreak = False

    def right_click(self, mouse_pos):
        clicked_cell = self.get_clicked_cell(mouse_pos)
        if clicked_cell:
            row, col = clicked_cell
            self.flags[row][col] = not self.flags[row][col]
            print(f"Right-clicked cell: row={row}, col={col}")

    def display_menu(self, window):
        # Set font and font size
        font = pygame.font.SysFont(None, 50)
        new_game_text = font.render("Play", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        new_game_pos = ((WIDTH - new_game_text.get_width()) / 2, (HEIGHT - new_game_text.get_height()) / 2 - 50)
        quit_pos = ((WIDTH - quit_text.get_width()) / 2, (HEIGHT - quit_text.get_height()) / 2 + 20)
        mouse_pos = pygame.mouse.get_pos()

        new_game_rect = pygame.Rect((WIDTH - 100) / 2, (HEIGHT - 100) / 2 - 50, 200, 50)
        if new_game_rect.collidepoint(mouse_pos):
            new_game_text = font.render("Play", True, (255, 0, 0))  # Change the color to red

        # Check if the mouse is hovering over the "Quit" option
        quit_rect = pygame.Rect((WIDTH - 100) / 2, (HEIGHT - 100) / 2 + 50, 200, 50)
        if quit_rect.collidepoint(mouse_pos):
            quit_text = font.render("Quit", True, (255, 0, 0))  # Change the color to red
        
        # Draw menu options
        window.fill("#E5AA70")
        window.blit(new_game_text, new_game_pos)
        window.blit(quit_text, quit_pos)

        # Update display
        pygame.display.update()

    def check_menu_selection(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # Check if "New Game" option was selected
                new_game_rect = pygame.Rect((WIDTH - 100) / 2, (HEIGHT - 100) / 2 - 50, 200, 50)
                if new_game_rect.collidepoint(mouse_pos):
                    return "new_game"
                # Check if "Quit" option was selected
                quit_rect = pygame.Rect((WIDTH - 100) / 2, (HEIGHT - 100) / 2 + 50, 200, 50)
                if quit_rect.collidepoint(mouse_pos):
                    return "quit"
        return None

    def restart_game(self):
        self.board = [[Tile(0, True) for _ in range(COLS)] for _ in range(ROWS)]
        self.flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.canBreak = True
        self.gameover = False
        self.set_board()

    def run(self):
        running = True
        menu = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        self.left_click(mouse_pos)
                    elif event.button == 3:
                        mouse_pos = pygame.mouse.get_pos()
                        self.right_click(mouse_pos)
            if menu:
                self.display_menu(window)
                #Check for menu option selection
                option = self.check_menu_selection()
                if option == "new_game":
                    menu = False
                    self.restart_game()
                elif option == "quit":
                    running = False
            
            else:
                if self.check_win():
                    self.draw_board(window)
                    self.display_win(window)
                    pygame.time.delay(3000)
                    menu=True
                if self.gameover:
                    self.draw_board(window)
                    self.display_game_over(window)
                    pygame.time.delay(3000)
                    menu=True
                else:
                    self.draw_board(window)
        pygame.quit()


if __name__ == "__main__":
    game = Minesweeper()
    game.run()
    



   
