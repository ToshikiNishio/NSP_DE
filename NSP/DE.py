#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import pandas as pd
import numpy as np


class DE(object):
    '''
    Differential Evolution
    '''
    S = None  # スケーリングファクター
    Cr = None  # 交差率
    Pm = None  # 突然変異率
    Np = None  # 個体数
    MaxGen = None  # 最大世代数

    pop = None  # Populationクラスを格納するための変数

    def __init__(self, DAY, WORK, requiredManNum, MAN):
        print("DE initalize")
        self.S = 0.4
        self.Cr = 0.9
        self.Pm = 0.01
        self.Np = 50  # 50
        self.MaxGen = 100000
        pop = Population(NP=self.Np, DAY=DAY, requiredManNum=requiredManNum,
                         WORK=WORK, MAN=MAN)
        print(pop)


class Population(object):
    '''
    population of DE
    '''
    pop = []  # 個体Individualのリスト

    def __init__(self, NP, DAY, requiredManNum, WORK, MAN):
        print("population initialize")
        for i in range(NP):
            self.pop.append(Individual(DAY=DAY, requiredManNum=requiredManNum,
                                       WORK=WORK, MAN=MAN))
        print(self.pop)


class Individual(object):
    '''
    indivisual of DE
    '''
    gene = None

    def __init__(self, MAN, DAY, WORK, requiredManNum):
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