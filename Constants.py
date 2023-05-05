WIDTH = 980
HEIGHT = 780
ROWS = 8*2
COLS = 10*2
MARGIN = 0
CELL_SIZE = (WIDTH - (COLS + 1) * MARGIN) // COLS
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN1 = "#90EE90"
GREEN2 = "#98FB98"
RED = "#ff5252"
RED2 = "#ff7b7b"
COLOR_NUMS = { 1: "Blue", 2: "yellow", 3: "red", 4: "purple", 5: BLACK, 0: GRAY, 6: BLACK, 7: BLACK, 8: BLACK }
MINE_PERCENTAGE = 20  # 20% of cells will contain mines