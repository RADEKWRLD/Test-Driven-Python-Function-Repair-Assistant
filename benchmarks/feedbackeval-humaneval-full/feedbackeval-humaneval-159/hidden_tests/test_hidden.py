import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[5, 6, 10],
 [4, 8, 9],
 [1, 10, 10],
 [2, 11, 5],
 [4, 5, 7],
 [4, 5, 1],
 [0, 0, 0],
 [10, 0, 10],
 [0, 10, 5],
 [5, 0, 5],
 [2, 2, 2],
 [999, 1, 0],
 [0, 999, 1],
 [500, 500, 1000],
 [1, 10, 5],
 [0, 0, 5],
 [0, 0, 1],
 [999, 5, 5],
 [999, 5, 500],
 [999, 10, 5],
 [5, 6, 6],
 [999, 2, 1],
 [5, 5, 5],
 [0, 10, 500],
 [5, 10, 5],
 [1, 0, 1],
 [6, 0, 6],
 [0, 4, 0],
 [10, 999, 4],
 [9, 0, 10],
 [999, 2, 500],
 [999, 0, 0],
 [7, 7, 6],
 [9, 1000, 10],
 [4, 10, 4],
 [999, 1, 999],
 [0, 5, 1],
 [3, 9, 4],
 [7, 6, 6],
 [10, 5, 10],
 [5, 10, 10],
 [999, 2, 10],
 [999, 0, 999],
 [999, 1, 1],
 [1000, 1, 999],
 [6, 10, 5],
 [999, 6, 7],
 [6, 0, 10],
 [10, 5, 5],
 [4, 5, 5],
 [998, 7, 4],
 [7, 4, 6],
 [0, 500, 0],
 [0, 1, 1],
 [997, 2, 10],
 [1000, 999, 998],
 [997, 999, 0],
 [998, 7, 10],
 [500, 500, 500],
 [997, 0, 3],
 [0, 0, 999],
 [4, 999, 4],
 [9, 0, 7],
 [5, 7, 5],
 [1000, 6, 998],
 [2, 10, 10],
 [6, 2, 499],
 [999, 2, 7],
 [999, 999, 999],
 [5, 10, 500],
 [10, 10, 10],
 [3, 10, 4],
 [3, 1000, 2],
 [0, 499, 0],
 [999, 6, 5],
 [9, 999, 7],
 [9, 999, 4],
 [500, 10, 500],
 [999, 5, 2],
 [6, 6, 6],
 [998, 10, 10],
 [5, 10, 1000],
 [499, 1, 5],
 [1, 9, 0],
 [0, 6, 7],
 [11, 6, 11],
 [11, 5, 5],
 [7, 0, 10],
 [0, 7, 7],
 [0, 5, 5],
 [10, 499, 500],
 [1, 499, 6],
 [6, 1, 7],
 [7, 0, 499],
 [999, 7, 10],
 [0, 999, 4],
 [1000, 4, 998],
 [2, 3, 1],
 [999, 2, 998],
 [1, 10, 1],
 [999, 999, 11],
 [1000, 0, 0],
 [6, 5, 1000],
 [11, 11, 6],
 [3, 499, 500],
 [0, 500, 6],
 [0, 1000, 1000],
 [1000, 0, 1000],
 [500, 500, 800],
 [500, 500, 499],
 [1000, 1000, 500],
 [1000, 0, 500],
 [250, 750, 300],
 [800, 300, 600],
 [300, 700, 200],
 [200, 0, 1],
 [300, 1000, 600],
 [500, 801, 801],
 [800, 0, 600],
 [800, 0, 599],
 [800, 601, 600],
 [800, 700, 600],
 [801, 500, 499],
 [800, 1, 600],
 [800, 601, 599],
 [1000, 801, 0],
 [500, 501, 500],
 [501, 501, 501],
 [599, 501, 501],
 [801, 499, 801],
 [501, 500, 700],
 [800, 700, 201],
 [499, 800, 499],
 [1000, 500, 500],
 [1000, 500, 1000],
 [500, 500, 498],
 [601, 600, 499],
 [1000, 1000, 1000],
 [250, 250, 600],
 [1, 601, 600],
 [1000, 801, 801],
 [498, 1000, 1000],
 [250, 201, 600],
 [801, 801, 801],
 [200, 1, 1],
 [599, 501, 600],
 [800, 202, 201],
 [800, 600, 700],
 [700, 800, 600],
 [499, 800, 500],
 [1000, 0, 1],
 [800, 801, 500],
 [800, 600, 800],
 [501, 749, 750],
 [600, 749, 750],
 [500, 800, 749],
 [501, 501, 500],
 [501, 502, 499],
 [799, 601, 600],
 [501, 749, 0],
 [600, 499, 601],
 [600, 749, 0],
 [0, 600, 499],
 [300, 1000, 300],
 [1, 801, 599],
 [1, 599, 599],
 [1000, 800, 801],
 [601, 601, 499],
 [600, 1000, 600],
 [1000, 1000, 998],
 [700, 800, 500],
 [750, 750, 300],
 [800, 202, 250],
 [800, 300, 800],
 [201, 750, 1000],
 [249, 700, 250],
 [700, 749, 600],
 [499, 500, 500],
 [600, 601, 749],
 [601, 600, 601],
 [601, 601, 601],
 [501, 748, 0],
 [300, 200, 300],
 [799, 1, 600],
 [1000, 997, 998],
 [499, 700, 499],
 [1, 600, 599],
 [599, 600, 601],
 [500, 748, 501],
 [601, 997, 501],
 [600, 800, 503],
 [799, 600, 499],
 [500, 500, 998],
 [800, 801, 700],
 [501, 799, 502],
 [700, 249, 699],
 [499, 499, 800],
 [599, 200, 601],
 [801, 600, 599],
 [0, 700, 600],
 [503, 1, 1],
 [700, 501, 748],
 [202, 0, 1000],
 [500, 500, 750],
 [1, 801, 500],
 [251, 250, 200],
 [800, 500, 498],
 [801, 800, 500],
 [800, 201, 201],
 [750, 1000, 600],
 [498, 599, 600],
 [1, 600, 1],
 [1000, 800, 0],
 [500, 1, 504],
 [498, 599, 498],
 [749, 700, 600],
 [1000, 1, 600],
 [601, 599, 499],
 [201, 801, 801],
 [748, 0, 501],
 [251, 499, 498],
 [1000, 999, 1000],
 [498, 499, 800],
 [801, 1, 1000],
 [0, 999, 999],
 [500, 498, 500],
 [800, 500, 799],
 [998, 801, 998],
 [497, 1000, 1000],
 [300, 800, 800],
 [749, 1, 503],
 [801, 1, 1],
 [0, 801, 599],
 [200, 0, 503],
 [600, 700, 700],
 [998, 499, 500],
 [748, 0, 0],
 [1000, 500, 504],
 [504, 249, 599],
 [700, 800, 1],
 [502, 501, 500],
 [0, 1, 501],
 [801, 1, 498],
 [1, 999, 599],
 [700, 499, 500],
 [750, 1000, 201],
 [999, 502, 999],
 [600, 999, 700],
 [600, 601, 599],
 [1, 802, 599],
 [0, 600, 800],
 [501, 800, 749],
 [601, 997, 601],
 [800, 600, 499],
 [800, 500, 500],
 [801, 498, 801],
 [998, 601, 601],
 [250, 249, 250],
 [997, 601, 601],
 [800, 800, 800],
 [800, 201, 800],
 [801, 201, 201],
 [501, 500, 501],
 [749, 2, 2],
 [599, 749, 1000],
 [250, 250, 250],
 [600, 500, 500],
 [600, 1000, 1000],
 [498, 499, 599],
 [999, 1000, 1000],
 [1000, 1, 1000],
 [299, 249, 600],
 [498, 800, 799],
 [749, 699, 749],
 [799, 800, 800],
 [750, 600, 750],
 [602, 600, 602],
 [500, 500, 251],
 [499, 501, 700],
 [750, 1000, 750],
 [750, 801, 602],
 [0, 800, 0],
 [499, 498, 499],
 [500, 504, 504],
 [500, 501, 501],
 [501, 500, 499],
 [599, 503, 502],
 [498, 499, 499],
 [1000, 500, 501],
 [1, 1, 600],
 [202, 251, 501],
 [601, 601, 600],
 [799, 2, 800],
 [999, 1000, 0],
 [2, 997, 997],
 [249, 997, 498],
 [999, 799, 799],
 [801, 800, 499],
 [250, 599, 801],
 [201, 201, 201],
 [498, 504, 800],
 [747, 699, 601],
 [1000, 1000, 997],
 [998, 499, 601],
 [500, 501, 498],
 [0, 499, 599],
 [1000, 999, 799],
 [602, 601, 749],
 [498, 300, 499],
 [2, 200, 503],
 [251, 800, 202],
 [499, 601, 499],
 [0, 1000, 999],
 [800, 801, 1],
 [0, 500, 1000],
 [500, 497, 500],
 [601, 802, 601],
 [0, 801, 801],
 [1, 499, 498],
 [501, 502, 501],
 [996, 500, 601],
 [800, 602, 600],
 [250, 801, 599],
 [800, 300, 802],
 [502, 503, 500],
 [1, 600, 600],
 [198, 0, 996],
 [602, 602, 699],
 [500, 250, 499],
 [602, 500, 502],
 [0, 600, 0],
 [2, 503, 503],
 [202, 750, 1000],
 [504, 1000, 1000],
 [499, 1000, 700],
 [802, 801, 998],
 [499, 499, 500],
 [1000, 1, 250],
 [601, 202, 499],
 [799, 250, 250],
 [501, 800, 750],
 [499, 499, 299],
 [599, 1000, 600],
 [2, 202, 497],
 [499, 503, 499],
 [201, 1000, 201],
 [299, 800, 800],
 [750, 802, 749],
 [251, 251, 200],
 [748, 801, 801],
 [300, 200, 200],
 [500, 748, 499],
 [251, 800, 600],
 [601, 300, 802],
 [802, 499, 800],
 [700, 1000, 1000],
 [202, 201, 202],
 [1, 1000, 599],
 [601, 250, 499],
 [501, 799, 748],
 [200, 1000, 500],
 [1, 300, 600],
 [802, 802, 602],
 [500, 503, 504],
 [750, 501, 750],
 [251, 202, 1000],
 [299, 501, 799],
 [800, 800, 497],
 [700, 201, 201],
 [502, 249, 250],
 [999, 504, 0],
 [299, 503, 502],
 [747, 499, 499],
 [1, 800, 500],
 [200, 0, 200],
 [0, 999, 0],
 [202, 499, 800],
 [800, 501, 498],
 [600, 500, 499],
 [200, 750, 1000],
 [500, 999, 799],
 [749, 600, 600],
 [501, 749, 501],
 [800, 800, 200],
 [700, 699, 700],
 [250, 249, 1000],
 [999, 502, 700],
 [498, 498, 599],
 [500, 500, 503],
 [801, 201, 200],
 [800, 801, 800],
 [598, 499, 599],
 [750, 999, 750],
 [497, 750, 999],
 [999, 499, 500],
 [599, 600, 599],
 [500, 500, 253],
 [700, 701, 1000],
 [201, 800, 602],
 [201, 499, 251],
 [501, 999, 501],
 [997, 997, 2],
 [1000, 502, 501],
 [501, 502, 800],
 [750, 750, 750],
 [748, 0, 999],
 [298, 501, 799],
 [599, 0, 999],
 [501, 600, 501],
 [299, 498, 501],
 [1, 802, 802],
 [1000, 1000, 700],
 [599, 501, 599],
 [501, 500, 500],
 [1, 501, 500],
 [801, 800, 602],
 [600, 602, 602],
 [748, 801, 748],
 [500, 699, 699],
 [202, 501, 501],
 [600, 603, 2],
 [997, 998, 998],
 [801, 602, 602],
 [249, 998, 250],
 [499, 250, 250],
 [499, 198, 749],
 [602, 799, 602],
 [601, 600, 298],
 [499, 598, 599],
 [498, 498, 499],
 [0, 497, 504],
 [200, 748, 1],
 [497, 504, 497],
 [501, 0, 1],
 [499, 250, 251],
 [1000, 999, 999],
 [1000, 999, 500],
 [801, 601, 599],
 [601, 600, 599],
 [1, 500, 1],
 [998, 502, 700],
 [200, 1, 504],
 [749, 202, 202],
 [997, 500, 500],
 [503, 501, 500],
 [1, 1000, 200],
 [750, 599, 751],
 [1, 500, 503],
 [498, 750, 498],
 [800, 2, 1],
 [599, 600, 600],
 [699, 502, 300],
 [998, 999, 999],
 [500, 801, 499],
 [198, 600, 498],
 [200, 748, 200],
 [499, 801, 299],
 [0, 501, 501],
 [200, 201, 201],
 [2, 801, 1],
 [700, 803, 0],
 [501, 253, 501],
 [500, 501, 799],
 [1, 699, 1],
 [503, 250, 1],
 [701, 501, 748],
 [499, 600, 600],
 [602, 602, 602],
 [0, 600, 801],
 [600, 599, 803],
 [601, 601, 750],
 [700, 701, 600],
 [201, 501, 749],
 [503, 801, 998],
 [499, 299, 299],
 [300, 800, 803],
 [801, 802, 801],
 [499, 499, 499],
 [499, 700, 498],
 [598, 599, 502],
 [601, 1, 751],
 [802, 801, 300],
 [799, 800, 600],
 [500, 503, 503],
 [1, 1000, 1],
 [600, 801, 299],
 [997, 601, 802],
 [800, 801, 498],
 [201, 799, 201],
 [0, 200, 801],
 [1000, 997, 997],
 [750, 751, 750],
 [500, 0, 500],
 [250, 500, 500],
 [799, 747, 799],
 [501, 599, 501],
 [602, 996, 602],
 [601, 599, 0],
 [502, 700, 700],
 [800, 1, 800],
 [199, 200, 748],
 [1000, 498, 498],
 [298, 1000, 600],
 [499, 500, 700],
 [200, 202, 499],
 [998, 251, 998],
 [700, 249, 700],
 [599, 599, 599],
 [497, 1000, 999],
 [503, 998, 801],
 [799, 601, 599],
 [500, 250, 750],
 [599, 251, 500],
 [201, 802, 599],
 [504, 800, 502],
 [200, 200, 199],
 [802, 600, 801],
 [200, 800, 497],
 [1, 1000, 0],
 [799, 998, 999],
 [801, 201, 603],
 [500, 251, 501],
 [253, 498, 504],
 [500, 997, 251],
 [799, 800, 603],
 [198, 1, 3],
 [250, 250, 248],
 [997, 751, 999],
 [600, 503, 502],
 [299, 202, 600],
 [503, 250, 502],
 [801, 801, 253],
 [500, 1000, 500],
 [248, 249, 701],
 [599, 803, 600],
 [1000, 201, 201],
 [802, 500, 503],
 [499, 299, 601],
 [2, 1000, 502],
 [498, 499, 498],
 [199, 498, 600],
 [499, 599, 599],
 [0, 803, 800],
 [199, 750, 1000],
 [801, 500, 498],
 [498, 498, 498],
 [201, 202, 1],
 [202, 1000, 497],
 [2, 200, 750],
 [1000, 249, 999],
 [749, 749, 749],
 [800, 600, 250],
 [499, 299, 603],
 [501, 748, 748],
 [501, 502, 748],
 [300, 601, 300],
 [600, 600, 600],
 [599, 701, 802],
 [0, 200, 800],
 [700, 700, 700],
 [999, 601, 599],
 [497, 200, 999],
 [1000, 699, 502],
 [501, 599, 800],
 [800, 600, 600],
 [499, 498, 700],
 [501, 996, 502],
 [601, 802, 198],
 [749, 500, 500],
 [1000, 200, 1],
 [502, 1000, 1000],
 [801, 997, 599],
 [502, 500, 503],
 [249, 802, 249],
 [498, 0, 800],
 [996, 801, 800],
 [502, 701, 701],
 [499, 298, 251],
 [999, 801, 998],
 [748, 253, 799],
 [250, 251, 250],
 [500, 499, 0],
 [996, 499, 499],
 [749, 748, 249],
 [601, 1000, 699],
 [499, 598, 499],
 [202, 502, 501],
 [600, 299, 751],
 [251, 500, 202],
 [700, 750, 300],
 [253, 600, 700],
 [600, 601, 2],
 [799, 250, 799],
 [600, 601, 249],
 [600, 299, 299],
 [251, 1000, 251],
 [504, 751, 751],
 [498, 198, 749],
 [799, 250, 1],
 [201, 250, 503],
 [501, 502, 600],
 [997, 998, 999],
 [600, 202, 2],
 [499, 801, 501],
 [699, 802, 801],
 [1, 599, 1],
 [499, 599, 3],
 [799, 799, 799],
 [600, 201, 201],
 [1000, 600, 600],
 [0, 1000, 0],
 [1000, 1000, 0],
 [0, 0, 1000],
 [300, 600, 600],
 [500, 1000, 0],
 [600, 700, 600],
 [250, 750, 250],
 [299, 701, 200],
 [1000, 500, 800],
 [700, 702, 600],
 [200, 500, 498],
 [299, 499, 800],
 [800, 300, 299],
 [200, 498, 498],
 [500, 299, 800],
 [999, 1000, 702],
 [301, 600, 600],
 [1000, 800, 800],
 [1000, 600, 0],
 [800, 200, 800],
 [800, 300, 200],
 [800, 300, 250],
 [700, 499, 600],
 [800, 701, 200],
 [500, 800, 499],
 [498, 500, 700],
 [199, 800, 500],
 [250, 750, 499],
 [299, 499, 300],
 [499, 499, 801],
 [498, 497, 200],
 [500, 300, 300],
 [299, 499, 299],
 [200, 500, 497],
 [700, 701, 750],
 [750, 250, 251],
 [1000, 200, 1000],
 [1000, 599, 500],
 [799, 499, 499],
 [251, 300, 199],
 [800, 500, 800],
 [299, 300, 300],
 [300, 200, 800],
 [497, 200, 497],
 [200, 800, 800],
 [501, 299, 800],
 [199, 999, 999],
 [300, 600, 601],
 [499, 499, 799],
 [600, 800, 600],
 [200, 500, 1000],
 [500, 599, 500],
 [999, 0, 1000],
 [199, 299, 299],
 [700, 702, 801],
 [800, 497, 702],
 [750, 298, 299],
 [250, 499, 499],
 [701, 1000, 700],
 [500, 800, 700],
 [600, 599, 600],
 [500, 250, 498],
 [799, 499, 799],
 [200, 199, 1000],
 [499, 800, 800],
 [200, 497, 200],
 [199, 298, 299],
 [199, 1000, 0],
 [199, 500, 700],
 [1000, 600, 498],
 [599, 499, 800],
 [499, 501, 499],
 [299, 1000, 0],
 [300, 300, 300],
 [299, 701, 599],
 [199, 198, 199],
 [501, 496, 200],
 [801, 750, 498],
 [251, 0, 0],
 [500, 999, 999],
 [999, 999, 702],
 [200, 199, 200],
 [999, 701, 700],
 [799, 300, 800],
 [700, 701, 700],
 [500, 499, 499],
 [601, 1000, 800],
 [801, 200, 801],
 [999, 599, 500],
 [600, 198, 799],
 [1000, 1000, 495],
 [799, 199, 500],
 [800, 301, 600],
 [500, 301, 500],
 [298, 800, 298],
 [800, 200, 700],
 [501, 799, 799],
 [298, 800, 599],
 [251, 300, 0],
 [1000, 199, 251],
 [498, 1000, 799],
 [999, 702, 700],
 [300, 1000, 1000],
 [252, 300, 0],
 [500, 1000, 799],
 [300, 301, 300],
 [500, 1000, 199],
 [702, 800, 800],
 [500, 299, 300],
 [701, 700, 801],
 [999, 600, 600],
 [0, 601, 498],
 [299, 1000, 1],
 [502, 701, 599],
 [500, 801, 800],
 [800, 500, 801],
 [1000, 799, 500],
 [199, 200, 199],
 [199, 0, 199],
 [801, 702, 801],
 [999, 600, 999],
 [199, 749, 499],
 [301, 300, 301],
 [700, 298, 702],
 [300, 300, 502],
 [801, 703, 800],
 [200, 199, 497],
 [749, 299, 800],
 [250, 500, 499],
 [501, 703, 500],
 [702, 1000, 1000],
 [800, 199, 800],
 [700, 600, 600],
 [600, 599, 599],
 [999, 999, 1000],
 [1000, 200, 799],
 [999, 800, 750],
 [299, 298, 701],
 [200, 301, 801],
 [502, 500, 502],
 [250, 500, 498],
 [199, 198, 198],
 [800, 199, 250],
 [252, 300, 299],
 [701, 250, 700],
 [500, 499, 800],
 [0, 0, 500],
 [250, 499, 198],
 [300, 599, 300],
 [499, 703, 499],
 [499, 801, 999],
 [499, 500, 499],
 [800, 300, 497],
 [500, 299, 801],
 [999, 200, 999],
 [1000, 499, 499],
 [201, 200, 799],
 [199, 601, 500],
 [600, 1000, 0],
 [201, 200, 499],
 [1000, 199, 298],
 [0, 200, 0],
 [252, 300, 253],
 [300, 0, 200],
 [200, 499, 201],
 [1000, 199, 499],
 [301, 0, 500],
 [300, 800, 300],
 [1000, 749, 1000],
 [599, 500, 500],
 [251, 800, 800],
 [800, 496, 702],
 [199, 601, 199],
 [298, 496, 298],
 [299, 300, 0],
 [201, 499, 799],
 [700, 500, 599],
 [501, 802, 801],
 [750, 249, 251],
 [497, 298, 750],
 [503, 701, 599],
 [500, 799, 500],
 [500, 599, 599],
 [504, 250, 504],
 [601, 299, 1],
 [602, 500, 601],
 [502, 502, 502],
 [300, 701, 700],
 [299, 799, 500],
 [198, 198, 198],
 [504, 200, 500],
 [502, 0, 0],
 [600, 699, 600],
 [600, 700, 602],
 [301, 499, 301],
 [200, 1000, 200],
 [200, 500, 299],
 [500, 499, 500],
 [499, 301, 499],
 [500, 298, 800],
 [500, 800, 800],
 [701, 600, 700],
 [999, 500, 799],
 [300, 199, 198],
 [200, 201, 199],
 [199, 250, 499],
 [702, 749, 701],
 [600, 999, 999],
 [801, 500, 801],
 [299, 599, 299],
 [200, 800, 799],
 [799, 198, 301],
 [600, 700, 699],
 [1000, 199, 300],
 [199, 496, 599],
 [599, 499, 499],
 [502, 500, 500],
 [1000, 199, 999],
 [502, 498, 498],
 [495, 500, 1000],
 [299, 299, 299],
 [299, 298, 1],
 [300, 600, 599],
 [503, 503, 503],
 [505, 504, 504],
 [497, 253, 498],
 [600, 600, 699],
 [501, 802, 701],
 [250, 200, 999],
 [1, 300, 0],
 [800, 198, 301],
 [701, 702, 1000],
 [301, 600, 599],
 [197, 498, 198],
 [499, 0, 298],
 [502, 300, 300],
 [600, 699, 700],
 [500, 498, 498],
 [999, 800, 800],
 [199, 499, 301],
 [999, 703, 601],
 [301, 0, 1000],
 [701, 599, 197],
 [1000, 1000, 298],
 [252, 602, 602],
 [199, 198, 699],
 [500, 701, 301],
 [602, 750, 602],
 [799, 998, 300],
 [500, 799, 505],
 [497, 504, 298],
 [999, 999, 601],
 [503, 498, 700],
 [801, 800, 800],
 [599, 0, 598],
 [299, 499, 499],
 [500, 198, 799],
 [198, 198, 599],
 [300, 251, 198],
 [201, 499, 499],
 [249, 200, 302],
 [0, 800, 800],
 [299, 1, 299],
 [200, 750, 496],
 [250, 300, 800],
 [748, 748, 748],
 [298, 499, 499],
 [799, 199, 199],
 [499, 201, 201],
 [301, 703, 500],
 [497, 500, 700],
 [600, 599, 300],
 [599, 802, 499],
 [299, 801, 300],
 [300, 1, 200],
 [250, 500, 497],
 [1000, 799, 799],
 [199, 500, 199],
 [200, 201, 200],
 [501, 500, 801],
 [505, 699, 700],
 [701, 1000, 799],
 [599, 499, 0],
 [701, 801, 701],
 [200, 749, 499],
 [501, 701, 701],
 [199, 750, 496],
 [252, 251, 198],
 [802, 702, 801],
 [700, 999, 702],
 [800, 200, 801],
 [200, 200, 252],
 [750, 498, 801],
 [1000, 200, 300],
 [800, 300, 799],
 [499, 499, 198],
 [299, 298, 299],
 [298, 300, 299],
 [699, 598, 599],
 [198, 799, 799],
 [498, 802, 499],
 [253, 602, 602],
 [749, 499, 198],
 [699, 700, 599],
 [303, 500, 500],
 [999, 500, 800],
 [301, 299, 300],
 [599, 500, 501],
 [498, 497, 496],
 [299, 0, 300],
 [200, 999, 998],
 [251, 249, 251],
 [299, 300, 301],
 [703, 701, 599],
 [300, 201, 499],
 [502, 501, 800],
 [199, 501, 200],
 [750, 499, 198],
 [799, 249, 799],
 [800, 748, 748],
 [703, 701, 303],
 [999, 249, 499],
 [499, 253, 301],
 [600, 999, 749],
 [0, 499, 799],
 [702, 748, 1000],
 [999, 702, 799],
 [0, 300, 498],
 [300, 200, 799],
 [497, 497, 497],
 [251, 748, 500],
 [798, 799, 799],
 [801, 800, 799],
 [199, 501, 199],
 [999, 0, 251],
 [701, 750, 499],
 [504, 250, 250],
 [198, 197, 198],
 [199, 499, 199],
 [998, 702, 700],
 [801, 505, 505],
 [699, 1000, 700],
 [500, 0, 199],
 [750, 700, 700],
 [798, 1000, 1000],
 [998, 502, 801],
 [200, 0, 505],
 [599, 497, 599],
 [1000, 998, 800],
 [503, 502, 702],
 [301, 500, 500],
 [798, 801, 800],
 [502, 501, 502],
 [1000, 199, 199],
 [500, 250, 600],
 [999, 299, 301],
 [501, 500, 250],
 [702, 1000, 700],
 [501, 499, 500],
 [700, 600, 200],
 [799, 799, 600],
 [298, 500, 500],
 [501, 498, 199],
 [500, 800, 500],
 [301, 999, 600],
 [496, 497, 700],
 [504, 1, 200],
 [501, 303, 801],
 [299, 505, 300],
 [500, 299, 500],
 [599, 500, 600],
 [299, 600, 299]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qXpJGN~*l4MsUkW|?WiuixD>Ier100&0t>;NT7C1&-'
    b'vrmYtnCmR4EG9xnIyZ4;E*8<$l%>e)WfB)P6{6GH7fBi4|pa1(m{;&V>zyH7geS}>8<A40O+D_X!rjvGFF3*xnSY!2KzRt9l%@gy'
    b'EbI;Q2=sqsrVq4~0Z#mEQAOHV<{P+L*KmJ=QBd+Lkt1<1dVlO$T=B(A}%W$Q3=X!2ymzl<xzW3I$&z8GQ+iU*oV_Z4m@NL7~<_k*'
    b'PBZSQNHJ9pHe0Q!j@6=28C0pC4^YG3}*rz4``<U2MvzgaPzE3~O<^xi<k=u-3-'
    b'`Tp$+a1fxTiw1#$9IlB>PaWB^{<b~we7&`@H5?NKGD4MsmE$5&s2xk>Wos?XnUp9+Bl)EY2MdkrMQ26Oe#C}mIkZ4l3$0fS|Md;B'
    b'ls0r@V<MA{7%@xw-shxYxv~PiradK|N0o#eAT`SzsZ86x%+f$#?wz8zJ$T6jors~$-'
    b'C;qVtq!Q$L}(BS*QN%V@e#;`B}~!$A)YC>oiw_>+SRvYguWH)OO_mv**3~v1*7hrc$O^fBRAg`*3yJPHcs9*2_LM`@@^1-'
    b'R39_)60JJ(CcjO1Q#ooaZ+u5uIYa-wMXNP=V23UpImI|bDG~f@N%<b-'
    b'K<N?jvsNWvn+>~Oee;|ik6=hM^{;`?)~PW)@(8IIlCEe=q;XQdt%jF8*Qt^h|9E87p@fcu-_6_y+_-'
    b'%^))sQQNxtk`VhkM0mEbiQ*?W_Gb$@$qgI=7`)PH=@LS^S`QWvh6>n)rwri)9ws)K7^Q#m*si%~a^)!8BrP!-'
    b'&V`F?NkDqJ$?#_~9;npLW$Dnb}oKg&KV*uILSiCEH;c?wu4K0S6SuZV84gdO>$veb==T~fR1^%XEfUTItgroX1^K=JivNdL9=QhT'
    b'd-AHxD=KZ)nRaP-Rs-$W@YS%5d!PD^X!)@%vmslMJirYE7f3V-chI1p^`T11stBw-lY9Wn|?X#x2vR2>+AX5fATX_Q+VJvoP%Vk)'
    b'|9z$x&|2CXg=*!|>>$IAzMV36a76Plu9(h2=@TIdcizN(9QG3B(jt-'
    b'8Lw@>p3{Z@?5fn=<7PnJV>b*|WIUCu?2w@+*@c`)Cn5c`_bZ|zCKxLr;^^gEF!Ff;aGyIFVcF_c;gSU$^acvlRwdxrty6RmsP8}M'
    b'%<l!lp{e|-#iPzp$c&m4>RWyQc8UtBWl<^0LH_qgY2$Fa_taInqFuB)(QExmo3xqbCM5CVX=klAX-'
    b'w>BOPTVJ^mr7D;|QwaclYd{1md<d2X%HFlX7iU;NZ``$y5KkP*@z~h?s4dO5dkA3R*+jvaOH}-DVG>mVmt5XL`q=r*f_-TX3`nwO'
    b'H7%l=3#Y_HJOVvg9H%vj(a*L<IBaz*KD!GPzyPM7K!M@Ge}6(+c>wx6R|5LmFqYL?2|Nx)Rf@$D0AuTT{C%lH068!RB4#_dcwb>d'
    b'C?>csbYLNY^})6`*1x-'
    b'AY!{Z1v3u74F&4AEC)UWbKxP0%VgV5#m9q%+M3Wh<^PH>$LBYlh^Hf%U0BF#e^jjNV2}%TNpUoQ=hgF9<<~s9;){NC+1(H_|6{n7'
    b'Kc969?;alZ3epU?r66AK?c3?%(`LfL668JZsJnRqw3M`9l0%RjWw4BbCR>$v@_QPTfiXW>WFlH7#`(1skBe74N0CITD3NvvV&jL!'
    b'vID_}Y`D2T{T7Da+9<i-QJB0~>-UQAbGo}FS#Xf@zW|Kc@5Sr|L-'
    b'<vmRa9gO`H~>_#fKQM01B$RAz+ymRF1f5d@ffUY094LHnnGWzcwQT33zj+uWs-Aj_CCaMu^7U`d-MjT^VEZHfG9_t5sp-Min9>`*'
    b'~WnB5OA6=M_Z9Ztl|&Sci0L_$7iw7!K;iZq8_H78}3e|;M+l%980ad51h<OGk5}_A-'
    b'K1Z!GTn;LI(|4V<fD3rLtz&Gk`P$RyA0uG(oEnK)ei-'
    b'!JYy333uM^ZMef(EG5UY4)%ntZviyu@D~N&T7_xH2WSM_UsebOA_28z*SZV$rFsYQ&u9>Wfsyo3@LVKM@j&h-'
    b'9&}KQuP3;qbDU%C;i+xozsIqXZ|x=k%RSF}X5S||{Mhi`gZ&%6+}J>5RjD|U7xtZ5K_>;IjTeU2FWJvM<EbI<ks&d#5}W~?Sh9o6'
    b'f8cpUAwMf#HCy0aAt$>S|3u9D1z*-4kS}!xcz0$K-'
    b'F5^CJoLap!70D_Qh^e$D8*D(jmNu;N*MidxO)U!VFbMkAuJ|r8G!)lO;P+IST*QpB%~IM5f+k1XD@ukq+ouMv+3du08>HxX>mbd5'
    b'Wh%apc(0tLFFbm^bQ9&IHOcDaw;5`#KztEDHz-'
    b'$N?fk#*wRBNPpFoz_o|_8SBT2I$wYv=P5dEn7*GaLfm)uie;d9^E2m&}V?uB|P=`__9+%_{lvJz*FnUg2swftots?#SQ^K?hZ-Js'
    b'G*AI}p(Uk)&36wAJpJ?G=f-4H8oemeWG@oc9e}mr@!UqBJ5)-'
    b'*MCYFlpbM?hzMZ7{%BpV_EF*s2s9zxi8cj!q#QLu+R4KSGB24B}vUO2rVp%xyOpXR;UsVcw0Ixuaw!KextM9>%ZXN1K9L*Vh>658'
    b'HG=J>AY9icD|`32Uf)0~oha<v&M3?~G#4>SQKbsTPkCJ!*%3+XxV_f5nK#6r~JTWCwR0{qKEryVXMZ>no3q&ez14(CA-'
    b'72xD&#R=AN9KM$J=D%edF__O`DS5n}4JR4M`KqYAx(~=YR<Mk?H!AUGHzl!6&{(z!8$KP-jVBSjGuqU%F#Ui%rL!$QOF@LgBVow!'
    b'9vH)Z>zWa^hjatRA^HnMgKN$Xr*Q>^uqz8AHdrex45+9+n}<mdFI=dEj-'
    b'Q9))zAT!BREl|k7tXr`No$ySZv1bPlf=T(kpM{GMXePZ1r@p_z~Os_d1k%B%onD1peVr^6Vk62xX{{N}f4vDIKCZa*PNJ@UIPX|4'
    b'za9--S~0?kyAL9|s0mD@&5us4xt4sYoNAa>iI37JrJ|QBf*)UNZ}`I}$CepWTSm<zaxnhv>Bfn#2)?=oOHG!Yq6@;0~Rb6YxCX$b'
    b'rm&`QU5JZ#^7T2`mXt2xG&MCuAm|))l*;BNoBJ0rPf&;9!mSJaF*2<rVDP&o#|sf2ZUosE#o#+}VIoLOJr(cm>oabO^FzKGjHU&>'
    b'1y9w1oo~{SF`x(H)bgnFsb0A=HM%Uj#?Ro{V(&AC}b6j9>=Xf+CqXHv3~n0f^N$Sdf^3FON&dwJNJbI4C1TI0c?0r^*wYz>*u$-'
    b'i@Xp5w7{I%o?PLLGrpQwb}@u@KOWmdL`7rybSI_^uo6X0nW9Ee1UfpF<N}<4DbThZeS&gC>>#)r{?vsCRP$!vLhSEijAPVgp?1TH'
    b'qCj%d#s&*OW5ierEbHcr%K|fac#c<CP0bUYH258WeE5~cN1QaQq}1sJl6sk?jOI@EZB_W854$y3~d-'
    b'GqChYS4zL@xV@MFOGf&pxBnk)++R(dU`R7yX;07qL0~sR5CbU=)`On^TmV*W(KsH!=ln?DMRs$Wo;`+yWzd+$yK`a1SM*MWHCwT<'
    b'{d_me0ud_Sc3H}2T&B*TKIz-'
    b'<wu}rq&?U8&SwC2TUSNxTr(An2MvFlYp9kgu}$7J6!z6}Gi(nls_I9*@__gfnT|57kIbBhiUeG}}c>BJg-'
    b'56q0{N;O@Cp=@~Og1W`LT`e<X7r(U`(m3o7Uf;q@xGp{qUCTkI4Ti+cdlp@PeOF}_zg+0D<uJH;KW6I0E&!U~36LDIpb95|T$E|-'
    b'UhIKS?(p4=cO#42XfR^rB!6u6Dqly4tls9B#;Tm)bkM$0z&)`su;dvW1RF88GP}Pg5rX$R4(rHyy(RnJmjvI@*YX6&O{}NzyHjQl'
    b'ibi&6Z8jQ}iDm@lcs*Y#k#&e9-'
    b'j4y=8gGB#&Zt)$pzuU>+Ztu)JpL>`+b{kS6r0P43Rx#B9ywHgR=j+~U2vENN)asAfYrnCA?Y5w#F4_NiVGOwv~md14br`lfCT7r-'
    b'd>(OT4JIf(Tr$CD4Y<1iJEH2lK@jLJQEMVvrZT@LK3E2`L~{eq50vb?ru21Q3jg@YZjM@pf`)1psdho5v%QRwBlf-QyT<N52r^Am'
    b'C(5R+Y{OZ&xOq|&=Or0#c7(P6Pw^Sa2g>!Bb7Ajg6k1mcoR7-'
    b'vJnLl+uPeRz5=g?qIOmcH1kADO9~zE{>}5?N1zN=h%_k}9!wn?=>OqVf95yhkfhFFp4IlTjX|IR3Mxbh{1uxR4U^i0Wa-'
    b')gJ!bt<VEga=RKd6ND!4=^)>I(PFtCDZZ6G&rIpKl15)rHEoC#t=6aro(N87$}3O!Y7+=R!5)`T1quk$!MkcY|k;@m1?1j5IoAcA'
    b'E(T@@FU<z*BDdvS`rc_WihDF$poVMBuf>*fZd*$0%`keX8vHUXXl@nxUTo<Fv=byi-1H-'
    b'kq^151NASrzbi7!=XX%~=W1#H}ScJ8J3!1$Y{Oc$auNvA-4*uHS&3q^)$`6Nq>=JeP%rDg(f<1(7=t-mx-hk#mp8@LT>mC^rFM&`'
    b'E=_Czu|#OTd9P!-'
    b'XJ|Y%)Iroah$%c<^ae*#8eGw%7>4n8*~hDR?dnoIPV1AZZY;z~;AhI?mg%MOj8c53y9J_W1T=h|ybGn^1=c&Y|{N1bOf>1SV>0)L'
    b'peIW9<ah#<q#Skq8x)1hW5x&_Ix(vKz#R9Ud%fs?xEDn`*!+KzMX&fn@rkJ!p`0BE9$DRgOm%K+StcHW7ZI&Du=RE;@XKhsc#J#0'
    b'Wq^*c)z~h=_4Zeegv6Er`Ct;x|XDz~csrV>V#RH3e^i+8%yaliq=xp<j+Gz=;mF7e0=&`$Z6_e`|v}3dl!;Jn@wL+V1QV6cOMyap'
    b'vj5vcO-%Sg{}IP-Z`*@a9PI-fQA)*#d#J8~ln`D8KdS0*B499sp{DNJ4Rk4kOw3z%tZ=>P15I$C4EW$^xLb%hKX`c)v~!_*~3l7n'
    b'sx0og!ir9SO$6fObDHHY6+p_icdL04KBxl!D3Bq8~j8rHZ`JH+E3bbdDE*`oo^GnZxT?qofHLEpK1yk=^V}EUHrHKq%kJ=3tv!G6'
    b'XHbZ)W(#$c|rejyUe&kK%4?>ijhQteAh*{WuyMLJ*1X2O<g`26V7|JjV^)x3k<J0m}wLdje8HQ4j_$*{{%obO_<#tnM#6(gAvisM'
    b'-#dyD;X#15U(B+r1rhZIl-'
    b'D3Bo}r{jE(7Y<7YXATZc1elY4psWh|<Vq)~ub$wrsZfA&_9_DkJH_!9)xK|`53rIdUCB_%3I8P|)k?uJr#Decl(J`Hy5MFjG=oC0'
    b'eXT$67V|Yujun~b00giwh2uzE$9PIJHwb({tEzF7ySk`%FoTWE$3&8UCF-bpz<TF#O#ey5l%|k)v(K%B`Y{ang**Cxn!#-'
    b'eK{2r#)@bjsFaU6Dqk6FGE^>rFq_0tApW#`yl9s!xi#}-I9uFlRi$ow4L?5aCd;PF`e1V+-'
    b'@IJ+IJe7aO>gXYalyx3dZo=Aq$Mw>tkAki5Jc?%RMIZ((3A(<$Xv++Vu*HdFdmOB(VZo4KV2Zhf2HI|EwOA~-'
    b'b<)61v^A#@^hsEJ4@H;w~1X5)sP!LL?EXhwu>@qfeBC5hbbuE^pG#rZm+T)jMtRsp5KHS20S0+8wb?q3o0>*$Dqa=7W@urMK4@i_'
    b'y1(tipzq5292~-ZpUN-'
    b'S<!?%g{2d;^1vegeejjyJ?zI$Qw81+Bvbr0;8WU~%!AQHqj3=pwX0aLtS!j=+3FHEhwWG{A1;BJtQL+El~-'
    b'5*QGWDkD?y$=bKKRVcg7kECtiq5u_5L5W&{tnj)pCa~p(60C3<&hP?(&2B|7E%zYoC+JvJ~pIN&~+ND52tTzQUdsVf&*^iPiCzQ9'
    b'0ThiibTh&8LBl8od?$q7H>G?(!DECHh_6+5DE;v=C;3+T$Y!|nk*%zHq2ce9?;pKV-'
    b'?SbieSMJF!$&?7Z(&XjFA8?mRAaHi|b?O0Cg|@%K6R@c_-LI!34o3QRU-68Rj!rnCJ|6jh4Bzh=AA1)ri(x#KZIUY5u)FhS-ONZa'
    b'=_!Y+UHgk9E<&5u#7dkZe2b5?w=PHtav><isyIof~h735xs^jx}_Mm*@8|PhG$1OcZ=oC|T$@L+!!2GOE|t34d+Tk3XM!bOre6X$'
    b'VjW6`6EX+hyxBDD|iN1$<YSmhQ8mrl<*5!AC_|{_%(pDB1A0Q?^s>4XM25_8teTizop<_}p0ue+!(>%H69&rwS0qA-'
    b'd|oqi|(eVDpO(^9jy*wT9ZQ>j2A8{D>bw<818#QgyiTzgAH<>pm=g^xnbDB6?O?jHR=VsynX;or2L6EDF`?CUD-'
    b'spv>FiX{!;8utRv-c<Y+~UNKyci3Mbcd?N0_c8xexS@9kT<wpyEju`Njfqn-NE1{Jq?J2asG#-'
    b'|1d4xcc8)rhtBBT)xv%|`C)Dd7mF%wFOef}Jqxg`P*3>%oAzmLJ;d9>iNj>mOrog1VvB2-'
    b'1j*VKtdj%)(_jp*u%13B>9*(!u_<+qU`^-'
    b'uz)7AlKM0EpYIl@CS<p45);=y<H>b$V?4UBo@SE?2s3UB$mWzroNvk?=DKcy`H49)=jk$=0fsPhQ;-'
    b'_}RO<`IMpi?G&o=$Z`*F)!idVhuIiRkOe-'
    b'q+bsMCJL?;Abh4F!m<T8k_5?yz60T)Hbxa!p7{hhVNBrhQ6>T7lAd0#S?Mj}&jrkaiHlZ4nC}}V;r|dc1L-jZ-'
    b'+XoRsP~B8qq6a(FurK5P)auU|Kn>o_=k~xphtA3_Lz5wi;>OvOq&xbG`(6P8N5JR_VQfQ2P5c*Ta-'
    b'43n!;qwK7?G8LQq(D%5`VqRrtFMzeoIWy0uxVP&?~Hajygd(<flVj@z`6}`ARrSDQe@vUnTuaLI`-'
    b'f{M$2%5hWhkUcw9;Ry%AqDqS#oOrFO?I8Q#dxW>cqUBDx{G@#tTxO`8OaC@SLPItGQ;!F>|pM?t9%DKRs_|Ub$23}`}st3egPywD'
    b'8aj(@u(WBge0Kg?Q3g%~{u%l?grR0iI@Bw0%8^ouqBh9QEFK1EL_c!@<;DAagF9kc4jSy{-$&0m8(wJk<&Sp`o@ZIcyjKfRev-'
    b'!5(9<9D2ZOAoN&dzu5Dd=Kz5OxqS<Qs7%$tSBHNul{Dqkbyesf<wSydbI@Q1EyWP=W2}#P!()9uL^$H&{h*l;5qZxDKbr==KTVSL'
    b'9Rn54M!ErPFw;308n?FmQkJqbPgtRNn&*`UNyMl>rt)<LJ<afr+UG;1}*72FdHnT|Zq17FF7mo3pM<iLa88%?}ig(w^{{vOii;vM'
    b'x8@2AG{r8-'
    b'*=b8i{FZ_Zmvfo65`z@gQN1@b4fVY4p>Kt@J#&#OWUseFPMbZarQdtpdP<hdzqFGAZ62Ny|co2sf&!RaLxX_?rm)Vp9WP410k+?J'
    b'J<8pS6EVZh<ivMJOt#;fZy7n3TqdvS;`3J2ro~V!fq2p*vyoxo_{o9|>se2=s)57GU9EuE=E8Xs9A>I7D>GvAFczY4yrBb_Z*R?*'
    b'arcuHVzN+O*_zEf?!Kcu8<5?4XMQ?{s*_ws=2N&aMy=o05MIj?<MX-'
    b't6Wk?Uj}iA7DNq<Qf(3qOy$m4^pi(90eceh1qL(ZabOXA11)8Hyxv4tpnC^us>xn<5oTRFC{={nGp66b&MDmoEpO9+ev&HVBHB=>'
    b'8-kZba?{Hhwl6KUG8;N5_H!p&aH$LcVHUdu_TdpBLf=VHcaPc-'
    b'2=AqX4nO^9J}j)V76>JJaMBCu#7%GuF)D2n2oBuR}w>qx1xYmfrEdATS36)0Tu|7tfcr9Qdh*qj^OHIJfSJ?AAQ+OQVZ8jL<YFLa'
    b'(ZqGw}<V*8SAL>&dL%PPbhL5cz~cPWHwOMnBX<;my-'
    b'3NS~X(t^!;WZ@{Fu{)cLG<aEUEJ4a$T)Y}6%kBJwVaSb<03T!U2^Jl_Gg_k1ga!d5zLlbS?wPRIhg7G1|lef3IS-'
    b'l*Z?up;m(;%R^v%0q`hA}IIt+Eu^9$JFKPY-L6%O=TGIvzYt_ZepxKkV^1Th8Kds&ib-LelL|o(pW6iw}XZ|HoJ?8g8%Fs0>8m#2'
    b'!cQu9<h%CuZ{yDR4|<%P|O$$ZtPXglXDznZ;>6>o6aqvp-'
    b'x9#Gn(=D9w*67s*?r84BX9jesu*%T<QEiVY`S06AY9{E))eBfKeq!meM-ju^P)eRH>0yK*1Qca1*YS>@~kE)WH_P_r6M*5hH{V8e'
    b'NqW=^!s>gA;sf3d+4vjT0~ZR}x!%YA~!X?_lwJ0!rimz%OD(C7r`o_K&ok#go(y86dO=rGfpPW<tff_^OH5g`@mXpqD_ff>eJaLX'
    b'8L>=fm3J_=TuXI82yDnWelv6$lQe_n0R<N~zuuH0+_3F_omJ0O`^|%JDi%$b{F8#`8JVXhnDPM1dwZi1q-'
    b't>SQK@2#JD|Pux?tt03~6xOK%pVY5Sgm%!Q;8spy*qbjOyasi4u{eY~guY$}~!X0FXxZzd>D1zv)Qt)N74YRM3dv~W;J3w|TID2q'
    b'G30VS(&R!%*8g@!l3={?$fE%y}KaA&~2-'
    b'=k%z!OkLNYdqlvb<n9a2_2@K!kXasq}U<sICFyksJo0vnt*|diORm;364T<CMb}_v}`1K??#ZD4tBgEAdP>DpBrQSP_-'
    b'7@t9So4!;0{)>I9Kv$ohIh?Kz~7Lj+J?n3q8b~9n9LxM)+&4w-'
    b'@7wUB4$N!dc9yW_Kkge<i&qB$maE|Ep<$s~i`S_*`UqlEDNteSQNYBIoU6$HS;Z7?1Z2&8gRmX7w-'
    b'HFm(eCEtsA)slQaQYtQusdT;x*#P|-=oz>u89CT-%5OUWk&2_Wk>PA6j-'
    b'=fmIat<^RQuTwXfjIM4uEmZCTIH(uuIEnr_6WfMNrmd<JM7Fc+`O+XEp{Iy#EP;dnT@N+xv;9p>Lo@m@Nn>q?Nvtg^14wc^UU(b+'
    b'1`petSE<WhMJ)X`Mw19SGb4(8FhAFG)7StURwAPk8>V6AKl0z{yQ>&(P1)uY`+R5ysz<jdq8b`LWjZFq*(>;+n?1hMqS?!s7=m>k'
    b'&r%rYWBbXLUn6W&>Xsl-'
    b'y90)pD%7U=Re{H#=E)UluRL^tL3@~yC7C44TW1r+^y#s&!B#5pru3fcWbKg3p<Kr0|Okb&4<a|BydDFhnHla!G+P~qT?8k>xyQ%p'
    b'V-'
    b'I$m$m^!)1Zl>f>LH{DUAQojUMzLxE7>ee$5S0HbKwV<0e0$SPFqw_hxwK>qwLReMa?J!sCBtRB|DY8`;^C(BYLG>+DSFnhztW(W`'
    b'T2k5VTg~tY(%~ab^)@0;S&Qm<Lmf<D_L!hNv$nMTCIn$!tKjsRMRT#mfz|)kW&+MTr~*=@wMq5jK~>9qIb=jM1r?9p#ODbYf&Zr~'
    b'>^@Uzyl%bbr*eso*;XPj%RwMf=?7Tj3!Wa~>J=gSl~Z8<@Jtn81a+5i@qWys1kYEOZg1>{5W3wg{E>rVqZm{Pt%yY6f*_mD|D5**'
    b'5B5jJa8S6meTY7HF~Q4k*j^oh!tkN?>?PD;NL9eT2Fe~QV5?_<XV1}inLR6TsJ<d9KKwmRK(zpJtvfaVc8q$#3&+$MQ$%e$9dw-'
    b'}P0!LQ+aF${LkRWpxS0!>J;KiE7(u4aj`qBhj;=-PAv}O$p1G;)_JFM@3*;7-'
    b'3RQyo{Xx1;VeO#il!~8_Vio7=?m&a!<tB~fH>?F23T^~lhE!s)&l5FxlV1tZN<~6ec(3%@qML-Kx*aI}lv-1M7N%d-'
    b'f`gF9%J7a$nJ@jX0m&QmBSt8&;*yB2Q?X8vU2UWa&c|Q&JRrg2AT)+f4^c*rl`HD^f-'
    b'KJWwoK{RF``znnvFm5`Y^a&Hx8x%H62#O$^>?bc!o5@5R?+Hw5{^i!^=>C{()s5q%Qlr;RI?Wp^{IvmRQ&d&zU9d4d>7E(_XAv)S'
    b'>*_ll{1PYS;v-^>epiNr`5$A=pJ4A~8c3hid>#QrEaOz8hAAdK`OPg5L!qP>s<$3Zn-'
    b's2T$ik1Ly>=PTCKg0$Ae3KnnQ4SBv2`OFkZ#eg1pp-'
    b'+<Ob?Tn^x1EhC=U{(blSgIN%nVzoa#f!RXMsWRO#0A2bey_f52rzKOzz=U74kGWG@-'
    b';r|J7uYU<N(43b#VbJZKvvM3CVuK4C~F=XW<CxA@V42KYn1TxEt~^*g99{nM5%a@keNJ5CcUCVQE!DEB^^0uM07Z)(53?p&%hJJk'
    b'J!KtB_Qcn6P#jI8-'
    b'MR3}ES*y(hBaFF$7h>k5P##np%$Y*;4Dfq!H8UWv(YA@%JViDyxsS<a#90MG?O6U6(+wtxd^q{!at`snL#p{i>lj}lN_Q4%IhS_u'
    b'ejwiZA)&!X;?C4GBD_UL2SS3Ch;pM*!5kY`h+R{_zW;^oL^<GMHoas|6KK30_)1U>xDesPLdgn~xQW6#Y)4Q$U_tq0Vop3Q<cpcs'
    b'>y>%cp3C=993eRS%WV|q*WCm=AC)OY;h{SlBL6oSK9KsYH>@E@t~q10czI(@d_RC9^FUo5U00ew)4e2MQ7$uNpIb&N6S<_k^>!0T'
    b'pFEe5``C=3UDfnE5U@7K?F7h!k=)QYf3uu<i3S^%DNiJwo_bg73FI7&H^K4%G{GGwp1Q+j7$E0x0=RyLM0LXlVFf7cAWl_MstuA7'
    b'=I0tv9Pi^nZ>&6q!4JOrBR9g|y!*0i=&foq5ml%!fr=w!xRcYF{3%p>V092~<P5a_p$$p8dUhicd5_?J{98fVjiS74iTd5gYby@+'
    b'uRO*b+)lvVV>>zBtl`>f~Q=@6fK)p-~Z9}?|h+&r<eE{-'
    b'm*2!=h@jz|#2hj9Yl>~6Ye6a*$%H?jnUfx6|#)zHTkUPIMETJ;XcQ3OZVlmpsNQ?o(e@vxiI2A@^m2P^?a34`E~*C9}%-'
    b'iqsdS`P?jr`JO<&9C1nCd=-&sqPn7KsViLLOG+VX?W~ev0qgTFM_v6L1MFpk;D3&ws@(2-'
    b'SJIhrkngK6Nv!UkqyHnqT`{Uj0Ov=sKX2#R<)-{Cn)k{G3-D*!76#Ldk6FNbu&OPf5c=iQwO$8NLg7&wUwC1@-6V3rN-'
    b'`%6zb}uySZ`+?V}BUl{5``<yp~y4P&wTRk|Qz*ww~oB44ZVF92UwPHO*Z3!2J^p-JX$dr4h?Do5Vq=J-~Y;zeIV>0QGSA-'
    b'K32QWwyv30P5%yAdOZRQ|6o<fHyKkIru%t<9rEy+@}4UXcK}N6^AO3HPW=1RaccKm~Kgc)jWDtaorsDG^II{{Yukh3Mntkcd<xpg'
    b'~Ox9<Ks>0CyHNDU>Ah;Efdvgy*Vw25&(Ht3i|ddbnL7ByP?-vwB-uQtC<;duWD&j!6)KZ0MEE_R7wf@#D@bt1p}_V*BH>^fy&G8('
    b'38CzgPY&Hr@j+p_&kgr26lv!L0PZYu|+tN`HJTy9sF9?KG{$9g-'
    b'5hf(BLX2eN2p?`nh?)v}GX=>7|v1Wv*NkWthP4x_$(XmNp^W7W+_0dV*XsBb*1raz1C#;khoT5{qcV6U$`2pwJt&-'
    b'?2qs>{*{zgA@_+G)lO3Lt%*0a<gZ58Q%icb%+kc1}%;a0ne&W%liHZ|8j!fh4#g0CRhS=IOeyP$vL&3PFvII;#hMx^Az6JKzuuSp'
    b'{167zhmoGRLaKFYu-wH`UGs1ae9jYh8I;imb>k3=s1xLz$ZfgZH;(YjhJPgLR?4RSKl@uYz8JArVtD07DFR8Lm~2?$J=GaBpl!wO'
    b'0F{r9V2^CzR+2lkGZc9Oe$M50TAN7kYjV%m&5?0WII<JLHte;@LKcu?{<bFI5QKy3tt5)#hm;-'
    b'&1f)2SY)bVNa{6I^W~x{J*IV+W~WkkiUL~P{3K#f=y>|S=X&t@X%ozhHt8f_|l5v(j6NdEb%sL?Tp7HozS&g$<MNE;av(q3I5Qrj'
    b';!<o{#;k;(!WjJ3bZ%{8&~XTtUhmdkAZ;st_uH_^grrUlE1z+eCJY21h&VgxB_+n@m+<;mjxH@tEL`y1B`O9ayX`@XM88YKowSBm'
    b'kpTd*4=p<gf7#8Ac)l_51b}8rqiMy`dNZcE5h;W>K_=D*#;!>T}PLzKp*S}XB%icLQ6NrWu2m`=h=K~H(D{2Au1Kpg4TD4MQc2oh'
    b'?VkIosJ8^kB~6*-A$#SUP#+^+kd6hk7`-pC>UT)-!|b<Da1+i5%h{&qrpr~?2*$b`>uMz3g7f%m_uu%ulOx-XJL5fscVA7&a-'
    b'nlvBxJbCAjNU6tazZ7U9d8b4lx&KiK)1H*N4yq8|RJ%1@uQAHLP_iQut3-'
    b'UUHZ$Iq`nvswdYsbioDUk23h!S4LqBl%Z}Go3}=2`E=QQq$iS2%h-POq#d=dDHQi>gZU(O{BA}j^$G0IqrLW2-'
    b'_d(L)D7f3C>oO(5|b)8BF<k{7Ke%JQlTDL4pSDDlb&wuYcX!CqKh)f)7VMtx!u%*UNK)DD1nAp^K@oG!vu?)Z(N~6h}*zv2J@wbs'
    b'6g@V)f1`1URS}TZsrJCLB}hMz3H;^&Uv}Ujrep@>H)z9qDS#<M<Vg2T;;QbzdWTuN<7#?dvWB`<@$(>x+;H94*Rr!A(@I*v8{KU;'
    b'o|bDaisJ;l3EM-Ks}NEQAsRw<GUeN((JogVT3BC41#UY^!f;5)Y0KRt3%9AS`_~4_#icP>!&EpTc4n+R#9c!NMpM6;^&_!pCjhpe'
    b'7G7DG5%4Emku1!BIOA0VPZ`7d2yAo!GBCsGwZAV7%*A&#a4n7S$M=x1TDYhZF1+zD~w!C$iN@Jga^QQj?qF7G8oEeB^+gNVg0t1~'
    b'l{0*#zD)bq22PabK@>?cspNA~-+~VN6sGCu9g3){+{w+&f>$mAY-hrIeL!K)QO_wWd~lSn|L_TZJn^RBR~cdc)35hqMTCcdthUMu'
    b'cvd-T)I?6|Dd~7LmT_FUIVni#837L@0U&^$W-'
    b'7mBe||+b0+i<=d^PXw$K?8>Ed3p#ReO(P(NGx`=yfH>f_PgqH|!Qm3}J7fbjHthgUZyaL?zfWg23pc7qP3FALlz7L$VyD9{2JS+b'
    b'=7NP!fKd6Fd<Di;K@fIV%Kb)E_!R=I!Fo+phX7pVf%sGPkJwt|Yms=L`?{z8=hf1vhHucD#HAJ}DhW`}x-miJ-bWC?HknX7Dj*@B'
    b'$YNRg;^LLu`D7~GC<ze7@nuyq3>JkTqUVW(-'
    b's)p}~fgRP?5VO>FaH!<NdsS`r=H5yVf)2)l*0n<57{T?$M_NQmf_m9j94<}`SvV4`Zhp6MQR%X}^?F>D^N8Q5%UDNaPbE6W%?81o'
    b'u}+K>MF?kO4|R@;cMUbBJq!5{5)sj|&fDK6&b-P5e{(AEtfiT5J(WH4Puq-'
    b'{!dKCV{6M@YdSm^k_?|~M^;!wi{Y9|dQMR`atu7^;hfMH)kY2nuMyvD?H608M*qh)Zf)qAU&Qddd^<32bH;VbTwb12Q)S+BaVzwx'
    b'QLp`LbMD4EATF^MMb(PQMOH`qYa#PLjz(npngW7s{Enb(tQ`7#Gs}>xos7v<E_Ehz?69X#_MoV1jyktGVTm4gatLks$!Z1rs$pEB'
    b'QL*@~Aj>6K^t@REX?hu+VrRuIZIxOUI`QD@C5M^VW{WYaLd=<<ENPuB)tiYNoVB8+E9@V%KgOzX@8!$Aoeyu!i>H{x}raW9+9mgr'
    b'IDz%)b$UhIZji*J89*t?}N;Y4_RCPJQzF5`2ysag*e3V)5V7dfrkT0U+gr;MK9n_}+i5~bEcaGPcSqPY)_Vzl%!n}kuE=pR1dLDW'
    b'RHxx7LnnZ-'
    b'6hpSWozYiU+sl1y7*8GQX+e>CO_J$s+QW$bVylhHPfRd;`x(dxo*)e^Ghw565kOkD)#g<{g@$cB#t42jrZ8pko2Z%oYj;4e|fEpr'
    b'RPR$){61HJTkWdzP<4?Y?{6___8MOn-NkzGPsa3X1nnnVwC<9piGe>PIR*>=sh_z@c^+A~busDf<R!plo_%+UsWvBzLT3f<cd2(Q'
    b'OsBJjG%K<_#Zxsbk&6(-9d;25wdqhmi-'
    b'Z6s)`(I?b>S7HDQsVf;oHb4lcY=7GiU)%wPT^wi=~OnD{|+<R2_@JpO`{Qtv^a``%y^_@87dzKwxr}hlTfMx1F~3GW`F4zuY5|Oa'
    b'>0po>^Nlhsv?WJ@CVD)G!=2J=@~jh2DvapNCJDbv4ec8xwft}*eQtaRz~?+EVWt^=w2|gjBE%d5T{z3@&z4rlGVHyA68AkeJOs$3'
    b'Cux#uY)PpvX+c-t)M9EzIk(@f~ye`t-hpL#Wb}z-'
    b'u`hCBQbs<`0zfyBSkxrmkiqzmg+!2;62izIzZYwp+lDw1J8lj0UWEo^{GcX+?p;jdGDgcS6)e7(^UfP&X*77RKFWE9xkt;?{aMfr'
    b'Q?R0G^F5doO(pBp(C)!ru(}wR5YUs#uC#`ChpZ{7J#?!2uzX|Zc6+EomB0;Z}5F|cgObPcV(-'
    b'2cWOiDr6nV@**ZcA(LZ*uqU*c`M^$Eo>aZQa1D*L#%J<Eg=u|cUufew~*|Iw244_4o%Y?}6?F`^LP31u1pq(JAVL9r}r7N+&8zJw'
    b'P&Q#Ze5*m~umKg@*xak%SqU&{3L+s05@s)=FjGQib4AyolmOv&YR$#6=9Uei=4O>>Ory2p6?};T<iINVrgTQ39q9)xK1kv&BhCjL'
    b'<eN>Ye0VEu9Da8z7FijIFOx?sL4&Sq8v6Y}}>x6#E1}}{orlJu}N)x+~E-4h1)HT&*c&IJ*Qk&<lQ+}Q*f0_8oH<E-I-'
    b'{s&uIjY>v-yU|vt)|E|5f8jZww6+1C6v7ub`uh2fd|gPBZ+Q++>ou-I{YQStvXiEhNLUAWUDGBWmaYqkEdGVC}E-'
    b'^s3QLjs$F4WhYGu}0V3?kmtH&e8PPUBA0ePe^lQ;UxE=N6IZg$DE;X;Qx~x&qp+Qyd1uu6eB0Or$7u3=>igMV{(Je2c;V(Lj2Lhc'
    b'}b2v0D{@t+wa2^7+M`X(_r55kBPcT0!66wM@L@`gDHa4lguJdkazi&IkN%7*tgN&r^1;ve7|LUi5Q!N1BgIHz{96YJuJ~nl*{54b'
    b'Gu_@Xia_|vipavB2#}=d!)7wn&SN!HpuE3+7QjcoqtER=NkzmyrI_3Omu+3;7rmk$HY&47}s==k3nhUK-nZ#JMT06Iw{DgGy*`ui'
    b'^EIW!G75hp$%a%D7HJDa6DwP;I9mb!34%OA{(EbX$-;}65D$sq@RppU~D~&&E%oWaSs-'
    b'%Wpz}g6`EW!S2x^tA<>#%hf&Ev%>;XzT*Xm>gdl2z&J1j|-5$4yP{A;%abDn9}0Ji7n-'
    b'sOpq_&H=kji8n6F?>}$596UOqeZ+4bsk>L1nUAJYA5qKA!UFfcfI3YV94f<A%`R&{biXiz=3P0JjSBtcw_7Q0H!@gKauYH6DD!9Q'
    b')TRtH10+Jl!@_n9X+proy6~iyfi!-?shW7bz2tw@iwr@7l_0lZRzt*jDYEGnaj6ATM^8GX?m@max5-'
    b'=q7<GkI4RmO4r;I$hyX#)l<&^u4QNiCdTm|3+f<;EaOo%5G4S`COiz}-qVJECE)0N_-*H$$nN~ct6-4w(zVP-'
    b'^?)f|dfG+)^+ieSo+tm9ytAdgqML%fjwYUatCzDY5Hc$!8-'
    b'=u*Z;Ah4j5&VfDG)79!ad;t&)?|tA6Q@QP$7r5%aO~fAEGd!Z#yk<}vS1?e`Lk=4^Rr~`wm<rUhMzd!1m7G|d>qV_EI>J0*)^^hd'
    b'C!{I%>@@>g8TIP_J|w#}C6S1hR9OfCYeR>->Zz+fc~BScef1Z%bYUKpg|;1B5(-'
    b'b~7+7xZDv=*5oa$bQD>~O&ny=TRdKN(ZRNq?PRuJg+sF;p@5EYP4U`-'
    b'pl3ZBHm>Z(G`@RJU?tNNTbL>2^WX+#=4{jLoL3O8L~rUn1COH#*7SnI?+;FNxUgccHIRR^#2oAnBjYCMyFi+-'
    b'#))=H38<zH<f#Gq_Ho=x$f=vef4r`$ID9(}6<e0C8yCKQx=di|)i_@fl3M}<$1N@CSkyY;GX9KbSfq}<-'
    b'_0W7#>i2v$NB3bl>gFsNWfG)x!`nnBB9`!za)Z6(Hp?w7Dk4^>7HwY?+PmfoLd%ho-'
    b')ZMTxEV}T|9)dM94xXe(RARalB7L8`Q;%+-'
    b'A0_H(5N)5`!cr0iftX)Rp(?YWs!?jF%8Wy_PM^?0M2?OiLy9X6p#N?78z%ZlKtHOkz*{7(ThZAk@K;s1ldBP+gR*)E+D(IJb;RAO'
    b'6z%@XN}U=m<a-'
    b'D{RjT875u^YlK;t~rmgo@PV&GrEah*F8a5M=L1(kG3Teh@ts`K$Ym`7CLQO^FWj=?=6bW6iG0sEo(KvlQG_=gI?lRAJ2X~vvD7u%'
    b'f`@ud8wSLckM6%WjaM_>7Cptf~aisFQDM_l1Fjbm4ORf{@3(lIHY-krK*t9HM<o$G;sRex(_w=&qGroeVxzAQYWSXTjR3<&RocLP'
    b'PUOttlf!mt#&?YW1UN>Rm!>N=XamY_w@L!cMu3A)URN<~!@<gA+$&~RB%LQ09X-Yl|6Od7f<`fkN^9(pQknUC@vN60L(QXw>o5<-'
    b'FPdQ*9>UV*UmC!h%@O~(^M$K8Z^^{L8LN5zVZ1S@q%?nHeY#sIRUwp_5O=plFY=In=%zNXBTc%|lDMc;f>6zvIZ>cs-'
    b'IOMPzT8m*;M{UGB+nfSkfV{h)mA6=fPof-'
    b'In-D+G+8iWryI!1f?&@gayC7#$cK&+OjO(oK}?E(~ZnR$b6P(lp)y|Dom@uf!C5gRhqCb=(DacaO2ur-HLiq*!d<Cc)i{?|lImzS'
    b'Cfi{pn4a9L&Ju~Oev=71h!qtzwNLTfl|2N&aP@Z70j{<9lJ6R2<e6rOij6~2QEf>c0jHvxE8^`6ILy)vcy$CB}5KY6{s%i1y2bvs'
    b'QB=9o<dJxacDI?B=g9IhFpzB7_xspDzK5LvUV26FzEnO8Ifk(q$7wR}kSq;k~Ou|}nsIaSpc=cBYnnqEi0Rs7l;4|5Of<R+@N43I'
    b'mpC01<Zn_bA#0_$b=Z=fk`yQ}gs@l2j5kVgpqFNqPGQ01;tZ2C77UfmRWF!lZBeTW8x1#s7Et^m)Hz9HplOb8D|``Qgu8JJ*or&f'
    b'<pByF-aomDl|rK)E#;vQ;&O>De88aidGyMF}X-'
    b'wr9>kbm$8&+JP6)|rfy>i5gvEwT8UhplQ*3gL%`60RH1rC4*>R#CkouuyOS)sxp!VC&-CcA!Ya06a{yYLvmCO0V`$3d7dGm-qvU0'
    b'oG60pstINlq|SYNp6J(fDl{l+*z{@QAm;yg$Sl=0RD*pUap60(*2i6*!X*5G?t@@t4rm)3SMZT%_8BoPRA%>1e2f$aRLm&4KR;7h'
    b'ivFvXNUCH$U@lFfwTtf9#IYhC?-cSKsYLw$SW3iAaJqN>D<GGsel8*LJ~~bzCe5yA71Tf+-%%BS=YrlqD2Xa!wu_Aylrb4Z-'
    b';X8D&{vOuqn*|pUNl`pP{U}PglOWFAEFMY#eN3>nJH`s3`Ax(|DXJe~;S5q*B#&Q72$qSD8!a#8owPn_rBYov!j`KFEDPsOq`Pwj'
    b'K!~1g`PI;F~(orJ=0pfL(bN-hrI3L0t!=58hI&Dwzj_Qr0chxwourhD(Y&IHe&KlRBjiJ`{?Nq||XnuUp5dgBXRv0pGJq43*DMVE'
    b'$P#HW5UMeNTp(hR#WhqqJ4RxpaD8H55w&(bdLF!#va*bEsopxFsWxQYyFRwQa999w4Vic<L^52IZFm%qUv6@Jpj{Fztqv0y2<0xV'
    b'TC-'
    b'9(UAx)T^V0Ml{=Sg+5fGH&i>F*l7oQgjg(rMuk!1Zg6;v8aWIKW(_Na0^e|#d5xn>qo}4x<wVu9PtV#CzJMUmoL%WfS&ryeNQ1VX'
    b'wflzbzCDF}ba`U@j9MvK=m@-mzC*8$tiG&>`K<l|UMWvYGex$BAAhZ>9O$Eo<iFs{3KK+B)2POz$7^7<c5>@b>_naME1-'
    b'Dk>;}Y2hUEScIHe*zrUEeJqjV2d)rb`EMgWvLKt(l}Vr4`=)je<RFMq<J?bqHqdnkK6Zd&+gr=t4U>^b2REWqqaH8oGr*R&RY)CW'
    b'R`UVDoLYgS#F%F5^Ub*Oi{;szy-'
    b's3XO2vlGRFhEBo=YGpgVBUAw=XmO50P7GCb=!fT58Qm>j#x_x6L<&R#v3Z3&>ejS8`%<llhCpwCDDXQ_>{1-'
    b';mR(hCJ39B~>~Edk07+JXCDsqIwDn$27ZPfx3{OROfWj)Q$tsux=MZUXwQ(MgTYNNQX{jO%27?X-'
    b'&Q{WOiDuvS>6E?;D<W!lRYakH6=7BDJP8R)NtgGU>s2+ESf_)6dTg?4<{iHsSZ>w9t7v(N^jil2Rg_Zl*-'
    b'IJCU>)Cc9(Ol=l)0deODd|6gA!bLMHSZ*5<s%zFlYpgn%Am@uxm=e#!c(OJCm-'
    b'$?r<a}QWBp4U}VEl`>izVhbKYQ|GVwO8yp{nMgo3$Bb5j)FyG%fiI1{69(C{ps$dx#tIfP0{++7|XEfJis*zLX*RsZM6C~Amjp#*'
    b'GO%ZX+_TP_Do8kpVf2s8lK{)KHP?Df-U5zlwLIzC%RwqHIJ_-^L@@%A`{%rqc$#+!G-'
    b'kJvo9t3`X*B1#pVC7W*FID%7UJ~86(l>B4JOjP$?sdhZB^FR?l;|uVh~`ea1r^%pSG5F;GH%VaCnPD86;uVr_>Ts|PrzWjJp|XuV'
    b'o)|LXpP!Y(*PE{;Ug=dQl=(&MtC+WrXliO`SMV4Ur;^jhW~Flit?4+yxH(%=D@S8E?b}l<osl{BEtm?LUpoNGmVY3D+EzQ|H^7Tf'
    b'OfZ8K#aFSs7nOZtn+x?u({AGqI@FY($vOJm{-'
    b'<;KTfj{qeTaz8UnH4_ZaJs3J{dlBdjXc5x)+>NO`hQENtb}%?j+GSq9LYd{6=!8IxgLNW5@GqE5>sh*kHjbVJv47~IrL52*tqS4S'
    b'`G1WvqQJFG_RgaM-Jh`LUFdzLPT0gj!TSbWpq(f(cR20HX*GVFy*YUrKXAEy<R`(Ko@nj?|yp3th(;2C~|%FhC${`*Fy_kY#3E~='
    b')NP|zedgB+RHF|@WWmTzX}qe}iqAHxorDHUtO$dx3*s+J0P_v*7kr4s8|>cYxo^;1;)QOP?U<(+#B^lE<in``w)PxC0D+(T&)f#+'
    b'z_Wl|$V)z)W?f<th^+P2#LD(zYAZ=4Dl)CZ^!RYjcJ((F-'
    b'Zv{!PzyZPlcCXg+CJ$MGVrfZ%29V(8lF^Ys{zDcK4ngroAWNLi*MQ@YsE0)^blKI0Kv1rH+%mt&?8GTY?=cR(vBApbVeN6`Kl~4q'
    b't-rS@|jj|qH9YYJD&FC_CmRKa@S4H-'
    b'1Mx|7+#51X_rpHIr=14=hA$Vl~2^l(Yt1FPxD#o;~Ceay++1&o{sS}K{(!VfbB%RX@O)kn4I1moEuuYcp7WX7w+^NyQVzYo!>o#>'
    b'|W}0`XHn~O5Q{zClY5F1BF;^XDYuLGatHV{7+u15fHQm6Z1w5#<_#A-'
    b'XD3_KEYs#BZy8(D&)dV<DF(FHCGjIM>?G<4(s65qx_1ql-BbRS19FW*~8&yy?jrh@pu!an(4&h)XSHYC?&*h^nRfOv93Ic>L>wc='
    b'J$qSsDm?b3uPv}F$XTZ?hS6H>*I>W1hV{fk2AEjeFa)w7j=uu+uqvGX9%@Q8jjZMu5nLM^{a7fmG6@hDK`Q<opYu)J#r_ltu7OzS'
    b'CAF`O^P~Yd<=p4D^__3+hbc$da{E1tIrhG6~nm67@vL3Q<)ZvXq|4snZAN_IPq(_GfuejfvYA(W&IuodinDLBx;=&RDS*PeaME*L'
    b'V8vqPYsfk>eL|2SeS<P^v$78Glx~0r2he1E6Lrd1ZTvn2>F5AHgB8(~FW?2@TYGe<3MA;ZOIRq}%HR=w@tuA=T-'
    b'T*K8y3I8>i~7W5Wx#|D-'
    b';#`0`l%iDN?bbid7DG~=%qlo7)(9vMYaGg4N)gD@p1cvMA(^{Zqm<D8WrZ))WR9(ce*Aye`gd;V}V0B>aY!9$^#?cuLE7>GP$*hw'
    b'NSY3n>xcfW$5a3o(MayWPQ|)2X#!e9)XWmi(-xIUAh}mWseGVG{3E?f*&o*JE#s>ZIWBFRcapREo{LH9e;!apf-JB-'
    b'I|(YcC}eiZ*}Y+*<N(Ut|@i|YH@3IEC83#uy3E{(Rp!IV^er#QK}%SI9lSzdPx-'
    b'$4g#y}2yO^E^Mf8FK&`81<Ju_O<sL8btLAg&m347Unckh)y~HbA?Ip@T6)vC=$9<WUnOLuZbu6Wvf)Dg>uPYvv#6Fr#$i{vH5S6{'
    b'yPG(uW&dQ4SZF^<Y^T(CFB5X_*zBS|TfDm<rpX;W7J%X)AWFLG{Qvs!nE5{Us38`r8psu^sxK7hHm88Qb5pE#eOG!4XJC)qr+p<R'
    b')FB%XI6M)riQ+2M|K@N<yq3-zvWzA>Ro@xZj?nxscQ|Ov7_ig5_EmLiwj$u{Dpwj1W?4SD2>;nX9AZ&}QZButI>>{?X2-'
    b'2mgRyN%W0;Q=%brVrcI^WqmmeG}5vp4dEJ+$%le>*zUMDhkyap}{Gns|Fl_8+AwH~t{OqZ*Dg)IUrbNa^HmFP7SQ&7h86l?@XCJu'
    b'GEKp){3<8E;n=O{*?L>`X|&>jc$Ir?$45DYdHEK?RMU)zc1}M8jpJfNB~WnsK~!O|Ofs{&n8N=~UFF#DbyO=ju42xtk4AYXcgqZ('
    b'v_hq1ujfpmcvl8cNhl;&jNTGQsXriVLg>ut)3#U2Q6{v1kvqj+mFO=w?TQJRU34i>Zv`OI6SuF}z)e2<lUUu$kWsEtPjI6+Eczi^'
    b'`zAMwBK=Gxs*7aw{!7LeS7y=8Bh<2A!Xy5*0d4$JwxBs0`|Z4>Zk@+uJWY+y9MB-f-'
    b'}N#qz~q1=~PeO+Bk3i{<cj=vrZdpiNzgdDU(HR8`af0MQ<oQcr*vC7^MhoiE1nT{&tmnWCazQoc$PQRi8+DJ8^f^y`-'
    b'D#vUHiBxORIBAN<Y3Qn%}!WuN94XfL1;kE8VH?=?tO4d_Jii-5wvbVP$3AR7g=t*g@&hg@3{`S|PD;C{?j2wdY2<U-'
    b'Ejg~bH3$ohOap)d9yVIPK$Uy_ZPPYOY?i0Wma0%TIG=U5j$fs4vLhyoJ{P4R>DStDTnmPvg!?&m!Q#n>(dLX_XjSNm0|58^;HSq*'
    b'>;M|DfrH=YF*#*&8O*UjRnEV1=G$dC&;8h(JKA_B~=hE0eaJpDfkFnvfrOeN(TlXEr`^btPO^HPTz-'
    b'@FErz_N<S_1fh&bqTMp?EQvt!*~<JCs~dA0@t8(cLc|aWla;lBy=9+U$l~!7xAobtpB=<Q(<RZ>HHcs>p3Bsc<cL6<DZ-'
    b'^wOlFrd8$ZEv5;oo7g(z$&f}*m?2cccU6q&F{?~4j0?e|89+*1I&ZUq9@Rh(CFSYsgKBRooCF4ls?aNHZj6qNCVW}NYbv#c+a#=8'
    b'*Y5C!ac>d{Ua2Sq@?t3BGl{*<YbZL38hWnQFBA5zRw>J2+L<7`_03JK<L_0@fE++fPE<Q*`~<zO@$6HClFw)=Fgh^6y47J!gID*7'
    b't9plV-KhB}jc0zxx)}n*w!@xr&XYP47MViiU25^7+|bN7WVHeTYEt5x+CTGj-`-'
    b'EHwNWb7urOcrzp^T5b5_Igh~@Dj%J9=n7Y|5Ol@C<a+)Y{Mew%;usPY6lJe4Q_PtbHaP(^JFbFKaxXrVC&rNQleX0s<kB_lt~e_e'
    b'xgq5pR9_aoQb$}a|;x(aeL)EA1s!*@k=gr}1rqjt+RB8io74xK{_D4jX#aOQ1i`$xw>V-'
    b'gh6D5txvGj?!P6QMMdgHV@?3VQKZ(>Xe79J=n5iQ=a^*{yhwRyVXTsdf~lZ%VwzbWN%AAxN9+QFO#Pj+*9}x&{}qAaFhJmF{_QRv'
    b'$R^lgye&Z61w?sVZ$W77aefr}-'
    b'fD5@0uhrloRof*`us6V~4*hdes!cof5nI+w$D4GleI7n*G|9dsFif<91tu^ly!2HFLa97@pEFj<XBgd@H+KTS<lW{6D<q5>-'
    b'+*D7eoeRSre^!u*r2&c9gSR!kw3yq`;xN|NOeU!OS`FPDob3p~^C~b(zR~hDW!M3IL3lOY;GHgJw+4iifDo41hH{t5U>ftS#W{?('
    b'oiwLzKW~e$fGt2uc=*>C>ZJJS-Q6WgYu89a5NpLSuMpN2&#3<C}$Z}LMM#&l?2TD3kqbXn2(fB88OLP7-'
    b'2_z*;>6Qy?f}(Fjvxf?CKWNGy(LlZ9HO()oN~mjyi$;W~lpe=R$e~)*2L9GhWi%6^tSLz?ZBcsSe}X4%B`xq=Np&3<fq`wlHPjin'
    b'rE$4@ZN8Jj9$gT$0rAvjqPRCAo82LlrHDpI>JcyiBP^SMQG<f7Dyu*nOj*6#Z-'
    b'(6?EQT^1^{7R~0Ga5piiw`AD}Uv>dyTpe8q29lYorxC!)wyJM8TZ*6!KAn{6`@AXs6IT&FOA*bxBI6K2Bfxt7@|hf-'
    b'^LeL$w<zDw!M>$Ro#<^v3D0Im?^i`-'
    b'tB>Ixl{d#OO6;QGK+EWQU3|p|mTHtt!F+?C{Sp^*jLP$?qEy7Gwok&@XM@QlrtAHWSJXlh&vxO@11@M~~eb`&K{+j9A&3c!*}?^7'
    b'(9Losg^jcw+aPQvtPH{_ZzWU@`KOKn9c%CbD}$qiQM^bZ{x{Z?c!74C=b3%LKgQ@yO&?!)ALQY`-R>p-'
    b'gmg3Zt5+3?flO_<LpGI?ZhfUdoDxQfo-K43g?>_x7NdFHz+hny{vCDm`p6W2ZwJOd<;GQM&;RTl-'
    b'34hI~auQmW;?vP{G6(E)1yq8mOiqbEHW$jQ>GrxO%J>6j|L-RcPil40@6`W$~*^0*k`nJ~a&I;ElarDofe7-3m-'
    b'!qp}HKC(tgtLf@cE<U#8QIofyXi|?ARhWC$0Xe1`7!Vvkb*ARdQ3rgT?+P8HUY1oxoroO}Ll!K)y*x3GLG{8G)}$ewy1HO1gRWO0'
    b'e<yjBa5klJN0k}3?>HM_^^I4%Jr{5dOrp;O?kXW<oHOe`oh4G!>0R>bNvrmiP?N1;ptu;1;q(S~27yXu&SpJOO3-'
    b'2qD5<^>W7063I#pu?r^Y82yb=$9SnyrwV~}v(BYDlW9U32yQ0_|I#V2<(-3swoN|aYsW>B9oP1j;`fSasC`=AWDzgaoHH}wy5I-'
    b'+a3tu+nWfv0J>pr+hG<kIqpmeuCLan%|(c78=icXx>~Dpi%waLhEpiy%9a4jGW$rn;`8d~PTXFr&TzhRDdm03C?*w+D8QvgE5c3$'
    b'Y=#?o~(?mIO;>DY}}vK%Axu1JM7_mv;UkwNtmi=G5lox5R8jRVPZ+p$<O@X8bh~D`~zLoG;i{N`~j*ekyN7PH&atCk=XejDC;GKB'
    b'IPxMU42kF7FjsC%&i7JmE{Xg1Os2%_fK1s_6EVNDL823-5fVHcAa^Cg(RmbL-'
    b'?=gT4UZ6*Y8EZZ^73rHFW%{sg7ty<wtW)5(8?R<#mJI@cUTHUg3J^^nKt)g5$b(z4z!kE(pR2Bk!usm-'
    b'a1+He0GgvuvwbOdF(G=bQgN^-'
    b'm!=rwgwR;P8fuF`5l$;8)JR>$d_uQNEcE*|ivuW^%s%o?_+>Q`V}H?n+M&T*mubWfSiQH?$fAvJ%_oj*m;ImbI<{21tEd=@EG6>p'
    b'|yg*&8%Qb)fAqdHrKj{*m_)!B@|-~LLCoVt9d=yO%R6`<`=&2Dsrurz%;0XoTaxzAJJH;^-'
    b'@66VN5ULoYQlbTncwlEsf05u0gA)EOtA5|r3IiD|-'
    b'=Gw&3;efEwkfn8g!PgU$RH~IC#v6;3P^Jn%n+2T)=q}&@KT04hj!(w)bm`jEd8gb?j73w!6>}mFr2ZDX5u!}Z*@y}ex^7B9RBxN5'
    b'BJ~+m=|Gf7x<;$_H0kT%<Y3TK(JgyKX9tNj_D3z0T;CctpkhE}kVkgP0&EJ}Go&(Z|C>rkL|E!5NC)mJ2^k0V+=m)KISrhZqbe3E'
    b'!%=f_5ew?;s>Wu&mzv-'
    b'6>GqMh$G(8Lc(YFUysvBx*0H>LwhXYLsi(DCJqi(!zV{HEP_KS>M8>({$bf_Pf3&G&dY3mMIcfR<j?eC!?vr+bprDo1O?JH{`;Sg'
    b'&eIP1ArFp=%0l~T)j8~nbKpeC?l4oxb_Nr6#s5z6RcS*KX8?XEJX-Wt~g)S#%&3r#CPfSm>)l(-'
    b'lV`yUR)=g~7T>}$<fQ4+(y_rbaE$l8tc(pHW>LCV$N6#%)3j43~i)LCtt2B-'
    b'^Rvo3SE^)&TtM$abu!V`pyjcp(r)7ubq3VNUnx>?>f~phrhUubACJUMTM&l<`^yrVLeVTIUEPstP?VFVsl?5MX!)M_a;%H61Ei`{'
    b'ZdBY-'
    b'i>RQ@)&~UTlUx~y=lGXEPvj9bj=Uw6zkY`Z8CH2~!S)Kc)26*XeS#8j@k(gRRg||N}F3mpdbm}`q7(a7qim7t`8jLIOJ~b#i6x4!'
    b'Ts@bQCVRa9TEw6veandSRJ35H4s#`g=t({-'
    b'uVTdgHVmmZ}K#gakCWWd+OCijCrx&^2+@wc6dZ90q_zmM49n+aja}d;y3ZLeehFVO3vt8w!O1)hl8AvR>hxwPA90KJ)bPbbOaErI'
    b'VK%t9^u+Va<UgAr!q-a?n*u-'
    b'sf#IUGL%j(~npJuwQhK2E?nv$k?bb^N06?Jyf^Fbf6C*AoDcuhM!DG#};Pt6?w^lB`y+hAi;+h}t-F9%mN6|kv(7!qol5|wrAAU-'
    b'@ylWh?4iplVf^EbvSl&tw{1BCdxm=ZSCDPAmMYISrH5_Q>$oYI~4*UAan@}(@+w*vanLGPoRMD(DBsJeo!XghdE02F<%2@1TiY1&'
    b'c`=Nll!zbU~)d4IZUnlOjUi=pGdktPau;-'
    b'soMi3!e${!29mKbF%OD8NuvuYsT)PB$oO4t$T~)z?P+3bs#V)YYHjiwC`RM3U8A`RGaO&gW}Sgm-'
    b'!!1i7GVu)j$fI{6{2MD@w6OJ}S62MM8?e-'
    b'IJVa}(E6)d+AB0|bffm<P6U)4#fk12sZ@ssk!Kv2Ev$i8pRQ)O6D8PgU}N_YHP^3d&v5p*8f>dE2SzQ8v&c*W@GrX^~LX2N1+ycT'
    b'YoZ;Gu1>47NY8=;^EA)mQ<D;To!h(hd9D`YH8y!$oiy(|iXWEN<Q3s5hQLPBQAjfl#oiqQ*YFj}Ap6Y84rH&(go*i9-0}{Xq-dQR'
    b'C@&yYtm3EA&KF4(`tC6+=tsGWc}B7v#A)Ca-d@-!udWCNaG7p5trLrgH&y2>(-'
    b'TAWi`Csxv3@*QPU!1{YEphKR#|5{ZOaf>$}J*y~FZXo#}zs1U}XEwd2I?FsIpk))tXSO0lA%*po<{83TZtIi>B+LAu9;z!v)k4lZ'
    b'Yu4IVwxCBbKsBNTE7MDu#qONuDb@ZjKT~$O3anaT7ss9W|xhHK9ML<)0Li$*(q0UG;PU}I5JDOE}BD_xr$j#93sDlh6@jyJX<VW^'
    b'ZCX>#r8a*!?*C=4!=54h=GI24T{iu=D(&U+-ql{M6-VRN*$K%4M2!E2knkx5D(=pgU-'
    b'I!1!UV=eWEoHOAM<CvaHvmC7u5fbjc8xy|hZGZ?!N_R?3Vh(kUbS)}T^-'
    b'r3OstKe^nOHdRoX>pM3I8lGrzrqdDQH(e*<5FMmOuyJZpesQ*PhTJW~h{Ozoc{kjk3zK(*+^mYA3AKXtfzG)3*vH5V4KC-'
    b'~=Kedu_!3NN&GQ-WJkqkP_>2&$aU5y3A4`wmhedTSTnmPNd(%5iXIr&(HO<Iia3^Rcd!q%7GRbb>12F;I<KulyA>FeoKO=_%p$RO'
    b'%;%Pskr08Y3K<eNqstn(fI}1vwY?*L;MWiA3Vn#0*~FlJbpuP#?9oJ?vi1$Oh$?fR*r-btHIn_`<$)A2j-{^W-'
    b'>)I!LhmKs!sxyDp-'
    b'0MSMIaCJ1FOXH#z0?DeZ@z|SBZVytJWEqKbn+&LzKQ8nyXhrg;|isx~S(4(v4M;#y@H6GTav!nilfwy5PH8QQOsI&{0)rpaSR5Z2'
    b'$W`gUfqv$rx<(e9*^*6wI7q8hoqbiG6P3YNv&{KI=K_y)?XbAKC(gbx&)rlm!hr<7KlJZvFJz`r&(|-BOt;}YW*-'
    b'*zGn4XH$rZ*iws^}gT(#AmhnW&2<pks!6-'
    b'_z?yZIA(ip$@fcYsfDm1n^YPB#;R$nayvnvl`ZAE@`hBoMx>jSP5$7&OF(ee*&}vbhho))$ah5fLVZ_tFb(4aR8evx^U`1cZRrO)'
    b'mhE$ZriR`CHNlPQv1Q3*kZ5lAvFc@e<-&)WMUl<0-`!(3w@*!6kjp0>bJt*1l_2-l&yJ<s-'
    b'8mSHg&2}DPC659A+3CBu7)LPY>UKA#Z9CiEq|B8cwBYwM?B{N0m#Vx0H6^MvU7UainU;T(JEWQmPO!s1jM<CtZ6FGu3WB5f8V+5C'
    b'hZ&^EoQxQ1dfg_8yqhmbh1=bePW4d4I98LP_@aWIrgw5bZ?-kimmYRi)DGOhL9-'
    b'SZZI5j0+J{+G=?M=TI{(#kS}kx2Ag3)<P2;)fPTshN*(6*hEwjk?L28XSsh(T{<7wgsqS@we;<p09Jc0Z}ZY0l{Q9YM5sp5G#pqb'
    b'M5CMpsShlPbyQVR3rHe&&N|x#AYiD_ex6uGr9aq$xQHL98#J4s*^sW_2I>jLQjVj^NL{V@G&#3^B{mbCHZ<KTto^o+$)oWgk4}?t'
    b'VGV!4^<d~yCs7d`1jl818u=_qI}f$~4%N5HWgY0QT1vGHx&^vHErB59S>**9S>)8PyYX#=N%qfSMp@@NbNQ0K?yHk;K#f*+_0%J0'
    b'P={oK_IBr+Ct4;XWwgX{VSfacY~N^KD0r^lU5NV4tA`GtU(#)O)Zo#)Xmgq$qj-7_8x9hDQ>rzzfhZT$n-'
    b'r`^0cPm$SF?jSh8o<17xj1q5S0*^q{);Ahn7nEQq9jTt?R(7s2aym{K!}*+1PiI#lIamwy-eX6X`g>bAGl+Lsj`gc3NMUT-'
    b'7AuH9}M$EBKRF0h;c8P&zji*C`ivE9Z;f<}<@LIDTj{st&3XLK#79P!G*%ig3^l&o`BhuJSmE@zJ<NED`Y$zM5H<KNEew3Vh-'
    b'@Jc3}C;XC20%2=AVrtyoRbP+B{XM9}A?`qQg792?Pd$TGdoz6m$Zb{|B5S1^}FUFROx;LnD4w8zd7<K%;)SIE9T^&;F0A^}br?I<'
    b'7Ew0yB-+|Rn*1rrJcuOXDPo1y_^_$jXmV1%?Xpjp8miR18S{croW1JGn>eHYZDv&eHYluSx7Khge5FSQD-IibdZ;9V9ibv-'
    b'6D8TejtD|s+`oUzy`f(tR><o%cWzf1w+Bz?UTn$3AvMjR>5T)4qTSEIt&OhoaAe%2|vG8CxJXAFaY_2D|DAEyYAp0q+*b=I5V}98'
    b';@YA)%{F_RxgK`2UrbFaVpzgc^HW1X<8JQup&_orm95toFF#<IUG!D>u?rqs4Ci>`l^wA;siJcH+>K-'
    b'38SqUdnWNS;_gNRQ$fp$9I!dXLZ2zu?}T2&)}+byTzWlXyp)yjz%+o`C7EPAGQB^9(TwxWhVs@3ALbv0Sk(`lYv>*INMkIe7QSeZ'
    b'wOGmlOM5a9qP)-'
    b'{^wHAF|bn{XrV7EBtRexS9^sp)tvPDdqxXsj>~MBbIGkNTLP0g~#QyZXOm*y_MQ!Ax~9QFqb^#lSGpV}=iJL&qj$M^j@n=Wdb4qn'
    b'&cSW3vrG2JR~ZxsPx7kMD?TWiJyEP5?CFVo0PCaDH(FFZIqQ-'
    b'#C@=pacSIpkq2~qpZ{`3^mUOddYpsa=&#EiShY#2Ain1nwqq6fui#Sz|qlAYXMRxpaE1ZZ>3bWuMT}W-'
    b'PQ8Zya;3mik7=1+|9k#xqS;t)v#EVA!b@ekSZ<B!)B3CQ+&K?FJb%;)o)a@l0KGBH*WRl{_>+Wf>*_rZhSSDt8}PPt(vX9`F#y=@'
    b'dQ?kYAz+ActSZ(_INhebfyNZUU$3*7~-a}b6E*ZHr1F2VP={tMSxJ3Zmiuo!lGfEYxlo{m!p;jx=K|ysiIk-'
    b'Sc!}lQ(9@M!F6ATv*MA+qO3lve7A(K-G)b1X*ST_5R=nB%72zh7t}Zyg*YbK3M?xc-uo3i^1R;#Bia~8eLINv(Z?j!JXE>7ayY%R'
    b't=IrSAHvnDA<jV_K&_ZkzS4K0I967f3ov!FIs)26lbF_bY~)Yg0%EpPDc4KWaFznCTUa{m6k<(4FeUbR1jXMW_@gt51Kx|NU>o55'
    b'UZJW#6;Ba$aKgUmQVwSY_@WftH=%85+;$%Awq4Kslo}T)w;Bu6ZMJR~<i8yR96jNP-'
    b'8wb_^t6NzOPw93YHKL_O>x>?gW)hvT}X7(B~D+GRSAQcI&BCoK_%*$@CCj_O>jI60ZDTQj-gL+K;XlnFL+d4&3!i$QxDMsAEkzcn'
    b')H#CgAcBtYt>Ods^j-'
    b'faZ(mR)IFH70A1;>WAvg#Q?D5S>dw`=YRGj60HGzSNu>noPt5!BVx&!EvzN%&JfC_kB68p1Eb(4FO@Is5STpB9*kKw@9-'
    b'LQ2!P~w`yuBt>L2*@k>W5nI>clDFgB8{@CB_nBi6vQpSkwT4sT7!eR961m@P!0infF8_fx(ewHdD>2GIx=K1-'
    b'>$HEMleluSm(ajhVIYB0x{`KmVWq^S^xm^Du!+_YFaFry&eQQzXGDWvQtq9^&P`led)!2q4-'
    b'fplkRSC@PnMar|W7k~&jLj8X>JI7n4iyCIe7Y{)Dm4cfK8vlZQbE%k}^yt2*!{zfA_x)@gnZl3w;T!x&6Ie(cqY8e^7BbU-'
    b'u*EKa8Jz^A2K()abc#h7z?tqW|4UdODcpbCJizjhh$4^BZ5=|a0=J7R1Q%0!M4Q~C;@Yc-'
    b'`)?l9&Q2g5E2|p+*VimwnwnT$%O2I22UZJYD&s;7l>lRbQPUho5o6tcWlxcXw&^?pW#eUQ6-2efCt6CElZtfX^;-'
    b'Q9K?5~B5Dw5rQ0v>{*uL4hy5-'
    b'gZ(H{T2HjNRCFU8<<SVjNLJ1$a!PK<yzUH`ht|)glSH@KUxx^y<03iq<?@%_{6MC^i9;ATia&T;)9KR}VFF_jrJ4t2=M#hfbV4VL'
    b'BQ_>nO8!={!3P&`HFvqQF$(G8Sftd21ZSE%?=-'
    b'_V0{gZgE>pT}HO>e0(FqWmctRYJ^=>8sf@B5FJ$jBEs>DG!@uU6MU2m+f}|!EUI}#xSy#u6=?&?v-'
    b'GpG_S9n6P=ls~fOGq3@3RPkMYlI90z}miK+%u7wpV%u{B;rj)upeRI6FI{5prl!UikL6XhG|@iK@`=qV#_yHt)Jc;f~I{e9+OahI'
    b'yFU)<$Ji{L^2;{q_8Pgzb;!bz-'
    b'W>WGuh8*uIwh)xI7>a7@X(opl+;Zvuh@dOHK1<C<=;lWgVf`ST+|uBL{{zVQLw1;D6g&O06En?{N9eo?tJYSvQ%^lwhxRfDuylQH'
    b'hF>{qSzaCjbwS0;9Vk|GgDy)B6Um||sBpewkqpBjz)WkDx309Hj^xlPH`I)|7T6P}~{TZl;4p(mdjG_H84rJS;@9n=uWV3~E}uX('
    b'XkX`^qK`1qsw%9xw?0VR{fmEsBNCc?54CUmURvO1XXcR)IE<gjX6@%r9O@(Maa>dK<9ph*VGnJAhNsGgb{83^xEGH6s|yoo3|YPa'
    b'Y^QrFq5UAM8MYH`u?HYFLLozquh*f;3J%c=WTAW}KSXtV<_4#7|-'
    b'4)oZ~J<zp0&)H5}8bBS<my#U+tGRPKvK54aXhydH<zYCWkbelXmQ~{<z{gGC97{L7yV;LE0Dn^da?mQktQXlOFNmP&xN0>t&`W>y'
    b'u3#5f)lrboZd;Q~G=QN{Bu*5m``xanA0iAvCHZi=9v*X+k4t*Lf4FjH&f!=bPjE%OpPE~02Ee3D1Gz3>5%N-'
    b'8^8&X3<*G*2zfS|?qYR##A4344i;&L9VU6;@prIvlw+0i4MQ9u%;Z=Lk6QcENmxuk`ym|u3QJfqqn0g^g#o=aEW|{U|d9*|ns!K^'
    b'oeO<W=@cmtm!oTOcQQU^MCbNG|m)V`M$4+X2mOF$yI3C~+!~t~Gz7v!t%<sKhy^EDk`&@aVyNtv7oj$R7xtXXw5D79iQi<q>z`zN'
    b'6LSHFfp$Om4Y`TBmWE+tWYq<;D)9`-qew{mVl_#NgIKb|#aGiH|KJDn5%{YuQ+WGpg?;VDA&uno&$cfyH@c-'
    b'DVGeL*Fiy|l@1Pna+l5wEO;bWGDcp|=e|5|%jML|`!-'
    b'Q@S^2giVlI(~Ycg5Yb%MLGtJ3UXpP1F2DYa9%lo!s`EWx!$y$c~ik*6Nqjqw{9v8ZR#J~WJb_Whm=dP%LSQCqJ{I36lEsqim{6_o'
    b'OXvCZ9&$;6pEDn-I>z!l@!5C82EGY+NIs91RJ|u^hzGK+sm4GF>@1;IgaEGD&WWKh;QA&%ufDk-'
    b'<A1*{Ch(yh8E$Q=$z+GPyj3PQtNpD7u_;n!IsvFdG8hf=%jhL0n*`hm%b!Z7omkHyADprd3RnGV!7p(E_qV$HnDpD7{0qQHz$+GU'
    b'~Ul#!~rHmpnBwx7qO7N1aKCT+^U&iJ}6p8!R@^)_qngrbN>4Qr#D1c'
)))

