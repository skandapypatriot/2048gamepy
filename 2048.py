import pygame
import random

pygame.init()

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
fps = 50
font = pygame.font.Font("freesansbold.ttf", 24)
colours = {0: (204, 192, 179),
           2: (238, 228, 218),
           4: (237, 224, 200),
           8: (247, 177, 121),
           16: (245, 149, 99),
           32: (246, 94, 59),
           64: (246, 94, 59),
           128: (237, 207, 114),
           256: (237, 204, 97),
           512: (237, 200, 80),
           1024: (237, 197, 63),
           2048: (237, 194, 46),
           "light text": (249, 246, 242),
           "dark text": (119, 110, 101),
           "other": (0, 0, 0),
           "bg": (187, 173, 160)
           }

board_values = [[0 for _ in range(4)] for _ in range(4)]
run = True
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
try:
    file = open('high_score2.txt', "r")
    init_high = int(file.readline())
    high_score = init_high
    is_high_score_beaten = False
    file.close()
except:
    high_score = 0
    init_high = 0
full = False


def draw_over():
    pygame.draw.rect(screen, "black", [50, 50, 300, 100], 0, 1)
    game_over_text1 = font.render(f"Game over!", True, "white")
    game_over_text2 = font.render(f"Press Enter To Restart", True, "white")
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (75, 105))


def draw_board():
    pygame.draw.rect(screen, colours["bg"], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f"Score: {score}", True, "black")
    high_score_text = font.render(f"High Score: {high_score}", True, "black")
    screen.blit(score_text, (10, 410), )
    screen.blit(high_score_text, (10, 450), )


def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_colour = colours['light text']
            else:
                value_colour = colours["dark text"]
            if value <= 2048:
                colour = colours[value]
            else:
                colour = colours["other"]
            pygame.draw.rect(screen, colour, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_colour)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)


def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == "UP":
        for i in range(4):
            for j in range(4):
                swift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            swift += 1
                    if swift > 0:
                        board[i - swift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - swift - 1][j] == board[i - swift][j] and not merged[i - swift - 1][j] \
                            and not merged[i - swift][j]:
                        board[i - swift - 1][j] *= 2
                        score += board[i - swift - 1][j]
                        board[i - swift][j] = 0
                        merged[i - swift - 1][j] = True
    elif direc == "DOWN":
        for i in range(3):
            for j in range(4):
                swift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        swift += 1
                if swift > 0:
                    board[2 - i + swift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + swift <= 3:
                    if board[2 - i + swift][j] == board[3 - i + swift][j] and not merged[2 - i + swift][j] \
                            and not merged[3 - i + swift][j]:
                        board[3 - i + swift][j] *= 2
                        score += board[3 - i + swift][j]
                        board[2 - i + swift][j] = 0
                        merged[3 - i + swift][j] = True
    elif direc == "RIGHT":
        for i in range(4):
            for j in range(3):
                swift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        swift += 1
                if swift > 0:
                    board[i][3 - j + swift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + swift <= 3:
                    if board[i][4 - j + swift] == board[i][3 - j + swift] and not merged[i][4 - j + swift] \
                            and not merged[i][3 - j + swift]:
                        board[i][4 - j + swift] *= 2
                        score += board[i][4 - j + swift]
                        board[i][3 - j + swift] = 0
                        merged[i][4 - j + swift] = True

    elif direc == "LEFT":
        for i in range(4):
            for j in range(4):
                swift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        swift += 1
                if swift > 0:
                    board[i][j - swift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - swift] == board[i][j - swift - 1] and not merged[i][j - swift] \
                        and not merged[i][j - swift - 1]:
                    board[i][j - swift - 1] *= 2
                    score += board[i][j - swift - 1]
                    board[i][j - swift] = 0
                    merged[i][j - swift - 1] = True
    return board_values


def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return full, board


while run:
    timer.tick(fps)
    screen.fill("gray")
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        game_over, board_values = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if is_high_score_beaten:
            try: 
                high_score = score
                open(".\high_score2.txt", "w").write(str(high_score))
            except:
                high_score = score

            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False


    if score > high_score:
        high_score = score
        is_high_score_beaten = True
    try:
        open(".\high_score2.txt", "w").write(str(high_score))
    except:
        pass
    pygame.display.flip()


pygame.quit()
