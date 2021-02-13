import numpy as np
import pygame
import sys
import random
import math
import copy


pygame.init()


class ROOT:
    def __init__(self):
        self.chromos = np.zeros((10, 10, 2))
        self.new_chromos = copy.deepcopy(self.chromos)
        self.mutation = 0.01  # 돌연변이 생성률
        self.parent_cromo_index = [[0, 0],
                                   [0, 0]]
        self.generation = 0

        self.FPS = 30
        self.screen = pygame.display.set_mode((780, 780))
        self.ROOT = [((390, 0), (390, 20))]
        self.ROOT_NUMBER = [0]
        self.ROOT_ANGLE = [0]
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

        self.create_1_generation()

    def restart(self):
        pass

    def create_1_generation(self):
        for i in range(len(self.chromos)):
            for j in range(len(self.chromos[0])):
                for __ in range(len(self.chromos[0][0])):
                    self.chromos[i][j][0] = random.randint(50, 125)  # angle 값
                    self.chromos[i][j][1] = random.randint(80, 120)  # distance 값
        # pprint.pprint(chromos)
        self.generation += 1

    def evalution(self, chromos):
        evalution_value = np.zeros((len(chromos), len(chromos[0])))
        print(chromos[1][1])
        for i in range(len(evalution_value)):
            for j in range(len(evalution_value[0])):
                m_sum = 0
                m_sum += self.get_point2(chromos[i][j])
                evalution_value[i][j] = m_sum

        return evalution_value

    def chromos_crossover(self, chromos):
        for i in range(len(chromos)):
            for j in range(len(chromos[0])):
                for k in range(len(chromos[0][0])):
                    if random.random() < self.mutation:
                        self.new_chromos[i][j][0] = random.randint(50, 125)
                        self.new_chromos[i][j][1] = random.randint(80, 120)
                        #돌연변이 생성
                    else:
                        random1 = random.randint(0, 1)
                        self.new_chromos[i][j][k] = chromos[self.parent_cromo_index[random1][0]][self.parent_cromo_index[random1][1]][k]

        self.chromos = copy.deepcopy(self.new_chromos)

    def genetic_algorithm(self):
        evalution_value = self.evalution(self.chromos)
        reshaped = evalution_value.reshape(len(evalution_value) * len (evalution_value[0]))
        argsorted_reshaped = np.argsort(reshaped)
        max_point = argsorted_reshaped[::-1][0]

        y = max_point//len(evalution_value)
        x = max_point%len(evalution_value)

        for i in range(2):
            self.parent_cromo_index[i][0] = y
            self.parent_cromo_index[i][1] = x

        self.chromos_crossover(self.chromos)


        print("=============================")
        print(self.generation, "Gen :", self.chromos)
        print('evalution value :', evalution_value)
        print('selected parent :', self.parent_cromo_index)
        self.generation += 1

    def get_point2(self,chromo):
        angle = chromo[0]
        distance = chromo[1]

        return angle + distance

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

    def get_coord_ad(self, angle, distance):
        # https://cafe.naver.com/mcbugi.cafe?iframe_url=/ArticleRead.nhn%3Farticleid=27916&social=1
        # 이분의 코드를 참고하여 만들었음
        point = [0, 0]
        angle = math.pi * angle / 180  # 라디안으로 변환
        point[0] = distance * math.cos(angle)
        point[1] = distance * math.sin(angle)
        return point

    def create_new_root(self):
        angle = random.randint(50, 125)  # 45
        distance = random.randint(80, 120)  # 100 * math.pow(2,1/2)
        point = self.get_coord_ad(angle, distance)
        # print(point)
        number = self.ROOT_NUMBER[-1]
        self.ROOT.append(((self.ROOT[number][1][0], self.ROOT[number][1][1]),
                          (self.ROOT[number][0][0] + point[0], self.ROOT[number][0][1] + point[1])))
        number += 1
        self.ROOT_ANGLE.append(angle)
        self.ROOT_NUMBER.append(number)

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
        #print("NUMBER", self.ROOT_NUMBER, len(self.ROOT_NUMBER))
        #print("ANGLE", self.ROOT_ANGLE, len(self.ROOT_ANGLE))
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # self.click_create_root(pos)
                    self.genetic_algorithm()

                    self.create_new_root()

            ROOT.show(self)
            pygame.display.flip()


if __name__ == "__main__":
    ROOT().main()
