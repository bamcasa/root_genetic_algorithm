import numpy as np
import pygame
import sys
import random
import math
import copy
import time
import os

pygame.init()


class ROOT:
    def __init__(self):
        if not os.path.exists("LOG"): #LOG 폴더 생성
            print("LOG 폴더 생성")
            os.makedirs("LOG")


        self.tm = time.localtime(time.time()) #LOG작성을 위한 현재 시간을 얻어냄
        self.number = 0 #유전자의 번호값

        self.chromos = np.zeros((10, 20, 2)) #z10 y20 x2 사이즈의 3차원 배열
        self.new_chromos = copy.deepcopy(self.chromos)
        self.mutation = 0.01  # 돌연변이 생성률
        self.parent_cromo_index = [0, 0] #부모가 되는 유전자의 수(우수한 유전자)
        self.generation = 0 #세대

        self.FPS = 30
        self.screen = pygame.display.set_mode((780, 780)) #780 * 780의 창크기
        self.ROOT = [((390, 0), (390, 20))]
        self.ROOT_NUMBER = [0]
        self.ROOT_ANGLE = [0]
        self.WATER = []
        self.joined_WATER = []

        self.pos = 0 #마우스의 좌표
        self.area = 50 #뿌리의 범위
        self.minus_ratio = 0.05

        self.clicked = False

        #색깔
        self.GRAY = (180, 180, 180)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)

        #폰트
        self.font = pygame.font.SysFont("arial", 20, True, False)

        #pygame 창 이름
        pygame.display.set_caption("ROOT_GENETIC_ALGORITHM")
        # pygame.display.set_icon(self.icon)

        #뿌리의 색깔
        self.root_color = self.GREEN

        self.create_1_generation()

        for __ in range(5):
            self.set_water_position()

    def reset(self):
        #뿌리의 초기값으로 초기화함
        self.ROOT = [((390, 0), (390, 20))]
        self.ROOT_NUMBER = [0]
        self.ROOT_ANGLE = [0]
        self.joined_WATER = []

    def write_log(self, text):
        """
        실행한 시간을 이름으로 한 텍스트 파일을 함
        세대별 유전자를 기록함
        """
        with open(
                f"LOG/{self.tm.tm_mon}월 {self.tm.tm_mday}일 {self.tm.tm_hour}시 {self.tm.tm_min}분 {self.tm.tm_sec}초.txt",
                "a") as f:
            f.write(f"GENE : {self.generation}")
            f.write(str(text))
            f.write("\n")

    def chromos_to_root(self):
        """
        유전자를 뿌리로 만듦
        유전자에 적힌 angle값과 distance값을 create_new_root함수에 넣어
        뿌리를 생성함
        """
        self.reset()
        #print(self.number)
        for i in range(int(len(self.chromos[0])/10)):
            self.aaa = i
            for j in range(10):
                print(j + i * 10)
                self.create_new_root(self.chromos[self.number][j + i * 10][0], self.chromos[self.number][j + i * 10][1])
            print(self.ROOT_NUMBER)
            print(self.ROOT_ANGLE)
            self.ROOT_NUMBER = [0]
            self.ROOT_ANGLE = [0]

        print(f"{self.number} : {self.ROOT}")
 #       print(self.ROOT_NUMBER)
