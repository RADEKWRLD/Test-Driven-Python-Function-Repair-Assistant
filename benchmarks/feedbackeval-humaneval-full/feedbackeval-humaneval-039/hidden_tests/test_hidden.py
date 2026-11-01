import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-lRZJB}4W3`Ic*)<T5J|8mAgkg%(4k+T6Jq6vrn;)mu@K}+3I-OuU!>*JsAAKv{t-'
    b'(EkzeERt#Q1tcXYhT=SN_eB0$pQ{oB9zB;NgP!pm$+hCRTy^TGAOHU0~37x{rcnm%U4x*-'
    b'hBauLzo%)G%`q?B`)*Pw^kg4eVYoYww-3lq&rgdCgWki^ayfz-EcRi#IkkKN%`s_@=$7q3$Daq$8FT_Wt~QEGK8R~VtJg<os*zzB'
    b'^W*=x8uq&FNq}RGHKo9d>tvrx+ULaSWd6D!Jr4l5B1huZfdNEN5;ZTr)$7gI-pXytn<`O#tlz4uqap4vV}%=M(J?TLr)l0Fk`3>h'
    b'LCMI^p1qwc`6_Gddk?UvRymxisPU|xBw6MuBBjWt+?4lDR-'
    b'~xL?}eKN0TCbKiN#1d~^*WVnSarwHwyGD{JFmUAO>UoUlL*I@wY>sLQ+SO{R729)5!+P+73!Ohq6OscON8c}-'
    b'fiLp)e1+I7Ru=)Sd{f6CT&%_!a6ocb@daMwMR75lNN84YdLl<}#aZA9;c@>BmyIo&-'
    b'2yO3zpsL{?nCbv0y?k;x{xN{F|Yb!n0e6~>C2?f|sHk)Hngkq1uV~DbM9GPG?l>D%ag;idkGqG|;sy*+Er^6kY`tlbci1>Q'
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
    candidate = prime_fib  # noqa: F405
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
