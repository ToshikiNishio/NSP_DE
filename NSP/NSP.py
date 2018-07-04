#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import EvaluateFunctions


if __name__ == '__main__':
    MAN = ["A", "B", "C", "D"]
    DAY = ["07/01", "07/02", "07/03", "07/04", "07/05"]
    WORK = ["日勤", "準夜勤", "夜勤"]
    GROUP = ["バイト", "社員"]
    # PROBLEM = []  # 未設定
    PROBLEM = EvaluateFunctions.getFunctions()
    for func in PROBLEM:
        print(func, func())
