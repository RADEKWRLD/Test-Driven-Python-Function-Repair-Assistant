import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[5],
 [6],
 [7],
 [10],
 [0],
 [22],
 [1],
 [18],
 [47],
 [101],
 [2],
 [3],
 [12],
 [17],
 [50],
 [500],
 [1000],
 [25],
 [30],
 [100],
 [18],
 [999],
 [49],
 [19],
 [13],
 [499],
 [998],
 [1001],
 [1],
 [99],
 [31],
 [101],
 [16],
 [48],
 [47],
 [997],
 [498],
 [15],
 [11],
 [83],
 [51],
 [996],
 [995],
 [24],
 [98],
 [102],
 [52],
 [82],
 [14],
 [97],
 [81],
 [29],
 [96],
 [28],
 [20],
 [23],
 [26],
 [4],
 [497],
 [46],
 [32],
 [27],
 [0],
 [103],
 [21],
 [22],
 [45],
 [501],
 [73],
 [95],
 [10],
 [104],
 [5],
 [1002],
 [74],
 [84],
 [8],
 [53],
 [77],
 [496],
 [91],
 [94],
 [76],
 [75],
 [78],
 [9],
 [105],
 [106],
 [85],
 [495],
 [107],
 [108],
 [7],
 [79],
 [93],
 [494],
 [109],
 [90],
 [89],
 [92],
 [54],
 [6],
 [33],
 [86],
 [502],
 [110],
 [44],
 [72],
 [200],
 [10000],
 [15700],
 [7919],
 [150],
 [152],
 [9999],
 [15702],
 [10001],
 [151],
 [9998],
 [153],
 [149],
 [15701],
 [148],
 [199],
 [198],
 [154],
 [10002],
 [9997],
 [10003],
 [155],
 [197],
 [156],
 [15703],
 [157],
 [158],
 [503],
 [10004],
 [55],
 [15704],
 [15706],
 [10005],
 [147],
 [56],
 [15699],
 [201],
 [39],
 [63],
 [40],
 [10006],
 [159],
 [7920],
 [10007],
 [7918],
 [196],
 [15698],
 [38],
 [504],
 [7917],
 [146],
 [15705],
 [195],
 [1003],
 [61],
 [7916],
 [10008],
 [87],
 [37],
 [145],
 [62],
 [60],
 [15697],
 [15696],
 [15695],
 [15694],
 [88],
 [202],
 [35],
 [9996],
 [1004],
 [994],
 [68],
 [67],
 [69],
 [80],
 [36],
 [15693],
 [66],
 [58],
 [15692],
 [203]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q}sJCY^4Zj=mZEwU6KegwU@5g8x}#`CoSS+cHqwVk&%WhrLv3Se}oCt{-ebR8BxnTbT5{;z-epMU5-'
    b'{omJr{P}Nx{Of=IJ=y%vKmL|)$M#8_!e_Xp#Hl0d^TbTLPt*8ZTf$*i#~v$Q<f2>iy?6io??3<k&wu<)^b)JTIG6WabqfD!)S30Y'
    b'P1nhr9?XYtF*}cAsl)TIMQHRMGxXl;ah{1(U6!5x<~`;14rwAaep}wCps|!=@x?bhYs~Y`{&h?qT<M3(2{&Hk&xJP?-'
    b'#q7RL^v<w1%&aKY9ri{8e)6N^GCmqdA0XcRC7eyI!K|&O4RghlN?IQIddMOG0NUJPxn~}SBUX_b2PysXPMkrs&t&i7V8^x?MW#&X'
    b'z3cb(W(&NQ))*ZG#nMHH-'
    b'8;N2bCR(7?z~ykTG7RXWSTj1s@+I6KPJ~Oc~}^gOkxTq;>q)G56w%S!Ggp#yawXrt@1%$EiRmHtv1Pwz1PtIkna+;ky1bvbQ!7YY'
    b')R$jGNc}r7~@Vw_aEwzAXrNEIJ2SeQz)K;xnJ1QsZ|tlC>Eyp4*nbGhUM1LO<`UT$kul$<;H*AewCVGNILi^PWWh<`m7PU}J=>^a'
    b'>@Od%xjdd5%_s!Rsl-9kgZpd6@yK7*D0|;NJ}&t{<-'
    b'W>u4^q>q%%B+ngw_zZ3i1+U`m#^WI!Z=gFOG(DT3GhyEQjfXDEykN})0xO~>#2~E&lV}rK~C<kbSwq9ImifD*U|6=&etuAL@%Y7F'
    b'jMr)rlKY0~L=QLk>kolTM1PRLRHP6lm9s131cDtreSc1otq0lVZd%Xm~ro<*0ysNYTcU_Ol`~$#?@z#CsFZdDr23qC4JuT)I88sk'
    b'{IhVf+g%IW;H3C;cb!f_t6$?@nsB|xio2c1T;wId5CDp^JbMdNfU$pLen*vE+QMJPCQ&1dwEQXn}HK`JDZnEcu&U0?D-V!$*)1-'
    b'b)DE?WT`dK2{G&Lcx>4rq_ST}U!nW=`iaE7iT@hTWJa^h_l1ryC(IwGFgs@F?~rV=-'
    b'qHc?){Q!Re#TV`T(E8OcgRMdPH4xOl{EjLP(>D2(R@LD}6(P^HVJ)LSgrfq7rP!o;{BDHugyw~U*r|@-'
    b'okcLb8xQ1}D@B^s9k^0JPM(_qp_UP?Y6K<NwU}9F3Q1H445?#q7;Dp~}SSQXvtM;eps7{U}FsX@s0jpeOAn)F!nsC#UR8urfYgyA'
    b'VO-VJa^IemnXWR`$0z+pe?u2aTdT^C+hm)WW7#IY(d-28y42P++-hk@?#RY@Gt+~WKZmUcEeiVwk{7uiUN%xMiwi$l;hz`8yo1-'
    b'wLz93<_uLSxw;U*}t_m44gG9N@)uioyJttNkC7_&4m)O6k}3k%QL05N{Z%I`VEL~|J7W8jEj)RkJQr#o(+d-'
    b'n=O(*{#sRwv(^n(^uk{7WS6*yPaKB`#AKv4QZMVCLMgKkRZ*!^iSF8Va7_+Z7wfS5V|0ys&_<qF<`H5Ti}6<ue#HFQ6FkxfBa`=<'
    b'QUKF=?tzlcYD1q3M{W+Wf3zewI))9n(b3E)@49b<D@ylgDSO1H7F_14Do5GC3E6WdsA>J|LM6paaN`mnK01PMqFPJ(}RxM9rp7HI'
    b'=w)pXxzzQ#5nHG0qnY&?WU{VV|AR&k9WfW-d>LtHdC>>UWQGg|VN)E8h=q-5<KOxb&tHH(AICns3#zVFB-Y-'
    b'aas~s6zp3uroj`><@gu-ITc~%Hee<Y!Sgb|0NVnzPQQIa;Brhrpb7_63oA+K^xw6mbqb3_FG5{oZ^KODjqzE5IFc?2Y(%d=7GHXQ'
    b'xGc_1OyPW$2vCQ{?<A;nnLOBScW+61+%9L-4i3%?-G-'
    b'J&#cG>L9HawRv_<vt4;~vtHZDX9jsLoX^gqjFZ?6m0NEJwJE?_V@9$ZdpHEt#eFbiOjVpLk9Qu8Z2QG2>(WRhUfD`08fvb_f*E0R'
    b'KxskkZqqkpq?sF&~HoJ$)XbOS{20kWzgCkc78d8cM0$TUiV;}$p8nxvb7B&~$6t0)-'
    b'8z`TmRh=a?1z=$$q~OS#L8u!RtsFnH#7)sOmAEOIrcPnzKw;Nj*pJNl*xm!!!vv;l0qjM9toc%89&7`{R}f5`Bfy0b+}o+9Xdp2t'
    b'hGH(mE?ge*?#AubOo4*nKQvLFj6G2kpLgvf%d-vJ;3+!I$NVTx{j6h}YIAS}8^!|-'
    b'qg>_(?HJfSSd@t(RwTg4i1@&}Jh73!#bFc();N2kX(B^YG}p!za;yXJ2ONpv0{;*k7_4`~SD<Br8506~E56}b6pMV&h40?n{A{ZU'
    b'H%%6@sZ&2|PBn?>&nj_~_p^<6&K+#9!Md+Nx^XKw(*&7znIYFIyQnzoMk5y2wSttmvDI(0|1RAL@2=Pl3=4tLN;7@mdNi>FAsSuK'
    b'8N@ZQ*r6^P`^7UIYhripjiw1VO+vA1GdhZ|Cor@?-kdN+NDe#M8HSaYaoe%-'
    b'VHd`}dj}Shv(NXOaisJn)nu=m222wfnsCD)5eHT~HJ*gNVk@@0Hxflq3)Of*B&G8v^d##|@ES7!*%g-V-'
    b'V*;TC)(8TuD_JReyls8!k`0vBi{}*_C7QWWA^)8o<JjEU(XB&SMEYjphXWakLFH6=UD7*#?@9C7kfVkMg?ra)y3Z@0h0*6fL_R$P'
    b'M=<{BM#x@-TkRY%k!Hi_%%(2riTA4fAh1BX@XyqF=;|^)70#et)@T!LIVvvM1?>|aOQrS$oH7?N-'
    b'?MyC|H4cp9@LU(5IH;<)aTlSuZuaqUre)rzYHVajK`p|L<0h`uG0@t?VO&'
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
    candidate = count_up_to  # noqa: F405
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
