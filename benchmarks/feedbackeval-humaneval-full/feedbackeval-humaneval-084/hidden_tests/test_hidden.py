import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[1000],
 [150],
 [147],
 [333],
 [963],
 [1],
 [10],
 [101],
 [1111],
 [5000],
 [9999],
 [819],
 [15],
 [75],
 [820],
 [818],
 [16],
 [1112],
 [17],
 [9998],
 [9997],
 [821],
 [2],
 [1110],
 [1113],
 [74],
 [11],
 [14],
 [10000],
 [100],
 [73],
 [27],
 [35],
 [817],
 [1114],
 [9996],
 [1115],
 [12],
 [18],
 [816],
 [13],
 [36],
 [28],
 [1109],
 [96],
 [97],
 [5001],
 [76],
 [1116],
 [9],
 [815],
 [822],
 [26],
 [814],
 [72],
 [4999],
 [95],
 [8],
 [102],
 [25],
 [3],
 [9995],
 [1107],
 [33],
 [19],
 [4],
 [1117],
 [20],
 [1118],
 [5],
 [24],
 [94],
 [23],
 [34],
 [77],
 [812],
 [4998],
 [6],
 [84],
 [4997],
 [813],
 [29],
 [103],
 [98],
 [78],
 [37],
 [83],
 [93],
 [21],
 [1108],
 [1119],
 [31],
 [1120],
 [9994],
 [85],
 [79],
 [7],
 [30],
 [71],
 [9993],
 [32],
 [52],
 [90],
 [91],
 [8888],
 [7777],
 [6666],
 [5555],
 [4444],
 [3333],
 [2222],
 [1010],
 [7776],
 [8889],
 [3332],
 [6667],
 [6668],
 [2223],
 [2224],
 [22],
 [7779],
 [3331],
 [7778],
 [5554],
 [6665],
 [6669],
 [2221],
 [8887],
 [5553],
 [4443],
 [7780],
 [57],
 [5556],
 [6664],
 [56],
 [5557],
 [5552],
 [3334],
 [6670],
 [4445],
 [2219],
 [2225],
 [60],
 [5551],
 [8886],
 [1009],
 [2220],
 [1011],
 [3330],
 [55],
 [2218],
 [5550],
 [58],
 [1012],
 [3329],
 [59],
 [7775],
 [6671],
 [6672],
 [2227],
 [8885],
 [70],
 [1007],
 [54],
 [1008],
 [2228],
 [2226],
 [5547],
 [4442],
 [2230],
 [2231],
 [1013],
 [5548],
 [7782],
 [44],
 [7783],
 [3328],
 [2232],
 [2233],
 [6673],
 [53],
 [5549],
 [2234],
 [69],
 [6663],
 [7774],
 [7773],
 [7772],
 [3335],
 [7771],
 [8884],
 [1014],
 [3336],
 [3337],
 [4441],
 [8883],
 [5558],
 [3327],
 [65],
 [66],
 [63],
 [7770],
 [5559],
 [5560],
 [7769],
 [5561],
 [8890],
 [3338],
 [8882],
 [8891],
 [7768],
 [62],
 [5562],
 [8881],
 [64],
 [7767]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'rk+JFZ>15gZ5OwKy7(&Hk|AL>qBHvYVKEHZajd3N<_R0$fMXwHM$vZ~_ZY0^Yk%yzJ_#>LSnm{pUab`S+i`|M|zazkU7dZ@(@Q{r'
    b'2_C@Dcc$VmWR$j&sMf+j+!t<&4;kJWo3rs_EzUT*PybrQNOH{`mImU%q~cGx4+LJ>}>%9%J<$^SZZlcjFW+VaGy4ZJah|H+SOPy1'
    b'Ae6W0{pRy0+QJwsS^TKWV{p65eo56OOh|=RNa^PH&cUPhdZOW6jTQRCZ3hAoE<Z9@I1Py2vIw9J9@_*BpoTG1ko6=gJ-'
    b'<GkfFvS*9)4VVZK!IkKBrr+#z-'
    b'Ghco3^TMR2%T)W0NvR?%ZSID*H~O(m5yVBy$XV+G=M#WpW@{M(`1IjhM|+SXpBo)uH%3X^(5%^%!tpmgodSwOd(Nw)Q@eqGr>%iE'
    b'YqYj8ZI4Y8J-!of52zY*_eCQpC-bMMwg^y;*s6D@(*Xg3PxkIPbq8IL1f<%1b=$VjU9;@~Wz3D*k7c@$`<TI4Mi@JoqGP37UhTY&'
    b'&xXF30h4pqwXLa3X|=X&F-dL1-'
    b'z5ecAsSO1oF8{nE{m9!AQM1s$^#X|QBVsCQO}MIHWMJc1ND9&9=W?sZmwPTq_a^Wwl4U7M5cGVNgMn64wq+@MY&NrN?hh2h;ucbv'
    b'JX4U-qSaoKJU3;7C^Ye`@Qq#+R3TeKyWj_pJ9Y8+N|ZxK?80QM{4gZ-'
    b'F<>aXY2>b2J|oV;mN$cK~$@^yLmm(wCjC+irQ$m=Vdu|(I6A-tuJLVopYg5-'
    b'y$Qy2TQC#H=OJ)r|2$MKSi}Jx^sEx+Wm?x;Nbf7J8tZ|Hdvz@8of%CH_^8|$D^%Bxf~z&L#v@Yq1nN65sEPw=s4vOU~z3i;PX;*1'
    b'3X~53_UYD&_iLZ)+l^1d`VH2!>eGtP2wTR0U75uV9$^UwlQU_jaHs;P|9cS_AFhisdr&h#Nu}im?FO^n&DLnmm@caCMu9MBChTsm'
    b'}9EJPJltyJrB!aT>Hkoxm{t0&39_MweHvY?Ux1|=SaxO31AZlFMKI{Md=zyw_1=~A4)#%BJB_e>wkuC5jI5%FKW20wc1#%Gv7ch`'
    b')LeXH@I=PBLi7r@i6Ox9FlQjPJiS@@DV@7`KGF<B2Cq}UlGJbnkt$MJd(BH74LRu7zFyn!MR6{!&o(<@kY=@4mu6$IM<omwK0(-'
    b'Pp@rw(K7f?(+265z8-YJ-|tf-oZ&P&4!{@aoU|Q7%$%5ONN+>rSwFNki5B_IyE-KZVg~VzjzBiy7>1*U%<ior^zG4C07!&{u<#5h'
    b'bq9_n$O|B@w^iGzcUgMTxGUNX0yH1q+ib(L&pOX9haaT4`<(7B!4+>G;~Wf3!Xl!SG&d22M6sn8*;dhHC>nP~yD5s-'
    b'MdPk0rN3)V6%|#a@FMpsYWNIN#1BDYhN}a|5K0gH4q?1KN*@f)JKoJWxr5QX@biNasPL*+UIQiKl}o3*5H__nVM%SW!864S2Dl)%'
    b'jhsc8WzQXjF4Qg1GJ0Tfif?FZI#py_MR!|8x%gdSzo_9wGrS0!qN0lESF}t~5-'
    b'l1q@47K5qF+(GE*dcJn&I!d>L?2Phs++f%DHwKsdRRr34968(CE2$8^`WNULm8~<r0{To-'
    b'1T_=ws<177fL8SdLl1dM?X2&=8sQ^edK_!PYmS^SsAFYx9A#ArR^O_su@`!LX>aFK0vBQ3~+@wV>JOHwOsu&|m^U23awnXz3NlhI'
    b'-qz(tOvgK+&0DLuO58uyB`$aKH||S#DUP!yO2;-'
    b'JH)Y`PxJGc5>8sxSb)LYj0?aX82W8&f|o2AjkEP8K$=YB)W7p?Gf&3P6#S(xCX?u#QL&)tm1<WUPh#y(FO!{`ZoRUr-'
    b'!n`GeyFew6-pjr*(LoX3RDH=tFXUrBM_O-'
    b'y%ydDyk^#Ln!AW6pP5?m(p=+Ir%&lUjyJwCQ#BEcF=nsm?D~rvL~6s8}t(eZpeT+4w&E+g0T_$+Ye?`fMN?S0Zp4P<YDXs)8&xhJ'
    b'BB);Fe{d3(YPy0TSXr^sJfCz2=ayP$}%z#f6@>%)>f_*<=aAV-Z>p6qmD3vt+|7vNe_&@b}~RwNM%41?l1(N70`iTNTZp-'
    b'Y8J9_n1&lpMHbE2IIUecBO|`1T5VB9UR<=Bq9bcj*e^1Qs?V6b>Nct98mK6=y=zVtVe_&l&_%(dNSZ~@!)tc)t_!;&qo~ToHK)6x'
    b'sae$Uq9j@r+KSGa|9{B;KM!q1MZJqRMHhBe5whk|stB8^JBpf^^sXpS)bOfK)g0&F^<lIk+bUvlku-}sRTYzpSX^@@U-'
    b'kK$SA7<;>e*e*O<NKDiXeX1^YEepQ)F93epB_#x8}@HbV#hS^qSoioi&S=De~f?U{Z9KUexfa?DyY$asKiz$2~-j'
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
    candidate = solve  # noqa: F405
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
