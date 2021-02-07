import numpy as np
import pygame
import sys
import random
import math

pygame.init()

class Flappybird:
    def __init__(self):
        self.FPS = 30
        self.screen = pygame.display.set_mode((780,780))
        self.ROOT = [((290,300),(590,600))]
        self.WATER = []
        self.joined_WATER = []

        self.GRAY  = (180,180,180)
        self.WHITE = (255,255,255)
        self.BLUE  = (0, 0, 255)
        self.RED   = (255,0,0)

        pygame.display.set_caption("ROOT_GENETIC_ALGORITHM")
        #pygame.display.set_icon(self.icon)
    def restart(self):
        pass
    def get_point(self):
        if self.ROOT[0][0][0] == self.ROOT[0][1][0] or self.ROOT[0][0][1] == self.ROOT[0][1][1]:
            print("기울기 0")
        else:
            slope = (self.ROOT[0][1][1] - self.ROOT[0][0][1]) / (self.ROOT[0][1][0] - self.ROOT[0][0][0])
            #기울기 구하기 (y2-y1 / x2-x1)
        a = slope
        b = -1
        c = -1 * slope * self.ROOT[0][0][0] + self.ROOT[0][0][1]

        dump = set(self.joined_WATER)
        self.joined_WATER = list(dump)
        #중복제거

        for water in self.WATER:
            if abs(a * water[0] + b * water[1] + c)/(math.sqrt(math.pow(a, 2) + math.pow(b, 2))) <= 50 and (
                    water[0] >= self.ROOT[0][0][0] - 50 and water[0] <= self.ROOT[0][1][0] + 50 and water[1] >= self.ROOT[0][0][1] - 50 and water[1] <= self.ROOT[0][1][1] + 50):
                self.joined_WATER.append(water)
        print(len(self.joined_WATER), len(self.WATER))
    def set_water_position(self):
        for i in range(500):
            self.WATER.append((random.randint(0, 780), random.randint(0, 780)))
    def create_water(self):
        for water in self.WATER:
            pygame.draw.circle(self.screen,self.BLUE,(water[0],water[1]),2)
        for water in self.joined_WATER:
            pygame.draw.circle(self.screen, self.RED, (water[0], water[1]), 2)
    def create_root(self):
        pygame.draw.line(self.screen, self.GRAY, self.ROOT[0][0],self.ROOT[0][1], 5)
    def create_background(self):
        self.screen.fill(self.WHITE)
    def show(self):
        self.create_background()
        #self.set_water_position()
        self.get_point()
        self.create_water()
        self.create_root()
    def main(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.set_water_position()

            Flappybird.show(self)
            pygame.display.flip()

if __name__ == "__main__":
    Flappybird().main()
