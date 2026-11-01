import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[5],
 [30],
 [8],
 [10],
 [33],
 [49],
 [77],
 [91],
 [99],
 [6],
 [90],
 [98],
 [25],
 [21],
 [48],
 [20],
 [22],
 [32],
 [26],
 [78],
 [19],
 [47],
 [31],
 [5],
 [29],
 [-98],
 [-37],
 [-38],
 [28],
 [18],
 [23],
 [-92],
 [-2],
 [57],
 [-99],
 [58],
 [56],
 [-1],
 [92],
 [1],
 [-80],
 [34],
 [-75],
 [-100],
 [-95],
 [16],
 [-94],
 [17],
 [59],
 [-7],
 [93],
 [-82],
 [-15],
 [-81],
 [-96],
 [-74],
 [2],
 [3],
 [7],
 [97],
 [42],
 [-101],
 [43],
 [44],
 [45],
 [-56],
 [60],
 [-55],
 [46],
 [62],
 [55],
 [61],
 [41],
 [40],
 [-57],
 [63],
 [-102],
 [52],
 [-72],
 [-97],
 [94],
 [12],
 [89],
 [53],
 [0],
 [8],
 [64],
 [-58],
 [65],
 [-71],
 [95],
 [35],
 [-70],
 [96],
 [-59],
 [15],
 [-33]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'rmPyAc8*5C&ikv<NFOa*hQSHoHa)7FgzT8!$4u@T}AZys?IJ9A|zC_?UgL!2R%iopzsfUC#6IHYr73=CKY`hawzpAg{$N54lr`A-'
    b'CM36R){MA}Pk*J95h1u~7?7Ly+Q^$1?5bF|{h(Q{tKfd5cLY<rNY2U25>Xu%*a3abs<wQnd!vV2P}*yKKvB6cm`R7aT#M;K&W;4H'
    b'#U$C^)(p?FR-77%*V)*Tka@448i%6gZm54RQkp%x@XHyaDd2u&M'
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
    candidate = is_multiply_prime  # noqa: F405
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
