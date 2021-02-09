#https://blex.me/@baealex/%ED%8C%8C%EC%9D%B4%EC%8D%ACpython-%EC%9C%A0%EC%A0%84-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EA%B8%B0%EB%B3%B8
#이분의 코드를 수정하여 만들었음
import random
import numpy
import copy

def evalution(chromos):
    evalution_value = [0 for __ in range(len(chromos))]

    dominant = 1

    for i in range(len(evalution_value)):
        m_sum = 0
        for j in range(10):
            if chromos[i][j] > dominant:
                m_sum += chromos[i][j] - dominant
            else:
                m_sum += dominant - chromos[i][j]
        evalution_value[i] = m_sum

    return evalution_value

if __name__ == '__main__':
    chromos = [[0 for __ in range(10)] for __ in range(10)] # 길이가 10인 리스트가 10개 생성 0으로 초기화된
    new_chromos = copy.deepcopy(chromos)

    mutation = 0.1 #돌연변이 생성률

    parent_cromo_index = [0, 0]
    generation = 0

    # 1 Generation
    for i in range(len(chromos)):
        for j in range(len(chromos[0])):
            chromos[i][j] = random.randint(0, 9)

    generation += 1

    while True:
        if generation > 1000:
            # Force stop
            break

        evalution_value = evalution(chromos)

        for i in range(2):
            parent_cromo_index[i] = numpy.argsort(evalution_value)[i]

        done = False
        for i in range(len(chromos)):
            if evalution_value[i] == 0:
                done = True
                break
        if done == True:
            break

        # 염색체 교차 및 돌연변이
        for i in range(len(chromos)):
            for j in range(len(chromos[0])):
                if random.random() < mutation:
                    new_chromos[i][j] = random.randint(0, 9) #돌연변이 생성
                else:
                    new_chromos[i][j] = chromos[parent_cromo_index[random.randint(0, 1)]][j]

        chromos = copy.deepcopy(new_chromos)

        print("=============================")
        print(generation, "Gen :", chromos)
        print('evalution value :', evalution_value)
        print('selected parent :', parent_cromo_index)
        #input(" ")

        generation += 1

    print("Done!!!")
