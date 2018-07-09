#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import pandas as pd
import numpy as np
import random
import copy
from EvaluateFunctions import calcFitness

DAY = None
requiredManNum = None
WORK = None
MAN = None

S = 0.4  # スケーリングファクター
Cr = 0.9  # 交差率
Pm = 0.01  # 突然変異率
NP = 50  # 個体数
MaxGen = 100000  # 最大世代数


def importGlobal(gl_DAY, gl_WORK, gl_requiredManNum, gl_MAN):
    global DAY, WORK, requiredManNum, MAN
    DAY = gl_DAY
    WORK = gl_WORK
    requiredManNum = gl_requiredManNum
    MAN = gl_MAN


class DE(object):
    '''
    Differential Evolution
    '''

    pop = None  # Populationクラスを格納するための変数
    curGen = 1  # 現在の世代数

    def __init__(self):
        print("DE initalize")
        pop = Population()
        print(pop)
        pop.generateMutantParent()


class Population(object):
    '''
    population of DE
    '''
    pop = []  # 個体Individualのリスト

    def __init__(self):
        print("population initialize")
        for i in range(NP):
            self.pop.append(Individual())
        print(self.pop)
        print("max_fitness=", max(self.pop, key=lambda x: x.fitness).fitness)
        print("min_fitness=", min(self.pop, key=lambda x: x.fitness).fitness)

    def generateMutantParent(self):  # 差分変異親個体vの生成
        print("generateDifferentialMutantParent")
        for ind in self.pop:
            parent_pool = copy.copy(self.pop)
            parent_pool.remove(ind)  # 対象親個体の除外
            parents = random.sample(parent_pool, 3)  # ランダムに異なる3個体選ぶ
            ind.generateMutantParent(parents)


class Individual(object):
    '''
    indivisual of DE
    '''
    gene = None #遺伝子には人を識別するためのインデックスが格納
    H1 = None
    H2 = None
    H3 = None
    fitness = None

    def __init__(self):
        print("inidivisual initialize")
        # 個体の生成
        gene = pd.Series()
        index = []
        for day in DAY:
            # day日の遺伝子を作成
            print(day)
            series = pd.Series(np.arange(len(MAN)))
            for work in WORK:
                num = requiredManNum[day][work]
                for n in range(num):
                    # index.append(day + "-" + work)
                    index.append((day, work))
            np.random.shuffle(series)  # ランダムに並び替え
            # gene = gene.append(series)
            gene = pd.concat([gene, series])
        index = pd.MultiIndex.from_tuples(index, names=['day', 'work'])
        gene.index = index
        self.gene = gene
        print("gene=",)
        print(self.gene)
        self.fitness, self.H1, self.H2, self.H3 = calcFitness(self.gene)
        print(self.fitness, self.H1)

    def generateMutantParent(self, parents):  # 差分変異親個体vの生成
        P1 = parents[0].gene
        P2 = parents[1].gene
        P3 = parents[2].gene
        print("P1,2,3")
        print(P1, P2, P3)
        mutantParent = P1 + S * (P2 - P3)
        # 上下限制約を満たすようにマッピング
        mapFucn = lambda x: 0 if x < 0 else len(WORK)-1 if x > len(WORK)-1 else x
        mutantParent = mutantParent.map(mapFucn)
        mutantParent = np.round(mutantParent)  # 四捨五入で整数に変換
        print("mutantParent 四捨五入")
        print(mutantParent)
        self.createChild(mutantParent)
 

    def createChild(self, mutantParent):
        print("createChild")
        """
        print("mutantParent")
        print(mutantParent.unstack())
        print("mutantParent len=", len(mutantParent))
        start = np.random.randint(len(mutantParent))
        print("start=", start)
        count = 1  # 交叉で交換する数
        while True:
            if np.random.rand() > Cr or count == len(mutantParent):
                break
            else:
                count += 1
        print("count=", count)
        gene = self.gene.stack()
        print("gene=", gene)
        print(gene.iloc[start: start+count])
        # child = gene
        # child.iloc[start: start+count] = mutantParent.iloc[start: start+count]
        # print("child=", child)
        print("----------------------------------------------------------")
        """
