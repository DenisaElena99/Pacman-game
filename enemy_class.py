import pygame
import random
from settings import *
vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour() 
        self.direction = vec(1,0)
        self.personality = self.set_personality()


    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move():
            self.move() 

        self.grid_pos[0] = (self.pix_pos[0]-TOP_BUTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BUTTOM_BUFFER+self.app.cell_height//2) // self.app.cell_height + 1

        

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x),int(self.pix_pos.y)), self.radius)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BUTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y+TOP_BUTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
 
    def get_random_direction(self):
        while True:
            number = random.randint(-2,1)
            if number == -2:
                x_dir,y_dir = 1,0
            elif number == -1:
                x_dir,y_dir = 0,1
            elif number == 0:
                x_dir,y_dir = -1,0
            else:
                x_dir,y_dir = 0,-1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir,y_dir)

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BUTTOM_BUFFER//2+self.app.cell_width//2, (self.grid_pos.y*self.app.cell_height)+TOP_BUTTOM_BUFFER//2+self.app.cell_height//2)

    def set_colour(self):
        if self.number == 0:
            colour =  (43, 78, 203) 
        if self.number == 1:
            colour =  (19, 200, 27) 
        if self.number == 2:
            colour =  (189, 29, 29) 
        if self.number == 3:
            colour = (215, 159, 33)
        return colour

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        if self.number == 1:
            return "slow"
        if self.number == 2:
            return "random"
        if self.number == 3:
            return "scared"
        