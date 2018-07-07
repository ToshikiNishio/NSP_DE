#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import pandas as pd
import numpy as np
from EvaluateFunctions import calcH1, calcH2, calcH3, calcFitness

DAY = None
requiredManNum = None
WORK = None
MAN = None


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
    S = 0.4  # スケーリングファクター
    Cr = 0.9  # 交差率
    Pm = 0.01  # 突然変異率
    Np = 50  # 個体数
    MaxGen = 100000  # 最大世代数

    pop = None  # Populationクラスを格納するための変数

    def __init__(self):
        print("DE initalize")
        pop = Population(NP=self.Np)
        print(pop)


class Population(object):
    '''
    population of DE
    '''
    pop = []  # 個体Individualのリスト

    def __init__(self, NP):
        print("population initialize")
        for i in range(NP):
            self.pop.append(Individual())
        print(self.pop)


class Individual(object):
    '''
    indivisual of DE
    '''
    gene = None
    H1 = None
    H2 = None
    H3 = None
    fitness = None

    def __init__(self):
        print("inidivisual initialize")
        # 個体の生成
        gene = pd.DataFrame()
        for day in DAY:
            series = pd.Series()
            # day日の遺伝子を作成
            for index, work in enumerate(WORK):
                num = requiredManNum[day][work]
                series = pd.concat([series, pd.Series(np.ones(num) * index)])
            series.index = MAN
            np.random.shuffle(series)
            gene = gene.append(series, ignore_index=True)
        gene.index = DAY
        self.gene = gene
        print(self.gene)
        print("calcH1=", calcH1())
        print("calcH2=", calcH2())
        print("calcH3=", calcH3())
        print("calcFitness=", calcFitness())