#        print(self.ROOT_ANGLE)

        #self.chromos[i][j][0]  # angle
        #self.chromos[i][j][1]  # distance

    def create_1_generation(self):
        """
        유전자의 초기값을 넣음
        angle값은 50 ~ 150까지의 난수
        distance값은 80 ~ 150까지의 난수
        """
        for i in range(len(self.chromos)):
            for j in range(len(self.chromos[0])):
                for __ in range(len(self.chromos[0][0])):
                    self.chromos[i][j][0] = random.randint(50, 150)  # angle 값
                    self.chromos[i][j][1] = random.randint(80, 150)  # distance 값
        # pprint.pprint(chromos)
        self.generation += 1
        self.write_log(self.chromos)

    def evalution(self, chromos):
        """
        각 유전자의 점수를 얻음
        입력받은 유전자를 get_point2함수에 넣어
        나온 함숫값을 유전자의 점수로 함
        그리고 유전자의 점수를 반환함
        """
        evalution_value = np.zeros((len(chromos)))
        #print(chromos[1][1])
        for i in range(len(evalution_value)):
            m_sum = self.get_point2(i)
            #print(m_sum)
            evalution_value[i] = m_sum

        return evalution_value

    def chromos_crossover(self, chromos):
        """
        parent_cromo_index 즉 가장 우수한 유전자의 값을
        서로 교배하면서 새로운 유전자를 만든다.
        그리고 self.mutation(돌연변이확률)의 값으로
        돌연변이를 생성하기도 한다.
        """
        for i in range(len(chromos)):
            for j in range(len(chromos[0])):
                random1 = random.randint(0, 1)
                for k in range(len(chromos[0][0])):
                    if random.random() < self.mutation:
                        self.new_chromos[i][j][0] = random.randint(50, 125)
                        self.new_chromos[i][j][1] = random.randint(80, 120)
                        # 돌연변이 생성
                    else:
                        self.new_chromos[i][j][k] = chromos[self.parent_cromo_index[random1]][j][k]

        self.chromos = copy.deepcopy(self.new_chromos)

    def genetic_algorithm(self):
        evalution_value = self.evalution(self.chromos)
        argsorted_value = np.argsort(evalution_value)[::-1]
        #print("argsort : ",argsorted_value)
        for i in range(2):
            self.parent_cromo_index[i] = argsorted_value[i]

        self.chromos_crossover(self.chromos)

        #print("=============================")
        #print(self.generation, "Gen :", self.chromos)
        #print('evalution value :', evalution_value)
        #print('selected parent :', self.parent_cromo_index)
        self.write_log(self.chromos)
        self.generation += 1

    def get_point2(self, i):
        """
        입력받은 유전자의 값으로 뿌리를 생성한 후
        get_point함수로 뿌리로 인해 얻은 점수의 값을 반환한다.
        """
        self.reset()
        for i in range(int(len(self.chromos[0]) / 10)):
            self.aaa = i
            for j in range(10):
                self.create_new_root(self.chromos[self.number][j + i * 10][0], self.chromos[self.number][j + i * 10][1])
            self.ROOT_NUMBER = [0]
            self.ROOT_ANGLE = [0]
        minus_point = 0
        for j in range(len(self.chromos[0])):
            minus_point += self.chromos[i][j][1]
        #print("minus_point : ",minus_point)


        return self.get_point() - minus_point * self.minus_ratio

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
                #ROOT의 x좌표 둘중에서 어느것이 작고 큰 것인지 구별
                if self.ROOT[i][0][0] >= self.ROOT[i][1][0]:
                    min1 = self.ROOT[i][1][0]
                    max1 = self.ROOT[i][0][0]
                else:
                    min1 = self.ROOT[i][0][0]
                    max1 = self.ROOT[i][1][0]

                # ROOT의 y좌표 둘중에서 어느것이 작고 큰 것인지 구별
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
                    """
                    직선과 점사이의 거리가 self.area 값보다 작고 
                    water의 x좌표 값이 ROOT x좌표 둘중에서 작은 값보다 크고 water의 x좌표가 ROOT x좌표 둘중에서 큰 값보다 작고
                    water의 y좌표 값이 ROOT y좌표 둘중에서 작은 값보다 크고 water의 y좌표가 ROOT y좌표 둘중에서 큰 값보다 작은 것
                    """
                    self.joined_WATER.append(water)
        return len(self.joined_WATER)
        # print(len(self.joined_WATER), len(self.WATER))

    def set_water_position(self):
        #랜덤값 좌표에 물을 놓음
        for i in range(500):
            self.WATER.append((random.randint(0, 780), random.randint(600, 780)))

    def get_coord_ad(self, angle, distance):
        # https://cafe.naver.com/mcbugi.cafe?iframe_url=/ArticleRead.nhn%3Farticleid=27916&social=1
        # 이분의 코드를 참고하여 만들었음
        point = [0, 0]
        angle = math.pi * angle / 180  # 라디안으로 변환
        point[0] = int(distance * math.cos(angle))
        point[1] = int(distance * math.sin(angle))
        return point

    """def create_random_root(self):
        #랜덤한 각도와 거리로 새로운 ROOT좌표를 얻음
        angle = random.randint(50, 125)
        distance = random.randint(80, 120)
        point = self.get_coord_ad(angle, distance) #새로운 ROOT좌표를 얻음
        number = self.ROOT_NUMBER[-1]
        self.ROOT.append(((self.ROOT[number][1][0], self.ROOT[number][1][1]),
                          (self.ROOT[number][0][0] + point[0], self.ROOT[number][0][1] + point[1])))
        number += 1
        self.ROOT_ANGLE.append(angle)
        self.ROOT_NUMBER.append(number)
"""
    def create_new_root(self, angle, distance):
        #각도와 거리로 새로운 ROOT좌표를 얻음
        point = self.get_coord_ad(angle, distance) #새로운 ROOT좌표를 얻음
        number = self.ROOT_NUMBER[-1]
        self.ROOT.append(((self.ROOT[number][1][0]           , self.ROOT[number][1][1]),
                          (self.ROOT[number][0][0] + point[0], self.ROOT[number][0][1] + point[1])))
        number += 1
        self.ROOT_ANGLE.append(angle)
        self.ROOT_NUMBER.append(number)

    """def click_create_root(self, pos):
        
        첫번째 클릭한 점과 두번째 클릭한 점을
        각각 ROOT좌표로 정한다.
        
        if self.clicked:  # 두번쨰 클릭 (clicked == TRUE)
            print(self.pos, pos)
            self.ROOT.append((self.pos, pos))
            self.clicked = False
            self.pos = 0
        else:  # 첫번째 클릭 (clicked == FALSE)
            self.clicked = True
            self.pos = pos
    """
    def show_gene(self):
        pygame.draw.rect(self.screen, self.WHITE, [0, 0, 170, 50]) #텍스트뒤에 하얀색 배경 표시
        self.screen.blit(self.font.render(f"GENE : {self.generation}  number : {self.number}", True, self.BLACK), (0, 0)) #세대와 number 출력
        self.screen.blit(self.font.render(f"POINT : {len(self.joined_WATER)}", True, self.BLACK), (0, 20)) #유전자가 얻은 포인트의 수

    def show_water(self):
        for water in self.WATER:
            pygame.draw.circle(self.screen, self.BLUE, (water[0], water[1]), 2) #뿌리와 인접하지 않은 물은 파란색으로 표시
        for water in self.joined_WATER:
            pygame.draw.circle(self.screen, self.RED, (water[0], water[1]), 2) #뿌리와 인접한 물은 빨간색으로 표시

    def show_root(self):
        self.root_color = self.GREEN
        # print("NUMBER", self.ROOT_NUMBER, len(self.ROOT_NUMBER))
        # print("ANGLE", self.ROOT_ANGLE, len(self.ROOT_ANGLE))
        for i in range(len(self.ROOT)):
            if i >= 10:
                self.root_color = self.BLUE
            pygame.draw.line(self.screen, self.root_color, self.ROOT[i][0], self.ROOT[i][1], 10) #ROOT의 두 좌표를 잇는 직선을 생성

    def show_background(self):
        self.screen.fill(self.WHITE)
        #하얀색으로 배경을 채움

    def show(self):
        self.show_background()
        # self.set_water_position()
        self.get_point()
        self.show_water()
        self.show_root()
        self.show_gene()

    def main(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #나가기
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: #키보드를 눌렀을 때
                    for i in range(1):
                        self.genetic_algorithm()
                    #self.set_water_position()
                if event.type == pygame.MOUSEBUTTONDOWN: #마우스를 눌렀을때
                    pos = pygame.mouse.get_pos()
                    # self.click_create_root(pos)
                    # self.genetic_algorithm()
                    self.chromos_to_root()
                    self.number += 1
                    if self.number == 10: #유전자의 끝까지 나왔을때 다시 처음으로 돌아감
                        self.number = 0

            ROOT.show(self)
            pygame.display.flip()


if __name__ == "__main__":
    ROOT().main()
