import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[50],
 [78],
 [79],
 [100],
 [200],
 [4000],
 [10000],
 [100000],
 [1],
 [10],
 [20],
 [30],
 [70],
 [71],
 [72],
 [73],
 [74],
 [75],
 [31],
 [69],
 [9],
 [77],
 [78],
 [76],
 [8],
 [2],
 [21],
 [68],
 [22],
 [29],
 [23],
 [32],
 [3],
 [11],
 [33],
 [19],
 [86],
 [7],
 [12],
 [4],
 [79],
 [28],
 [6],
 [60],
 [85],
 [5],
 [80],
 [61],
 [59],
 [62],
 [63],
 [84],
 [18],
 [27],
 [81],
 [64],
 [26],
 [83],
 [82],
 [13],
 [66],
 [24],
 [34],
 [43],
 [42],
 [14],
 [65],
 [67],
 [50],
 [94],
 [25],
 [51],
 [17],
 [52],
 [41],
 [40],
 [16],
 [58],
 [15],
 [555555],
 [303],
 [12345],
 [2000],
 [9999],
 [123456],
 [304],
 [9998],
 [12344],
 [10000],
 [302],
 [12346],
 [12347],
 [12348],
 [12343],
 [123455],
 [123454],
 [555554],
 [123453],
 [10001],
 [301],
 [123457],
 [12341],
 [1999],
 [12342],
 [123452],
 [555556],
 [9997],
 [92],
 [90],
 [91],
 [123451],
 [93],
 [12350],
 [555552],
 [12351],
 [555551],
 [123458],
 [9996],
 [12352],
 [555550],
 [555557],
 [12340],
 [10002],
 [555553],
 [555558],
 [44],
 [12349],
 [555549],
 [45],
 [123459],
 [12339],
 [305],
 [49],
 [300],
 [555559],
 [555560],
 [123460],
 [95],
 [1000],
 [2001],
 [2002],
 [2004],
 [1998],
 [2003],
 [53],
 [54],
 [2005],
 [555561],
 [1997],
 [55],
 [48],
 [555562],
 [1996],
 [47],
 [306],
 [307]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'rllJB}nb42JE%dlmx*3{rfE%JvApfCEyLu(>bb$kBx3`<i3SZn%+v6$aHPbkJS(75VcaN`L?I?;pSY^#AA2*I!>g{q@D0=<Ca8WM'
    b'j!d;)G$rEVKK<4Q&Jgv_^#JG}np=3W1isC_yZsP1vvhyngxl<@3&Fb(65Q-'
    b'n#&@BZyGUt{^^DI}P!a9&4@UJv|wfwOhw7?H!{!2HQ?-!Y<6*c<#n1Yk~}^ABXAk*~*MftI@JPH%kO%q3A4zC-'
    b'8Rmwag*S`zS9b)9z4;&5kk_+32ae;Vjn>dr7ETw4M#$F*p&_IO`3@B#^_+(OiM8D;lC0fVLdyuAQAqINRaafEB)B)QQwR*J!-'
    b'6`_>NSj}IJuxwl1FRzf$o2AjFSCOiaZ8#BLRyp$&fNeZ*Av1Q5JqryQNgM>3hvH~d;(MHC+#}LX2nW@QFZ4TwlgLyCy=1R<=mi|c'
    b'mU>?ksm_uXIqs^nu57g#~)Kd(PQ&(=FpPG6wPxpHyelR~CLzn=$a)nIY7}Gc{!h1b9Eu*rvw)WZ`ceIw=fcjAMT}h0a`5gn<CHDZ'
    b'AIlL^g5g3qr)$1zxVe1+ZZ^w%GMw+~VB74r+t0Zu|V@BKEjJEG)^-x=}bHq}g%F+mgXN<ifrOz%@<t2^R*xWn~z8x-'
    b'vR~brV<PPn9iZ+G5fSUx&DX>RMPU-ti4sl50uo>WM^vJ_UtLVW%V-hc{EB2I0dzL{#66zZl3Ycx0q-|@(K-'
    b'H2l2G!r=ti*?$Iuxlx*4&kT9};sYiw|KAwXIW5U6sX$oVu$Q-'
    b'<8FuR?U`kRrm(<@_&?nR9_s_R^f4w7Bbt0n6kZPt>n|Y)KYKWZTpqGyHj)VnMfV7=1}?_%A32aIW^y$DTceWxhvp@)~UO+IkXYFt'
    b'fmfa60aHsPR%!Gv^iwWWyNsSs)-'
    b'dIM2eBCsk)If#A2lEjT7C$RjAynb}p4Sgn^o3B6C9mpB*6|%y*7Dt~!)D<kX>>`j8TTNNo<a^aGgn`+v#KdWQ'
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
    candidate = fizz_buzz  # noqa: F405
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