def _is_floats(value):
    if isinstance(value, float):
        return True
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(isinstance(item, float) for item in value)
    )


def _framed(payload):
    return len(payload).to_bytes(8, 'big') + payload


def _stable_output_bytes(value):
    if value is None:
        return b'n'
    if isinstance(value, bool):
        return b'b1' if value else b'b0'
    if isinstance(value, int):
        size = max(1, (abs(value).bit_length() + 7) // 8)
        magnitude = abs(value).to_bytes(size, 'big')
        return (b'i-' if value < 0 else b'i+') + _framed(magnitude)
    if isinstance(value, float):
        return b'f' + value.hex().encode('ascii')
    if isinstance(value, str):
        return b's' + _framed(value.encode('utf-8'))
    if isinstance(value, dict):
        items = [(_stable_output_bytes(key), _stable_output_bytes(item)) for key, item in value.items()]
        items.sort(key=lambda item: item[0])
        return b'd' + b''.join(_framed(key) + _framed(item) for key, item in items)
    if isinstance(value, list):
        return b'l' + b''.join(_framed(_stable_output_bytes(item)) for item in value)
    if isinstance(value, tuple):
        return b't' + b''.join(_framed(_stable_output_bytes(item)) for item in value)
    raise TypeError(f'unsupported output type: {type(value).__name__}')


def _output_sha256(value):
    return hashlib.sha256(_stable_output_bytes(value)).hexdigest()


def test_humaneval_plus_suite():
    candidate = eat  # noqa: F405
    for index, arguments in enumerate(INPUTS):
        output = candidate(*copy.deepcopy(arguments))
        comparison, expected = EXPECTED[index]
        if comparison == "sha256":
            if _output_sha256(output) == expected:
                continue
            raise AssertionError(f"HumanEval+ case {index} failed")
        try:
            exact_match = bool(output == expected)
        except (TypeError, ValueError):
            exact_match = False
        effective_atol = ATOL
        if effective_atol == 0 and _is_floats(expected):
            effective_atol = 1e-6
        if exact_match:
            continue
        if effective_atol != 0:
            if type(output) is not type(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong type")
            if isinstance(expected, (list, tuple)) and len(output) != len(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong length")
            if np.allclose(output, expected, rtol=1e-7, atol=effective_atol):
                continue
        raise AssertionError(f"HumanEval+ case {index} failed")
