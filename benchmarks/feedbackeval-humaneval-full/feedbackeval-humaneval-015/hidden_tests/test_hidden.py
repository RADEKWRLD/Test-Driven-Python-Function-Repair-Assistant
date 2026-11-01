import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[0],
 [3],
 [10],
 [1],
 [100],
 [500],
 [2],
 [99],
 [1000],
 [10000],
 [15],
 [20],
 [50000],
 [49999],
 [101],
 [50001],
 [102],
 [49998],
 [1001],
 [18],
 [37],
 [36],
 [501],
 [84],
 [16],
 [10001],
 [65],
 [19],
 [66],
 [499],
 [83],
 [21],
 [98],
 [97],
 [17],
 [82],
 [22],
 [999],
 [67],
 [998],
 [50002],
 [9999],
 [75],
 [38],
 [498],
 [502],
 [96],
 [23],
 [50003],
 [9998],
 [76],
 [14],
 [29],
 [49997],
 [31],
 [85],
 [9997],
 [77],
 [503],
 [103],
 [13],
 [30],
 [86],
 [997],
 [1002],
 [35],
 [1003],
 [63],
 [39],
 [12],
 [68],
 [24],
 [1004],
 [3],
 [4],
 [95],
 [78],
 [5],
 [25],
 [28],
 [50004],
 [104],
 [0],
 [40],
 [9996],
 [64],
 [74],
 [10002],
 [94],
 [41],
 [105],
 [32],
 [73],
 [81],
 [26],
 [72],
 [6],
 [996],
 [42],
 [93],
 [79],
 [1000000],
 [1000001],
 [1000002],
 [999999],
 [1000003],
 [1000004],
 [34],
 [33],
 [27],
 [999998],
 [1000005],
 [999997],
 [87],
 [88],
 [89],
 [90],
 [1000006],
 [999996],
 [999995],
 [1000007],
 [7],
 [43],
 [44],
 [45],
 [999994],
 [999993],
 [1000008],
 [999992],
 [62],
 [61],
 [60],
 [59],
 [1000010],
 [999991],
 [1000009],
 [1000011]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO+JF;cFZHDc@PBagfBNYjPuS^qh0Ps=DH33DAZg@3ceK=|^X#l#xt?tu%bCJN0|G{<s`d@$h!~gup&wu~-`~Uv--'
    b'+%eDNo~LX_NRJv6uo+fN=a?nRL>%EY)GEku8dP;S1D!k(Yx1K^SY(Hrkdv8|Nr+t|L1Ri%4gg&J-'
    b'43rIa=I$si%AOF;lKpx`+?C)^z5PuD3i!EuMDwdx!s8W|g{Y%T<r}lhjhGB7K#dvNykVskc;@*IQJVY+GH@$>(f4b87vy%v~%~>h'
    b'L|XBtCR*<x}bGTJxDD-;sx}<~n-amRstJP34<7tx0*y44z9FPOdBWd2UKQH`&Ek+I4HHRKWK((_V6xR`&H-'
    b't(CQlj`3@m;@&DnWar|1Y$nPud*0);eQPNkO8xX)%GJWRcWcY~X??UzdEPQ|I9HlOwRSpimw7qv$<MMaC(k)k<;PQxj(M9Voolkb'
    b'#M$H>O7mGh>M+Tcwaigd<*Sz><kiY)Qunnz_g<85-+o5cPJ`RkdgrfYQd&l-'
    b'{4|w59ax+!edKv|%Eyw;#0hq4GH9CW_EXq7aL8lr{TiNXr!*tlnG2g?=UOsPzS3syTEtA!Y;){HRjbssb>GxwuVnH{yuf4$7-'
    b'(kW&3u(16p=nq?NqGmF3l&~DqTf;@~QcDJHTYG_G=lN-EHK~XKJhU@FixzO1d<HeYU<^PTK{bu(D2TG;yVz7c)~HZu*f+DOx}4<m'
    b'Po3P{*Fz;ro>HtgKYGq`rOk*(`M(fbV8og=fEI0z|FPvS?&41&~mcbG5TKU)q2?9XozwJY<jJdI7gM#{|}|;VDm#S@M|U!Ei2$d8'
    b'I7NXP>?I*uAz>N*Z<&pxYo~fo1lz(wnK=cXA-fF%L{J=SbyrXrT2x8_QhF`RD-^0Z!SM4-'
    b'OmJw$h#TYnju>sePZ>8v{rUm7aU=H;p#6&mIjrsh)F++1_&&RtE#US9<oANwU%^YxT;2FRK?^mF!HjLkT{7UI;4FwQR%I6_a`3wo'
    b'|95<^5}!HU`}=Z-bNaoqgM#y(a+`nTnk3C*R3@4!x-sChmG??B--'
    b'Q^PyN8<41!N1JwoS@f5mYi9fCDtF8fwm_VJ9IlmTw+JIA<+4{Fkr7WW^vwI4K7-LS6#G=L&q*iC^p2lu_H}?y$_`zM-iqQ)3`LSQ'
    b'|k>E(sLQ892wIrS+W1j+z8Z%of<3*PMM$yeQX=|zES~&Y__{ybK&z%ag)$GofU=AG>9vw*)5P@SW2f}Jg_dq(R4kuMk`erIo$up>'
    b'>LM=ni<b!txJ*P@B)}&zu(*zPT!#6ibo8xpf%J>APyQZM|vh&^OfFMF(2F|pz+C7JH^+7FzL;974zTCcgX_pb~`@>E5t+U*v3d~@'
    b'L)z_Q|N%K>0h0T4!T9<;~tZ2^hZL|V)q|o1?N}EDu5Ap*g@J-v*g>iJ~j^iC&w`xWq227qta8>K@EMwI__UoOoZOmjY-LgQz=hD^'
    b'H(lm(fq8zqh#a)>sHqovh;m}zYOft`}W%gNX6&9n_d1n<EN@~5*;XRI*qCAWB_%Ssu22o52QfoQyuQtr>57a~47zl{44MfM;-'
    b'dsSV(lnoqA75k?$bil^U1I1?8;?X8B(~S79;kuRpum9^IAq#+dWXLXvS}Qb%2PjDMcX)SMSY|{xq~E<_5*s+6&k=Ja2*AD+6zTXM'
    b'WK%gl6Km&-Ept)9BqX=%pOtXRvRv+-pvy$fT(xjIR-!)jk9<zREyme&7(^Vo?Jf)R@hd3;@jKC$Mm~p8hSCE-42-'
    b'ufVC)Xo(KZya~hXXSekZOnSD6QC~p~L?aV9zQ21>J{Udx}WR|nWrE3@s$An;Ya%|4vc9$%c7+L)sg@6|XwU&hyV5PC4O-'
    b'C0?l_NF#-'
    b'ANOECnW&E1|<V2Te)#qe>#P7ZxC9Gnt8^qDQ$yDk@SO~sbljOXr19d%86Ke?2<qZ!&cWL3Z#wBv17!9DaGgvY=~Th2lJ<}ALCq^`'
    b'n1^VZF4UgpmK9xf(E?Z0D`nJVPze`cywJX*1}JWPOU03?wm7BUB!sfX)KKBDV%!GM-*lCunUY|co@5&pI*7N-C@a-'
    b'@Ua>wZWs%MY>zrw=G-'
    b'$dRrKVcc*EXUUoZm5;4dCmE&@*dmhcy<S~bPg8=yu}XM&y?D3~7u`1mFo#c+Zv(9@{kY&c{H(>eoIk%uWLA%98?AM*mKqGuheIYx'
    b'g(fz)$`Q$k^q)U-6uEgi1BN`agXjsh>h4$%I+$Q=9IhOE=R{oprRkTL!*%%SsngoFT4H}>}qn#WleM2vlcm)kal%c$3nElwZbh+-'
    b'u)FQ_YZc;OzVpdns#&u*eL?#D_;`&Y2fW!!Kw8;8h%mggvBfXJOr%F0jxTJP8_b95ACz`lv!h1g(;8Xj<aI~AtLgNkD9(^F08ol('
    b'Oqp<c4X{j4*CC2x^?GHoYs%p&jt*6zkf!673uVZ!y`hf^)1O2P;Y+K34yBjBr)5iaa(b|I%=iyS)zH|2G)@f*;FM_iA#0OCcQu>;'
    b'5jxo3t`Z7acBR0Gq4Mq~)1UWkwZ#nTzJAGM)1>C<oq14C2N3T`DO;Sd|0B^?N`XcW|H3Bj7ULR>48os8ieg&^0<vykEJ62t_V6;Q'
    b'jepo1xg0)pm()v07oD#0dlHi3`e)I1y@<oGXgw}V7rSJChjyW;2}rc!N$AEMcY#_Taj1X8g#4aPZ$8d&}s-'
    b'Z$Y#BL;S`jvxZv5(*;2U9(|ov8A1OFmUX4!ukdoWRlE4*WNH-vM^i_|AxUVY(pcZWE>I+3OPVN)1lh<y@VN(N#r8W!ispvZ>GXgW'
    b'9QN>jJOE_5IcZ71Z!j{Xrk~J2;(#oR?uu=Ou|%}by(~14GI9$=piwyi;_Z7ph<)|h?dg;ZKSXvxDgJ|zSmG-'
    b'g;6>P#pnH$7z)k~dUhFW;5&?r+Twe;S)OT&;Z*T(LJI44mDG+}RJ|bm?S{!FGKIqyMi{jlX@<y<YzEAT4s@a)k(vR}8zM5-'
    b'0arMWX8Yq}DBbYJw3}%{5;rYl!SJVm7|_BLs3W3sAqFLcf<tzSTRPa@X9X&K1D=>_=mEEJajOjzb4ek1g8~0C=P+2SSd|DCxW|fG'
    b'6Zt1J`fHg<fD$X17g;gBki#_u1)K}50(kkysKQDq3I~KRg?BNZ33Yfuh?&IP5N7EYeh+EEyAabsASpD?*HLCbigOR9$L{682DUhE'
    b'59Gtm#4Cebw!=K#1Ap&R33aqPT$U~ZVzChC0jV$?!y!sqo7R>mFeq=vWNfJ@1G_%Z{>cL^2uULH;YSi#UNMIkJ4w=~X~;~&+oo?c'
    b'@v?xQ(+rFzD#UCvFFvrL9Ed>V;j{*xsS!U3><ByoT)<g0FMqcJRLbBhasYI@LU$RcfmWA`|6~|(Q3wWH#IVzVgv=ha78)7n9SUFF'
    b'H*N+ePL8KNW5SXhER)id=mY@jATT1}bQ-FkrzV4_(F<nxEdv<vS&>L(ktb6mXh)YoF*1xbk8#f<B+wLJQh!JgF+*hWn{PA?Ph-'
    b'puS;{M04uZ&;k^+8db_bs~Oe~x@aUwA6A*Mht;i%eYA*E%MEpDYw*!jdzaW-uFBn9)i7=0{$W=_dm@Ldq}oMdTuMcy)`0Wh3uwK&'
    b'OP7QtvHdvs=-EL6}#7B~q$J5HQrh!?>hGMtIte*T822e*-'
    b'z)6b3_y|3hQ%p9|z8DJT+S>z{oVth;qo$=58Fc5Dv5gST@!8ZyAhmv5)Q3D^_kp##eU0O&ITy^8V3t1D7i<uY+ng8B<zi|K;CKiT'
    b'C7$IyZYQ=b9y2*665rFZem2*p6^P%Gea0C?->UDjcBJUQ$`619dBzzzyilCj43xbG_-XhwQd~g>%xS1RR+9&dkP(PxmQCehDfwu1'
    b'k3-f=z=naDsw?Hea0dFMt5F7AKj0uLAiFZ=jgI{=-Hc4X>=LbcAbtGUPlb$I|MySb)aMdK-aCEE*E?mi1X)Gr0%M6?lgE1oN(~=%'
    b'`w_WNX=-'
    b'Si^0SDWl6fk;RAgo=&M%J)5`_UEwhqwZPEWvz~6v}IaAs&zCK_Js%j)6qp*4Yc7M>vzn&&5ai?kI+*fD+_Q#}h|)v<~USoplr`z*'
    b'6}qz_?+Qk%KuBy`QXV{z{y{H@hWYWCjY^MVC%EBqY+1Vwjf>()%M8N5UV>ONQp@ZH@6y6#rXpuRZRURv5w+T8DrF37j-'
    b'qZD&k;HY~y+vE~A55CdkJp`|BDj((KhF@%8AgYM`#K&AZ^X2ogrg)cQEl5j~E7eB`!&~^maS}@XErdEJH@V;1Qe8@sNkB2Q4f<?n'
    b'0<I0m5o;rt#O5LIRL>k`MC|vzJ)Gcfr3kgq=H*fgag7wJZ)&~H=-KP`xwi^Qg(-7Qa=7B1L+n(DJ3Ysu-'
    b'M4(Py$T1Lja*$GCj*KIwHY5eRE3}uIF$0ZIKuFd4&zVZ~5QKmNh8U}hA%aZd8?5+QKfw&L(z33rr`6~mld`}BgD0Q&QvkrJXi51I'
    b'xu%4woq~inb^_EfC=-'
    b'F<ZwFk*O%M?nhguh4e8YfeAj5XalxCvy{j`PAhx<HkTE~rxsECkpNr%J6kU+A*2^WpAr&HUhIKq9I>`X^buwR+X6vcwW<3fSRXEm'
    b'Z0A#;EkSQq5axWjm~1)}*@*tHa+l!SRMz^6yf1cm~KEL;dPFJ#TQ|EFeMI#e97{=1>YX8K}o5Aj;Z0%q8l+d`6I%i+*Pi-'
    b'~u_W13_xvKQLHVHe~7tN<qV;-'
    b'xNJWyB!)2WexT6C%nS;h44F3}B!Sj0A(%@TAz6@G`Gc7~&n%aCJ5^B~AwfSR!j+<WN~$BkCFNWo`)ii91uQ7C$Git<SVI)RwQ5wa'
    b'}+7jYDU$KW>U)%Qg|DjU#siY=|LXt*xJgeI0j@&u1Z_51bU#Vn8F%Cj;*!7rSNz8peZx8~6??mYLZw`C1noiS^XaUK8K2l*tGT3x'
    b'jEbRUZ}p8_Gd$=9vYQ5T>Wa{cENhh%DYGr~Pm<E2oHU;&b=D6Z*RF2rNvHI}m3hfTDXhE&NGHD1xb!hbPSYQ949f7}><8F@y~-'
    b'L5n({0e(5|0q_d2VZA^C5xY!yNNU`B5}>|23RnTd!Y=vzQU*1$>xx^{!5U^Iu4A;vO~6!exykCKMpB%Hi~n{*a)c+yl5lIbokCLL'
    b'B~I8=<|N0vf?AaH!8fthur@h};DFnp1+T<2M6m0QFTi|o6uj3NavU(CTW9=PCZ|Ec%INW~qlQ~zg9PtKTbLk9+wf-xc+i%aFwR$K'
    b'NTz>ELc%o$agpz6MZr*zonV8i_8Aibm*S-JinkMlj8p3l(OoE#O?EVMcrZw0!uzD+gySF(q6<c1{en<OjLG5zJ3O6-'
    b')*$4JA+{pkuq7%SL7jA6iJu{MC0+-f_y&&V;ij`krO|~@IthrxL6+$nszhui-'
    b'P0@p6K~}}N0xZS!{jn@ux9)2L?aul7NN(;h{SccWv+NVHz;o031b_{`^zym<cG-'
    b'N@m7Opw$E*mHIWRpxbx%09sD!CV5nS<X@o=Sf5NE?Pl5sP7uZo4s|+~f9V)yHE)Fw3BNwx6PzHm-Dvjb-'
    b'2nU0X1s@GK^&X?*u+EGZQhMHKf)$>tk@-'
    b'2EqH@rucyG)mG0va_X0@Dzn*kEIaYkz>Rw}svvjTjaTE&}&B*_uU1p%F(=s@(R&U^B|g8d-{QhKDl<*-'
    b'p$wv4Vme}fEhYE&R&rbtZiH(>y{_l-'
    b't#W_(Tfe^i>MkOq1J%=^+O?5cg23lSulhYjCf#=_!q%fchWHBgquRWBrnUJ~#BVTLfGBy%wEMOHd#j(oRp3Gq%5?_sbx8^@D5g+N'
    b'U!$AieoZGwdyWL|W3u$}g0O^+8n*!_3`886KiwiUjjTsL2Yv!8emhGe195<?CXMUx=SUEABut{kLOgihkY662xk0r~N|3wa0gCEk'
    b'1{-'
    b'NcFQ;RrZrx1UILJ`@)OFledcDvO>0cO%iwU?x;|7N(5~EZR8Zg7d^}OzETXPY3aPe3OVcGhSPg<0m}LrXinB*2|nTh8i*@tg@wJ)'
    b'8hTxf&Syg1aqYCYSnRQ<k-'
    b'IAE#)wpg3dEs0cor{sY&^K?U*aDJZit}iS07AfU&)X!{l{qi|kCa#qY(P{LfoH<_wZ2zsHjl;2bxLcdj`gK(nC(`(6Peg~Z%F9q}'
    b'UYU=jj_h)poiNjI)`jEGbWch`!o@b3mAa@uC)%Tsy!B?1gwD3(R@SYTzrv<PUta$XdxJFXhj2G2M&2kG~o6JGb5Da}7`#@dSC;6O'
    b'G>^W;d(gL|;wCAB5}$=DDfhGV6P7Alf8=)8V${!-X@2?M^X$1gVAmR6~8gEMP<fo`wx<Qgr-fDxnxYqP@)eabMLVUQA*3Wj0)LlR'
    b'mzCirF17LIJ#L3}dY<2Y_y6?U#Lzw*7GBHR*NnqV<8kaS}>gadEjR}xTx&v6tWJx4k=#n>^gVsW)i*S@!9J8y)L>az6>Q5yre9hx'
    b'V_f|MMH@{r}9E0i9d;vjW=<l;%+Zit^=;ISFD&EwZTQoNr^@hcty5NcF3enSFD!9#Mec-Nc5dh;*x@)VO8ceJaKkO=KNX0Ld>ZH0'
    b'r{B`R#uxF~_`TDW(@89k(@2dDSx6zKv-9k1@$HL8h8(L%5yuH?9A#1e01K-'
    b'U1c#8t+n@Cj)lgkHaEASAzx_(huycfmb@{7Hq76_luArcY0d2b90#b`K6E<L|PdUJ&y6n~G!8xW>Voi>#m5*d#D`X2dNZp0=F0GQ'
    b'i+CY_Qlkz(FG8j`Y=rxiPqj+#E1V7!$x>Ik<-QkusMD`!-'
    b'0;Nl19_xZdR>kQA`}#FyH5ghnJ4Ac8soqz&s=kaGZuJ8H#QU=&1%c)mK;1=~+d1P#v$AXFTBhx-'
    b'e&Nsa=k_`gPuVZvI~kn(C8R%2sP_s?%MaPauuqo~dK<KF=_{qBV'
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
    candidate = string_sequence  # noqa: F405
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
