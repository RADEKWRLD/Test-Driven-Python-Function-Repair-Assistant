import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['(()()) ((())) () ((())()())'],
 ['() (()) ((())) (((())))'],
 ['(()(())((())))'],
 [''],
 ['((()))'],
 ['(())(()())'],
 ['(())(()(()))((()()))'],
 ['(()()(((())))(()(())))()'],
 ['()((()))'],
 ['(())'],
 ['()()()'],
 ['()(())'],
 ['(((())(()(()))((()()))))(()(()))((()()))'],
 ['(()()(()(())((()()(((())))(()(())))())(((()))))(()(())))()'],
 ['((()(())(()(()))((()()))))'],
 ['(()()(((())))(()(())(((())(()(()))((()()))))(()(()))((()()))))()'],
 ['((()()(((())))(()(())))())((()()))'],
 ['(()()(((())((()()(((())))(()(())))())(((()))))(()(()))))()'],
 ['()(()()(((())))(()(())(((())(()(()))((()()))))(()(()))((()()))))()((()))'],
 ['((()(())((()(()))((()())))))'],
 ['((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))'],
 ['((((((())(())))())((()()()(()(((()(()))))))))()(((())(()(()))((()()()))()))((()))()(()))()'],
 ['()()()()()()'],
 ['((((((()))(()()((()))))(()))))'],
 ['(((())))'],
 ['((()())()())'],
 ['()()()()()'],
 ['((((())()))()(()))(())'],
 ['((())()()()((((())(())))))'],
 ['(((((((()()()((()))(())()((()))((()())(())))))))()())()())'],
 ['((((())())))(())(())'],
 ['()(((())))'],
 ['(((((((())))))))'],
 ['(((((()(((()))))(()))()()())(())))()(())(())'],
 ['((())())()()'],
 ['((())()()((((())(())))))'],
 ['(()(())()())'],
 ['((((())(())))()()())((()))(())'],
 ['((()))()()()'],
 ['((((())())))(())'],
 ['(((((((((((((((())))))))))))))))'],
 ['((((((((((((())()()()))()))))(()))(())))))'],
 ['(((((((())((((())(())))))))())))()'],
 ['((((())((())))()(())))'],
 ['((((((((((()))))))((()))()))))'],
 ['(()(())())'],
 ['()'],
 ['((((((((((())))))))((()))((((((((())((((())(())))(((()()((())((()))(()((((()))()())))))())((((())))((()((((((())))))))))())))))()((((())))))))))))'],
 ['((((((((()(()))))))(((()))()))))'],
 ['((((((((((((((()))))))((()))()))))))))'],
 ['((((((((((((((()))))))((()))())((((((((()(()))))))(((()))())))))))))))'],
 ['((((())())(((((((())((((())(()))))(((()()((())((()))(()((((()))()())))))())((((())))((()((((((())))))))))())))))()((((()))))))))(())(())'],
 ['((((())((()))())(())))'],
 ['((())()())'],
 ['()()()()()((((((((((()))))))((()))()))))()'],
 ['((((((((((())))))((()))))(()))))'],
 ['((((((((((())))))))((()))((((((((())((((())(())))(((()()((())((()))(()((((()))()())))))())((((()))))((()(((((((())))))))))())))))()((((())))))))))))'],
 ['((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()((((()))))))))))((((((()()()((()))(())()(((((())))))))))))'],
 ['(((((()()()((()))(())()((()))())))))(()((((((((((()))))))((())))))))'],
 ['((((((()))(()()((())))))))'],
 ['(((((((()))))(()))))'],
 ['()()()()'],
 ['(((((()()()((()))(())()((()))((()())((((((()))(()()((()))))(()))))(())))))))'],
 ['((((((()))(()()((())(((((()()()((()))(())()((()))((()())(())))))))))))))'],
 ['(((())((((((()(()))))))((((((((((((()))))))((())(()))())))((()))))))((()))))'],
 ['((((((((()(())))()))(((())))()))))'],
 ['((((((((((()))))))((()))())))((())()()))'],
 ['(((((((())((((())(())))(((()()((())((()))(()(((((()))()())))))))((((())))((()((((((())))))))))())))))())((((()))))))'],
 ['(((((((((())((((())(())))(((()()((())((()))(()((((()))()())))))())((((())))((()((((((())))))))))())))))()((((()))))))((((())())))(())(())((((((((()))))))((())))())))((())()()))']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'q}qIkFo^47CIM0=|SJ8$fSBri(bh)}`DRaO6ng*M0q{($@(l_+=IYa@d1u;4NtIpI^TI`P)z5UVpv){^i%dKfA2`_T`iBUBrHK#-'
    b'iiSB7;XUIkyqrzFDHS^$tCfdb%oUXU%nw9ew-'
    b'v?eouHK8>c<o?7W+?i`k3ZQ^~j1{ud{Dv?Fvo96H$im=U^yII!#9_B71Ifss6NzD$d7}qV-'
    b'<rwaoW<iI1>TQo%SF77{)tdXv_b{HGx|4d7r5o+LhXl2hXJ$y8gUtkO;Vab9*^H25g^jx}eGg-'
    b'<%OnR+=3J+iQ@Y0C!MLt6Y0^Hc*mYLym=?l$SM816^ZFh})q)pZ%H{a&`V@+TeP3NDkj1EKHp-Nc*DiYRmOOWi9qiBU#*_j@o>Kd'
    b'&hN+&t_1q{HKN=%*srudAJ}=Xai8^zj=pJ_bL)J!W5=(&r+PtGocRLcjG^eW8dQmv-1ot|;Y1akMR$CMa`1deU&y={<80oV+i-'
    b'PaDw7~M1j6Bvl2s7;pC_H#uGQA{>y%4|X9rZBa`;56(`Z`|W>b@*(z!7GpEo%twPN@G>qaI8v*Ak-Uh<o|+yHR)nj&%`X&e^(kL}'
    b'Pyt@Z3$Sb00qev*-ma&Lr&7Mby;_eEI=6&=^t!m?-gqXAQ2g8;MPwv}UqhLq=^AKQ!El5-'
    b'i;2cmRFKq|WkjO^i*TkWElh;z9#$N02=T#FYp{!ZTQ?`U)5b@R!ax-rY~5dtP%+y&N^Hra4yhah051Jz<4NhonXJh259Y+;fqy$<'
    b'J!)Ar?Q>86L8&hidbXG#{ehL%ew?sfPf6h<*?G%|rBi2=M>qiQ=(#x1<2&4OJEnH2g`|U+>|`GS+5*Zn*ivwvV%)#9<dS#KSe-'
    b'!+6LU=D}O4L88}LxL858AX4f<HKpAcB<g(wM`vYkxz`wn*JnG!$Ldob%ZtljQ$xW|P$2EJ3s*~kx2RprFc%G_VJ)ig9wde-'
    b'2nPb+T|4{f=BvX{*cpVCiWvrz3&q@;qIYS6ZOb*Q!enDuD-'
    b'inbl;jL#((iy@kW34y@3XIs38R$0%7}5OadjTeiMyw<?6w6ewxNKA@9TZKi-gev>6c@|=sW?X<pGgeF-=_@m{-'
    b'5Xsf}`A@;l|A7Tf4^Rep%!W7*b2EPg1=L-fN6*py=M-SCe^b<zKHcy!@5>48$udw?|dtZR#pzQZN>z?@b-'
    b'8|I<r`&bWu#3+^*G!P4d9SjC?Hjg{6JN1bT3D!XKIFK672>~d*2js^g-5~3;VIJyJ582j3VxZK5x-VKZY$o{iw-'
    b'YzjkWGqS2|Hq+?81nV-kcL-J06Ytk=%FsK^cM!;%se9=?$}aO?eRk$C#)Q0Om0di^aZ86ngQ|vOov_#^V0tKasnAg#'
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
    candidate = parse_nested_parens  # noqa: F405
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
