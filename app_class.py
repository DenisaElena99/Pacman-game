import pygame
import sys
import copy
from settings import *
from player_class import *


pygame.init()
vec = pygame.math.Vector2
logo_surface = pygame.display.set_mode((20, 20))

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.player = Player(self, PLAYER_START_POS)
        self.walls = []
        self.coins = []

        self.load()


    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# HELPER FUNCTIONS #
    def draw_text(self, words, screen, pos, size, colour, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2

        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH,
        MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
        #print(self.walls)

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))
        #for coins in self.coins:
         #   pygame.draw.rect(self.background, (167, 179, 34), (coin.x*self.cell_width,
          #                                                     coin.y*self.cell_height, self.cell_width, self.cell_height))




# INTRO FUNCTIONS #

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):

        self.screen.fill(BLACK)
        self.draw_text('HIGH SCORE', self.screen, [4, 0], START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text('PUSH SPACE BAR TO START', self.screen, [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, WHITE, START_FONT, True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2+100], START_TEXT_SIZE, MINT, START_FONT, True)
        self.draw_text('© 2020 BICICLETE.RO', self.screen, [WIDTH//2, HEIGHT//2+150], START_TEXT_SIZE, BLUE, START_FONT, True)
        pygame.display.set_caption('Pac-Bike')
        logo = pygame.image.load('logo.png')
        wlogo = logo.get_width()
        logo_surface.blit(logo, (WIDTH//2-wlogo//2, 85))
        pygame.display.update()

# PLAYING FUNCTIONS #

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BUTTOM_BUFFER//2, TOP_BUTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_grid()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [60,0], 18, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2 + 60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BUTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BUTTOM_BUFFER//2), 5)
