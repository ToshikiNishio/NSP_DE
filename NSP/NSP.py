#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:08:48 2018

@author: toshiki
"""
import pandas as pd
import numpy as np
import EvaluateFunctions
import DE


if __name__ == '__main__':
    # パラメーターの設定
    MAN = ["A", "B", "C", "D"]
    DAY = ["07/01", "07/02", "07/03", "07/04", "07/05"]
    WORK = ["休み", "日勤", "準夜勤", "夜勤"]
    GROUP = ["バイト", "社員"]
    # PROBLEM = []  # 未設定
    PROBLEM = None

    requiredManNum = {  # それぞれの日の合算はMAN人となる
        "07/01": {"休み": 2, "日勤": 2, "準夜勤": 0, "夜勤": 0},
        "07/02": {"休み": 2, "日勤": 1, "準夜勤": 0, "夜勤": 1},
        "07/03": {"休み": 1, "日勤": 1, "準夜勤": 1, "夜勤": 1},
        "07/04": {"休み": 2, "日勤": 1, "準夜勤": 0, "夜勤": 1},
        "07/05": {"休み": 2, "日勤": 2, "準夜勤": 0, "夜勤": 0},
    }
    requiredDaysMax = {  # 項目の最大値はDAY,最小値は0
        "A": {"休み": 2, "日勤": 5, "準夜勤": 0, "夜勤": 0},
        "B": {"休み": 2, "日勤": 2, "準夜勤": 2, "夜勤": 1},
        "C": {"休み": 4, "日勤": 0, "準夜勤": 1, "夜勤": 2},
        "D": {"休み": 2, "日勤": 3, "準夜勤": 3, "夜勤": 3},
    }
    requiredDaysMin = {  # 項目の最大値はrequiredDaysMaxの対応する項目,最小値は0
        "A": {"休み": 1, "日勤": 1, "準夜勤": 0, "夜勤": 0},
        "B": {"休み": 1, "日勤": 1, "準夜勤": 1, "夜勤": 0},
        "C": {"休み": 1, "日勤": 0, "準夜勤": 0, "夜勤": 0},
        "D": {"休み": 0, "日勤": 2, "準夜勤": 2, "夜勤": 2},
    }

    # 表示する勤務表作成
    matrix = pd.DataFrame(np.random.rand(len(MAN), len(DAY)) * len(WORK),
                          index=MAN, columns=DAY)
    print(matrix)
    matrix = np.floor(matrix)
    print(matrix)
    for index, work in enumerate(WORK):
        matrix = matrix.replace(index, work)
    print(matrix)
    # グローバル変数をimport
    DE.importGlobal(gl_DAY=DAY, gl_WORK=WORK, gl_requiredManNum=requiredManNum,
                    gl_MAN=MAN)
    EvaluateFunctions.importGlobal(gl_DAY=DAY, gl_WORK=WORK,
                                   gl_requiredManNum=requiredManNum,
                                   gl_MAN=MAN,
                                   gl_requiredDaysMax=requiredDaysMax,
                                   gl_requiredDaysMin=requiredDaysMin)
    de = DE.DE()
