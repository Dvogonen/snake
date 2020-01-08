import pygame

pygame.init()
sqr_positions = (41, 31)
sqr_size = 12
win = pygame.display.set_mode((sqr_positions[0] * sqr_size, sqr_positions[1] * sqr_size))
pygame.display.set_caption("The Snake")
squish_sound = pygame.mixer.Sound('squish.wav')
count_sound = pygame.mixer.Sound('count_in.wav')


class Snake:
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)
    stopped = (0, 0)

    def __init__(self, win_param):
        self.body = [(sqr_positions[0] // 2, sqr_positions[1] // 2)]
        self.toward = self.stopped
        self.window = win_param
        self.hiscore = 1

    def reset_window(self):
        pygame.display.update()
        pygame.time.delay(300)
        self.window.fill(0)
        pygame.display.update()
        pygame.time.delay(100)
        pygame.draw.rect(self.window, (75, 75, 170), (0, 0, sqr_positions[0] * sqr_size, sqr_positions[1] * sqr_size))
        pygame.display.update()
        pygame.time.delay(100)
        self.window.fill(0)
        pygame.display.update()

    def reset(self):
        if len(self.body) > self.hiscore:
            self.hiscore = len(self.body)
        self.body = [(sqr_positions[0] // 2, sqr_positions[1] // 2)]
        self.toward = self.stopped
        pygame.display.set_caption("The Snake - Hiscore: " + str(self.hiscore))
        self.reset_window()

    @staticmethod
    def frame_hit(pos):
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[0] >= sqr_positions[0] or pos[1] > sqr_positions[1]:
            return True
        return False

    def draw_cell(self, pos_x, pos_y, color, bkr):
        pygame.draw.rect(self.window, bkr, (pos_x * sqr_size, pos_y * sqr_size, sqr_size, sqr_size))
        pygame.draw.rect(self.window, color, (pos_x * sqr_size + 1, pos_y * sqr_size + 1, sqr_size - 2, sqr_size - 2))

    def draw(self):
        if len(self.body) > 0:
            self.draw_cell(self.body[-1][0], self.body[-1][1], (255, 100, 0), (170, 170, 170))
        if len(self.body) > 1:
            self.draw_cell(self.body[-2][0], self.body[-2][1], (0, 100, 100), (150, 150, 150))

    def cut_tail(self):
        if len(snake.body) > 1:
            self.draw_cell(self.body[0][0], self.body[0][1], (0, 0, 0), (0, 0, 0))
            snake.body.pop(0)


# globals
display_counter = 0
run = True
snake = Snake(win)

while run:
    display_counter += 1
    snake.draw()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # parse keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not snake.toward == snake.right:
        snake.toward = snake.left
    if keys[pygame.K_RIGHT] and not snake.toward == snake.left:
        snake.toward = snake.right
    if keys[pygame.K_UP] and not snake.toward == snake.down:
        snake.toward = snake.up
    if keys[pygame.K_DOWN] and not snake.toward == snake.up:
        snake.toward = snake.down
    if keys[pygame.K_ESCAPE]:
        run = False

    # calc head and tail
    if snake.toward == snake.stopped:
        display_counter = 0
    else:
        if display_counter % 10 == 0:
            head = (snake.body[-1][0] + snake.toward[0], snake.body[-1][1] + snake.toward[1])
            if head in snake.body or snake.frame_hit(head):
                squish_sound.play()
                pygame.time.delay(1000)
                snake.reset()
            else:
                snake.body.append(head)

        if display_counter % 15 == 0:
            snake.cut_tail()

        pygame.time.delay(10)

pygame.quit()
