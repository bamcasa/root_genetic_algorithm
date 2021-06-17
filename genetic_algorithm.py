#https://blex.me/@baealex/%ED%8C%8C%EC%9D%B4%EC%8D%ACpython-%EC%9C%A0%EC%A0%84-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EA%B8%B0%EB%B3%B8
#이분의 코드를 수정하여 만들었음
import random
import numpy as np
import copy
import pprint
import time

tm = time.localtime(time.time())

def write_log(text,gen):

    with open(f"LOG/{tm.tm_mon}M {tm.tm_mday}D {tm.tm_hour}hour {tm.tm_min}min {tm.tm_sec}sec.txt", "a") as f:
        f.write(f"GENE : {gen}")
        f.write(str(text))
        f.write("\n")

def get_point(chromo):
    angle = chromo[0]
    distance = chromo[1]

    return angle + distance

def evalution(chromos):
    evalution_value = np.zeros((len(chromos),len(chromos[0])))

    for i in range(len(evalution_value)):
        for j in range(len(evalution_value[0])):
            m_sum = 0
            m_sum += get_point(chromos[i][j])
            evalution_value[i][j] = m_sum

    return evalution_value

if __name__ == '__main__':
    chromos = np.zeros((10,10,2)) # 10*10*2 z축 10개, y축 10개, x축 2개
    #pprint.pprint(chromos)
    new_chromos = copy.deepcopy(chromos)

    mutation = 0.01 #돌연변이 생성률

    parent_cromo_index = [[0, 0],
                          [0, 0]]
    generation = 0

    # 1 Generation
    for i in range(len(chromos)):
        for j in range(len(chromos[0])):
            for __ in range(len(chromos[0][0])):
                chromos[i][j][0] = random.randint(50, 125) #angle 값
                chromos[i][j][1] = random.randint(80, 120) #distance 값
    #pprint.pprint(chromos)
    generation += 1
    write_log(chromos,generation)

    while True:
        if generation > 1000:
            # Force stop
            break

        evalution_value = evalution(chromos)
        #print(evalution_value)

        reshaped = evalution_value.reshape(len(evalution_value) * len(evalution_value[0]))
        #print(reshaped)

        argsorted_reshaped = np.argsort(reshaped)
        #print(argsorted_reshaped)

        max_point = argsorted_reshaped[::-1][0]

        #print(max_point)

        y = max_point//len(evalution_value)
        x = max_point%len(evalution_value)

        #print(reshaped[max_point])

        #print(evalution_value[y][x])

        for i in range(2):
            parent_cromo_index[i][0] = y
            parent_cromo_index[i][1] = x

        done = False
        for i in range(len(chromos)):
            for j in range(len(chromos[0])):
                if evalution_value[i][j] >= 244:
                    done = True
                    break
        if done == True:
            break

        # 염색체 교차 및 돌연변이
        for i in range(len(chromos)):
            for j in range(len(chromos[0])):
                for k in range(len(chromos[0][0])):
                    if random.random() < mutation:
                        new_chromos[i][j][0] = random.randint(50, 125)
                        new_chromos[i][j][1] = random.randint(80, 120)
                        #돌연변이 생성
                    else:
                        random1 = random.randint(0, 1)
                        new_chromos[i][j][k] = chromos[parent_cromo_index[random1][0]][parent_cromo_index[random1][1]][k]

        chromos = copy.deepcopy(new_chromos)
        write_log(chromos,generation)

        print("=============================")
        print(generation, "Gen :", chromos)
        print('evalution value :', evalution_value)
        print('selected parent :', parent_cromo_index)
        #input(" ")

        generation += 1

    print("Done!!!")
