import pygame
import sys
from random import randint
import Scores
import WinColor

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SQ_WIDTH = int(WINDOW_WIDTH * 0.025)
SQ_HEIGHT = int(WINDOW_HEIGHT * 0.025)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Score:

    def __init__(self, score):
        self.hs_file = "highscore.txt"
        file = open("highscore.txt", "r+")
        self.high_score = int(file.readline())
        file.close()

        self.font = pygame.font.SysFont('brushscript', int(0.04 * WINDOW_HEIGHT))
        self.text = self.font.render(f"Score: {score}", True, WHITE, BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.center = (int(0.075 * WINDOW_WIDTH), SQ_HEIGHT)

        self.high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE, BLACK)
        self.high_score_text_rect = self.high_score_text.get_rect()
        self.high_score_text_rect.center = (WINDOW_WIDTH // 2, SQ_HEIGHT)

    def update_score(self, score, b_color):
        self.text = self.font.render(f"Score: {score}", True, WHITE, BLACK)
        if score > self.high_score:
            file = open(self.hs_file, "w")
            file.write(str(score))
            self.high_score = score
        self.high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE, BLACK)

class Snake:

    def draw_snake(self, win, x, y):
        pygame.draw.rect(win, WHITE, (x[0], y[0], SQ_WIDTH, SQ_HEIGHT))
        for i in range(1, len(x)):
            pygame.draw.rect(win, WHITE, (x[i], y[i], SQ_WIDTH, SQ_HEIGHT))
        for i in range(len(x) - 1, 0, -1):
            x[i] = x[i - 1]
            y[i] = y[i - 1]


class Apple:
    def __init__(self):
        self.x = randint(SQ_WIDTH, WINDOW_WIDTH - SQ_WIDTH)
        self.y = randint(SQ_HEIGHT, WINDOW_HEIGHT - SQ_HEIGHT)

    def draw_apple(self, win):
        pygame.draw.rect(win, RED, (self.x, self.y, SQ_WIDTH, SQ_HEIGHT))


class Game:
    points = 0

    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.max_fps = 15

        self.clock = pygame.time.Clock()

        #self.high_scores = Scores.HighScores()

        self.win_color = WinColor.WinColor()
        self.x = [WINDOW_WIDTH // 2]
        self.y = [WINDOW_HEIGHT // 2]
        self.vert = 0
        self.horz = 0
        self.snake = Snake()
        self.apple = Apple()
        self.points = 0

        # begin main game loop
        self.main()

    def is_out_bounds(self):
        if self.x[0] <= 0 or self.x[0] >= WINDOW_WIDTH or self.y[0] <= 0 or self.y[0] >= WINDOW_HEIGHT:
            return True

    def is_body_collision(self):
        for i in range(len(self.x) - 1, 1, -1):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                return True

    def is_apple_collision(self):
        if self.apple.x - SQ_WIDTH // 2 <= self.x[0] <= self.apple.x + SQ_WIDTH // 2:
            if self.apple.y - SQ_HEIGHT // 2 <= self.y[0] <= self.apple.y + SQ_HEIGHT / 2:
                return True

    def extend_body(self):
        for i in range(len(self.x), len(self.x) + 4):
            self.x.append(self.x[i - 1])
            self.y.append(self.y[i - 1])

    def change_direction(self, key):
        if key == pygame.K_UP:
            # the up arrow key was pressed
            self.vert = -SQ_HEIGHT
            self.horz = 0
        elif key == pygame.K_DOWN:
            self.vert = SQ_HEIGHT
            self.horz = 0
        elif key == pygame.K_LEFT:
            self.vert = 0
            self.horz = -SQ_WIDTH
        elif key == pygame.K_RIGHT:
            self.vert = 0
            self.horz = SQ_WIDTH
        elif key == pygame.K_SPACE:
            self.vert = 0
            self.horz = 0

    def generate_scores(self):
        h_scores = self.high_scores.get_scores()
        scores = [score[1] for score in h_scores]
        if len(scores) < 5:
            player = input("""Name: """)
            self.high_scores.add_score((player, self.points))
        elif scores[len(scores) - 1] < self.points:
            player = input("""Name: """)
            self.high_scores.add_score((player, self.points))
        h_scores = self.high_scores.get_scores()
        result = ""
        for i in range(0, len(h_scores)):
            result += str(h_scores[i]) + "\n"
        return result

    def game_over(self):
        # scores = self.generate_scores()
        # print(scores)
        while True:
            font = pygame.font.SysFont('impact', int(0.09 * WINDOW_HEIGHT))
            text = font.render("GAME OVER", True, WHITE, RED)
            text_rect = text.get_rect()
            text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

            score_font = pygame.font.SysFont('impact', int(0.04 * WINDOW_HEIGHT))
            score_text = score_font.render(f"Final Score: {self.points}", True, WHITE, RED)
            score_text_rect = score_text.get_rect()

            self.win.blit(text, text_rect)
            self.win.blit(score_text, score_text_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_SPACE:
                        Game()

    def main(self):

        score = Score(self.points)

        while True:
            if self.is_out_bounds() or self.is_body_collision():
                self.game_over()

            if self.is_apple_collision():
                self.extend_body()
                self.apple = Apple()
                self.points = self.points + 1
                self.win_color.random_color()
                score.update_score(self.points, self.win_color)

            # movement
            self.y[0] = self.y[0] + self.vert
            self.x[0] = self.x[0] + self.horz

            for event in pygame.event.get():
                # pygame.QUIT is the x in the corner of the window that allows you to close the window
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    self.change_direction(key)
            self.win.fill(self.win_color.get_color())

            # draw objects to screen
            self.apple.draw_apple(self.win)
            self.snake.draw_snake(self.win, self.x, self.y)
            self.win.blit(score.text, score.textRect)
            self.win.blit(score.high_score_text, score.high_score_text_rect)

            pygame.display.update()
            # gradually darken display
            self.win_color.dim_color()
            score.update_score(self.points, self.win_color)

            # tick, to tell the clock that one frame is complete
            self.clock.tick(self.max_fps)


if __name__ == "__main__":
    Game()
