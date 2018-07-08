#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import numpy as np

DAY = None
requiredManNum = None
WORK = None
MAN = None
requiredDaysMax = None
requiredDaysMin = None


def importGlobal(gl_DAY, gl_WORK, gl_requiredManNum, gl_MAN,
                 gl_requiredDaysMax, gl_requiredDaysMin):
    global DAY, WORK, requiredManNum, MAN, requiredDaysMax, requiredDaysMin
    DAY = gl_DAY
    WORK = gl_WORK
    requiredManNum = gl_requiredManNum
    MAN = gl_MAN
    requiredDaysMax = gl_requiredDaysMax
    requiredDaysMin = gl_requiredDaysMin


def F1():  # 勤務パターン負荷の軽減
    return 0


def F2():  # 禁止パターンの低減
    return 0


def F3(gene):  # 必要日数の確保
    fit = 0
    for man in MAN:
        for work_index, work in enumerate(WORK):
            workDay = 0
            for day in DAY:
                if work_index == gene.at[day, man]:
                    # print(man, work, day, gene.at[day, man])
                    workDay += 1
            # print(man, work)
            # print("workDay=", workDay)
            p_max = max(workDay - requiredDaysMax[man][work], 0)
            p_min = max(requiredDaysMin[man][work] - workDay, 0)
            # print("p_max=", p_max, "p_min=", p_min)
            fit += p_max + p_min
    # print("fit=", fit)
    return fit


def F4():  # 勤務間隔の均等化
    return 0


def F5():  # 必要人数の確保
    return 0


def F6():  # グループ人数の確保
    return 0


def F7():  # 勤務の質の確保
    return 0


def calcH1(gene):
    return F2() + F3(gene)


def calcH2():
    return F1() + F4()


def calcH3():
    return F6() + F7()


def calcFitness(gene):
    H1 = calcH1(gene)
    H2 = calcH2()
    H3 = calcH3()
    array = np.array([H1, H2, H3])
    return np.linalg.norm(array), H1, H2, H3
