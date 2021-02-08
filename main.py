import numpy as np
import pygame
import sys
import random
import math

pygame.init()


class ROOT:
    def __init__(self):
        self.FPS = 30
        self.screen = pygame.display.set_mode((780, 780))
        self.ROOT = [((390, 0), (390, 20))]
        self.WATER = []
        self.joined_WATER = []
        self.pos = 0
        self.area = 50

        self.clicked = False

        self.GRAY = (180, 180, 180)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        pygame.display.set_caption("ROOT_GENETIC_ALGORITHM")
        # pygame.display.set_icon(self.icon)

    def restart(self):
        pass

    def get_point(self):
        for i in range(len(self.ROOT)):
            if self.ROOT[i][0][0] == self.ROOT[i][1][0]:  # y축과 평행한 직선
                a = 1
                b = 0
                c = -1 * self.ROOT[i][0][0]
            elif self.ROOT[i][0][1] == self.ROOT[i][1][1]:  # x축과 평행한 직선
                a = 0
                b = 1
                c = -1 * self.ROOT[i][0][1]
            else:
                slope = (self.ROOT[i][1][1] - self.ROOT[i][0][1]) / (self.ROOT[i][1][0] - self.ROOT[i][0][0])
                # 기울기 구하기 (y2-y1 / x2-x1)
                a = slope
                b = -1
                c = -1 * slope * self.ROOT[i][0][0] + self.ROOT[i][0][1]

            dump = set(self.joined_WATER)
            self.joined_WATER = list(dump)  # 중복제거

            dump = set(self.WATER)
            self.WATER = list(dump)  # 중복제거

            for water in self.WATER:
                if self.ROOT[i][0][0] >= self.ROOT[i][1][0]:
                    min1 = self.ROOT[i][1][0]
                    max1 = self.ROOT[i][0][0]
                else:
                    min1 = self.ROOT[i][0][0]
                    max1 = self.ROOT[i][1][0]

                if self.ROOT[i][0][1] >= self.ROOT[i][1][1]:
                    min2 = self.ROOT[i][1][1]
                    max2 = self.ROOT[i][0][1]
                else:
                    min2 = self.ROOT[i][0][1]
                    max2 = self.ROOT[i][1][1]

                if abs(a * water[0] + b * water[1] + c) / (
                math.sqrt(math.pow(a, 2) + math.pow(b, 2))) <= self.area and (
                        water[0] >= min1 - self.area and water[0] <= max1 + self.area and
                        water[1] >= min2 - self.area and water[1] <= max2 + self.area
                ):
                    self.joined_WATER.append(water)
        # print(len(self.joined_WATER), len(self.WATER))

    def set_water_position(self):
        for i in range(500):
            self.WATER.append((random.randint(0, 780), random.randint(0, 780)))

    def get_coord_ad(self,angle,distance):
        point = [0,0]
        angle = math.pi * angle / 180; #라디안으로 변환
        point[0] = distance * math.cos(angle);
        point[1] = distance * math.sin(angle);
        return point

    def create_new_root(self):
        angle = 45
        distance = 100 * math.pow(2,1/2)
        point = self.get_coord_ad(angle,distance)
        print(point)
        self.ROOT.append(((self.ROOT[0][1][0],self.ROOT[0][1][1]),(self.ROOT[0][0][0] + point[0],self.ROOT[0][0][1] + point[1])))

    def click_create_root(self, pos):
        if self.clicked:  # 두번쨰 클릭 (clicked == TRUE)
            print(self.pos, pos)
            self.ROOT.append((self.pos, pos))
            self.clicked = False
            self.pos = 0
        else:  # 첫번째 클릭 (clicked == FALSE)
            self.clicked = True
            self.pos = pos

    def show_water(self):
        for water in self.WATER:
            pygame.draw.circle(self.screen, self.BLUE, (water[0], water[1]), 2)
        for water in self.joined_WATER:
            pygame.draw.circle(self.screen, self.RED, (water[0], water[1]), 2)

    def show_root(self):
        for i in range(len(self.ROOT)):
            pygame.draw.line(self.screen, self.GREEN, self.ROOT[i][0], self.ROOT[i][1], 10)

    def show_background(self):
        self.screen.fill(self.WHITE)

    def show(self):
        self.show_background()
        # self.set_water_position()
        self.get_point()
        self.show_water()
        self.show_root()

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
                    self.create_new_root()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.click_create_root(pos)

            ROOT.show(self)
            pygame.display.flip()


if __name__ == "__main__":
    ROOT().main()
