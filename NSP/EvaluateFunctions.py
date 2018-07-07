#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import numpy as np


def F1():  # 勤務パターン負荷の軽減
    return 0


def F2():  # 禁止パターンの低減
    return 0


def F3():  # 必要日数の確保
    return 0


def F4():  # 勤務間隔の均等化
    return 0


def F5():  # 必要人数の確保
    return 0


def F6():  # グループ人数の確保
    return 0


def F7():  # 勤務の質の確保
    return 0


def getFunctions():
    return [F1, F2, F3, F4, F5, F6, F7]


def calcH1():
    return F2() + F3()


def calcH2():
    return F1() + F4()


def calcH3():
    return F6() + F7()


def calcFitness():
    H1 = calcH1()
    H2 = calcH2()
    H3 = calcH3()
    array = np.array([H1, H2, H3])
    return np.linalg.norm(array)
