import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[7],
 [-78],
 [3452],
 [346211],
 [-345821],
 [-2],
 [-45347],
 [0],
 [2368],
 [-111],
 [-2468031],
 [1010101],
 [-123456789],
 [-590],
 [125890],
 [444444444],
 [-1111111],
 [-222222222],
 [-591],
 [444444443],
 [444444445],
 [-222222221],
 [-1111110],
 [-592],
 [-222222224],
 [-222222223],
 [-7],
 [2369],
 [-2468032],
 [-112],
 [125889],
 [-589],
 [-588],
 [-123456790],
 [-593],
 [-2468033],
 [-222222225],
 [-222222226],
 [2367],
 [-110],
 [-113],
 [444444442],
 [1010100],
 [-114],
 [-67],
 [-586],
 [-1111112],
 [1010099],
 [1010098],
 [-222222227],
 [-2468034],
 [-123456791],
 [2366],
 [-9],
 [-123456792],
 [-587],
 [-1111113],
 [-2468035],
 [444444446],
 [11],
 [-222222220],
 [444444447],
 [-109],
 [-6],
 [-585],
 [125891],
 [-93],
 [-10],
 [12],
 [125888],
 [-115],
 [125892],
 [13],
 [-48],
 [37],
 [-97],
 [-94],
 [-92],
 [-98],
 [-11],
 [-1],
 [36],
 [2370],
 [14],
 [-1111109],
 [15],
 [-222222228],
 [-123456793],
 [34],
 [-16],
 [35],
 [10],
 [-68],
 [444444441],
 [-1111114],
 [-69],
 [-222222229],
 [444444440],
 [-15],
 [444444439],
 [33],
 [0],
 [-5],
 [-2468036],
 [-1111115],
 [-53],
 [-358947934856],
 [54837398243239],
 [-78653034582],
 [-1021021021021021021021021021021021021021021021021],
 [-923456789],
 [9876543210],
 [246813579],
 [-1234567890987654321],
 [11111],
 [-2222],
 [54837398243240],
 [-923456790],
 [11112],
 [-358947934857],
 [-1234567890987654320],
 [-923456792],
 [-2221],
 [-1021021021021021021021021021021021021021021021020],
 [-2219],
 [54837398243238],
 [-70],
 [-71],
 [11110],
 [-2223],
 [-1021021021021021021021021021021021021021021021019],
 [-18],
 [-358947934858],
 [-2220],
 [-1021021021021021021021021021021021021021021021018],
 [-923456788],
 [3],
 [-1234567890987654322],
 [-17],
 [-78653034583],
 [54837398243241],
 [246813578],
 [-1021021021021021021021021021021021021021021021022],
 [-85],
 [-923456793],
 [-78653034584],
 [11109],
 [-8],
 [-59],
 [-19],
 [-66],
 [-923456794],
 [-923456787],
 [-58],
 [-923456785],
 [-2218],
 [9876543211],
 [-80],
 [46],
 [-358947934855],
 [-60],
 [-81],
 [4],
 [-1234567890987654323],
 [246813577],
 [-12],
 [-923456786],
 [-1021021021021021021021021021021021021021021021017],
 [-358947934854],
 [11107],
 [19],
 [5],
 [9876543212],
 [-1021021021021021021021021021021021021021021021016],
 [54837398243242],
 [-61],
 [-14],
 [18],
 [-1021021021021021021021021021021021021021021021015],
 [11106],
 [-13],
 [20],
 [-56],
 [-923456795],
 [11108],
 [-1021021021021021021021021021021021021021021021023],
 [17],
 [2],
 [-923456784],
 [-65],
 [1],
 [54837398243243],
 [89],
 [-64],
 [-82],
 [-63],
 [64],
 [11105],
 [90],
 [-358947934859],
 [99],
 [65],
 [11104],
 [11113],
 [-83],
 [6],
 [-62],
 [9876543213],
 [53],
 [-84],
 [-2224],
 [66],
 [11103],
 [-358947934853],
 [-86],
 [-2],
 [67],
 [-35],
 [-1021021021021021021021021021021021021021021021013],
 [-2217],
 [-2216],
 [9876543215],
 [-923456783],
 [-3],
 [-57],
 [-77777777777777777777],
 [22222222222],
 [-33],
 [13579],
 [-2468],
 [2147483647],
 [11111111111111111111],
 [-11111111111111111111],
 [-2147483648],
 [9876543209],
 [9876543208],
 [246813580],
 [246813581],
 [-1234567890987654319],
 [16],
 [78],
 [77],
 [76],
 [-78653034581],
 [-1234567890987654318],
 [75],
 [-2225],
 [58],
 [-78653034585],
 [246813576],
 [39],
 [246813583],
 [-1234567890987654324],
 [38],
 [48],
 [-21],
 [40]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'rlnIg%tx5r#p4vmjxy_!6N#jRPPf#A;9H0!T<B4)^8Dw(eF@Tu2*Zgt6|fs>n$9fAh%t*Ps6L_rLw&<KI7i{^iG?|M~kUYCnJcHt'
    b'j6GQgid((?0c{q~1oBtWA$>%hjr@YFT~nmFlVDzS6owZO)(n{`vbKfBaTvO_JJ{vrg&4TgNEZtja96CfD4iyWc)X+tqw17jfO~wx'
    b'%nmuVt2T)!gN@GW)2zkA8=6QBjr|diQFnS?*ohI-LtHtF`r`W34Tp%e1B9TF<!kx~?>n-&Dkg&U??YvP5dT*K-lAx0IBxt-CbmmB'
    b'e!FGA4Q7GMie>a%7d}GasGQuUJ2+Pt#-'
    b'+ivs33Tnfc+`Pj{tsp#i2eJsoQ?(C`RFlk4VuYQlzHFO<%w_8ipJC&NK{FwFdfizpDNGWzV()2;cEP39N*;MDhZKsYyQO0ts*QCz'
    b'28qiqlG%cg1ec9{n?W<FDQ^9g>yQ`l)xxlnVgDq)V*-'
    b'shNvz2O1oo1xjr8ga|X3f{lKbN_@L+;I4%GkN=qP}_ko_WEs7B6+Ol~lHjA?HY1>eF%pT}^WR+Ra)v$0|DwD!I1{7cBiu9Xif~Sf'
    b'IxKO@@tpc9FH{`&QO;`t!NWl$qIIt6I6ff#sfB-_@5E+oefsH`xI`r3iJawVq-'
    b'!`=OLN_UAIIjCQ;zi|u8iIY~*HtB*D4GB?`Gr3L)Opf0ai9_h?dx&1R*EQ<3zdS;)quj%Dkw6=3or?aeEVdgy6N-'
    b'35)9gr$0L>BYihWIF-%cM0x5|^a(*#}$jv&DD0U16}#bDmXewx`YuI1MoAZBfw;3SxH?1ivP-'
    b's+}amTXBld=0OGvt)jc%S*3Afx!(3cr9`j6E6e~o&F(9gxz_yhW~%X&0EEJzKDQ~3kx-'
    b'Uu13K91c*X%!>88A<7MSkHQ7nps8Xi=eDA$a!ySsbASM#1d!KY4b+gdET>$uud&PR-Dc}26fpuy-'
    b'sNrrgSHnCUgO%!fu&RKQuwuEvt-BpWB!JFLmxXi0gaW<_nPb;N7y{=7+0R<K;>F=_;ATk6|Gl&d9xC!c1P;HDoxBlEzMLldcJ~J+'
    b'mcD0eR-X(Vs)GqH!cL4Y&du>6H+*=LS;-Ih}M9m<d3d(*#or?1C7-'
    b'#5i##TjTrK?*g!Ib1e$t|UMsnN3KA2flIdrqL+Z%a@G;>_5YA;^5+mC}Q9agZ|v$rcSwr^A2dQ6^4pho;J!6l2v+@lSyw>-'
    b'fH%McGPeqwJ*&r!L~J%zi-)51PZHBpsQ?>v*wZZkQ`!?Uc=LRnY-Mo=2&)gq=w_LmMcflSoz@2yJY`qfV28e5ygo)@1uZqrETlLn'
    b'{^%gcz*V7Q(8_X%4_d&(I~~Z5cB;ZPnmeGbUaKb;==<T*Y~j6@u6!mmLX)GE+6_vgD5>9e$#?soL$muT{WpDK{85za;#EmI<oOFL'
    b'_=Zw40zL`YzWD%6`8j8KQO*Bcks*_Y11cyUr+raKoi4J5);yU(6RuK)0vRy-'
    b'p*A?c~T9Dq6>2U=;F(`+OW9Q{OXKD1wq`kTV30tU>cslxyNfwH5-'
    b'Hx9hUI2&p^|W8BQQq{9%lvaK`dMM^e0<8MoBlI(ZC8P24<vI2o#`$l0w>5|K6x~HFZ4RTu7Ln0sPIdMo_sMRMLdO34_KOWs{Ccp&'
    b'p#_bG)^Z85B2LbF;QE`Y-Qib!(-nF;Vm>3u{4txA|%|6h68kN}#-'
    b'5s82gLX~R3SfTtSyP2g{b6{1hH7dLiVA{3n2w#parUfpAMU2muG6wET9Z<{gn{%N9#I<tG1`$TTQV-'
    b'1z$cnD#tA+ZFqghho@cfCh#X8mQ#;!N1%O}DsMV>?xke|Ulu^8DrMH}#el4S@@M<b!_Dv%;8h0u;brbYN{4yw?t0Ieao@TNc@J8C'
    b'}vb>e~9ZWKR=sF7q%}!EVdkVQ}TmYjoeaRlM4(!(Fuwdj{+cQG|Fk=$=o;6FU&V5WXX2dZc4SVWzC83kVuzCRfKFa61P1G}!26*u'
    b'?ta)QgjPzfuaPHd_$&l7lPs~@jH<I801ZyrB1Tc7C=O^q7rZAWlNcHVg7?aP|GVs+gYAHwhc<iB#HEWSMD(+VOKI~_kh7GsdFUoV'
    b'TemTQ)R@l|J^TCicQIm3^W1bn`dMepn@*+A>F(2sp-0+Igc{?UwTWoEDPTKl&Bsx<gpiBg-AYX&VViD&Qzw0pGvb`!w6%n#rN=K!'
    b'+NeWJ}VpBSLMn_p0SKRs`=$YC1@fMIva=_Nv6+EB`UD$=!luJU9nBA?uGC~HSIH=(bJ07N3FCA0^ZO*a?!b%joiy}`Qn{73(-'
    b'O7^!#&b7wUZYGJTjC(s3{t-!yTcYX(F3oY-pJTQAb2ncVb6h%rwy5iw7Hd~#8jALAIELg3n05C_z*lswt~n2v->4-'
    b'l7QEyJ9<46%I=~+JB#MYnyJqGgwrlNmqDTj-;bxFjj=)z)Tt;Djp0<#I3E-'
    b'tgVZl*f_c{|WYDQVP@)K0CdwIJ6_ZefRUd$pYT!Yl4@3BDDO)b#oYXAIj0l`y+8Cgb=zbD4030d!7$|6&pj;fan;6^#2}RI!_byH'
    b'a*<DbCjLLp72J^0mCqYLYL4h{tRN$9<=oUnVps)VFE10}1&<2$_h*R%6*$;AtsO%RbqAxp5dRO*))lEem^aeRYP%eJe6X+oI3wm7'
    b'fuCO13;;13<RURI6wE8lkc-7<^gyMHS^@w`T5c6Q^UB^IC2X;X*DW>6L?pdc%2Bl3&>aBasMM&(VbyeoV)-O{%1-'
    b'pv1lv;cqClvPzXTESlXkVMgcBrm?z3rPegQWnThfLh8w&e_*`}t~Yg@E&FHrH09jM$rc*VB2zt3BuIaQ9qWX1N)C2P98m&&pC8Pu'
    b'InLc2L{r^F3}EIT2^eTCtr9T88eXEC#Y2W~Mu;*l0Bs&nCV5L@``kJ8!$7nX*DvM0ij=^fmUxB&fu0q$jSrCHKqL@dZhpN$}WI2Q'
    b'-R2%rp+HE;*;dXC2bdTf3dCv11u{q=wlCs#D2(s33FmY;Ks#?aSx$%{v%WkRj}|p)tLzgI(0@Isg9)p8q>u$2`{zI(81KO^|E8tH'
    b'eQ^ih3R%^j(3Nhy3q46?o5X&R_ov>5xas'
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
    candidate = even_odd_count  # noqa: F405
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
