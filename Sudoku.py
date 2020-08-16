import pygame
import copy
pygame.init()



class Board:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self,width,height,cols,rows,win):
        self.win = win
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.solved = None
        self.solve()
        self.model = None

    def update_cubes(self):
        for j in range (self.cols):
            for i in range(self.rows):
                self.cubes[i][j].value = self.board[i][j]

        # [[self.cubes[i][j].value = self.board[i][j] for j in range(self.cols)] for i in range(self.rows)]

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.cols * gap
        y = self.rows * gap

        for i in range(10):
            thick = 3 if i % 3 == 0 else 1
            pygame.draw.line(win, (0,0,0), (0, (i*gap)+2), (self.width, i*gap+2), thick)
        for i in range(9):
            thick = 3 if i % 3 == 0 else 1
            pygame.draw.line(win, (0,0,0), (i*gap,2), (i*gap,self.height-gap+2), thick)

        for i in range(9):
            for j in range(9):
                self.cubes[i][j].draw(self.win)

    def select(self,y ,x):
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].selected = False
        self.cubes[y][x].selected = True

    def parse(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def possible(self,y,x,n):
        for i in range(9):
            if self.board[y][i]==n :
                return False
        for i in range(9):
            if self.board[i][x]==n :
                return False

        x0 = (x//3)*3
        y0 = (y//3)*3

        for i in range(0,3):
            for j in range(0,3):
                if self.board[y0+i][x0+j] == n:
                    return False

        return True

    def solve(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    for n in range(1,10):
                        if self.possible(y, x, n):
                            self.board[y][x] = n
                            self.solve()
                            self.board[y][x] = 0
                    return
        self.solved = copy.deepcopy(self.board)

    def gui_solve(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    self.board[y][x] = copy.deepcopy(self.solved[y][x])
                    return
        self.update_cubes()

class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.width = width
        self.height= height
        self.col = col
        self.row = row
        self.selected = False

    def draw(self,win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value!=0:
            text = fnt.render(str(self.value), 1, (0,0,0))
            win.blit(text, (x+(gap/2)-7, y+(gap/2)-7))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x+1,y+2, gap ,gap), 3)


def time(second):
    secs = second%60
    minutes = second//60

    return str(minutes)+":"+str(secs)

def redraw_board(board, seconds, win):
    board.update_cubes()
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 35)
    text = fnt.render("Time: " + time(seconds), 1, (0, 0, 0))
    win.blit(text, (400, 560))
    board.draw(win)

def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Board(540, 600, 9, 9, win)
    start_ticks = pygame.time.get_ticks()

    run = True
    while run:
        seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.gui_solve()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            parsed_pos = board.parse(pos)
            board.select(parsed_pos[0], parsed_pos[1])

        redraw_board(board, seconds, win)
        pygame.display.update()

main()
pygame.quit()