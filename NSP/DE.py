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


def DE():
    '''
    Differential Evolution
    '''
    print("DE initalize")
    pop = Population()
    print(pop)
    for gen in range(MaxGen):
        print("gen=", gen, "********************************************")
        pop.createChild()
        max_ind = max(pop.pop, key=lambda x: x.fitness)
        print("max_fitness=", max_ind.fitness)
        min_ind = min(pop.pop, key=lambda x: x.fitness)
        print("min_fitness=", min_ind.fitness)
        if min_ind.fitness == 0:
            print("Calculation is end. Fitness is 0")
            return min_ind
    print("Calculation is end. 最大世代数まで計算終了")
    return min_ind


class Population(object):
    '''
    population of DE
    '''
    pop = []  # 個体Individualのリスト

    def __init__(self):
        print("population initialize")
        for i in range(NP):
            self.pop.append(Individual())
        print("max_fitness=", max(self.pop, key=lambda x: x.fitness).fitness)
        print("min_fitness=", min(self.pop, key=lambda x: x.fitness).fitness)

    def createChild(self):
        # 個体毎に子供作成
        for idx, ind in enumerate(self.pop):
            parent_pool = copy.copy(self.pop)
            parent_pool.remove(ind)  # 対象親個体の除外
            parents = random.sample(parent_pool, 3)  # ランダムに異なる3個体選ぶ
            mutantParent = ind.generateMutantParent(parents)  # 差分変異親個体vの生成
            child = ind.createChild(mutantParent)  # 子個体生成
            if child.fitness <= ind.fitness:
                self.pop[idx] = child


class Individual(object):
    '''
    indivisual of DE
    '''
    gene = None  # 遺伝子には人を識別するためのインデックスが格納
    H1 = None
    H2 = None
    H3 = None
    fitness = None

    def __init__(self):
        # 個体の生成
        gene = pd.Series()
        index = []
        for day in DAY:
            # day日の遺伝子を作成
            series = pd.Series(np.arange(len(MAN)))
            for work in WORK:
                num = requiredManNum[day][work]
                for n in range(num):
                    index.append((day, work))
            np.random.shuffle(series)  # ランダムに並び替え
            gene = pd.concat([gene, series])
        index = pd.MultiIndex.from_tuples(index, names=['day', 'work'])
        gene.index = index
        self.gene = gene
        self.calcFitness()

    def calcFitness(self):  # 適応度計算
        self.fitness, self.H1, self.H2, self.H3 = calcFitness(self.gene)
        # print("fitness=", self.fitness, "H1=", self.H1)

    def generateMutantParent(self, parents):  # 差分変異親個体vの生成
        P1 = parents[0].gene
        P2 = parents[1].gene
        P3 = parents[2].gene

        mutantParent = P1 + S * (P2 - P3)
        for index, day in enumerate(DAY):
            st, end = index*len(MAN), index*(len(MAN)) + len(MAN)
            gene = mutantParent.iloc[st: end]
            argsort_list = np.argsort(gene)
            mutantParent.iloc[st: end] = argsort_list
        # print("mutantParent")
        # print(mutantParent)
        return mutantParent

    def createChild(self, mutantParent):
        gene_len = len(mutantParent)
        start = np.random.randint(gene_len)  # 交叉スタート位置 0~len(mutantParent)-1
        assert start < 15, "start >= 15!!!"
        # 交叉する数を決定
        count = 1  # 交叉で交換する数
        while True:
            if np.random.rand() > Cr or count == gene_len:
                break
            else:
                count += 1
        # 交叉するインデックス取得
        if start+count < gene_len:
            cross_idx = np.arange(start, start+count)
        else:
            tmp1 = np.arange(start, gene_len)
            tmp2 = np.arange(0, start+count-gene_len)
            cross_idx = np.hstack((tmp1, tmp2))

        # 交叉処理
        new_gene = copy.copy(self.gene)  # 自身の遺伝子をコピー
        """
        print("new_gene")
        print(new_gene)
        print("mutantParent")
        print(mutantParent)
        """
        for index, day in enumerate(DAY):  # 日付で分割して交叉処理を行う
            st = index * len(MAN)  # 日付の初めのインデックス
            end = index*(len(MAN)) + len(MAN)  # 日付の終わりのインデックス
            # print(new_gene.iloc[st: end])
            cross_idx_day = []  # 交叉処理を行うインデックス
            cross = []
            for i in range(st, end):
                if i in cross_idx:
                    cross_idx_day.append(i)
                cross.append(i in cross_idx)
            if len(cross_idx_day) == 0:  # 交叉しなければスキップ
                continue
            cross_gene = new_gene.iloc[st: end][cross]

            mutant_gene = mutantParent.iloc[st: end]
            # 差分変異親個体で交叉対象の遺伝子を抜き出す
            cross_pool = mutant_gene[mutant_gene.isin(cross_gene)]
            for count, ind in enumerate(cross_idx_day):
                new_gene.iat[ind] = cross_pool.iat[count]
        # 子個体生成
        child = copy.copy(self)
        child.gene = new_gene
        child.calcFitness()
        """
        print("child.gene")
        print(child.gene)
        print("********************************")
        """
        return child
        