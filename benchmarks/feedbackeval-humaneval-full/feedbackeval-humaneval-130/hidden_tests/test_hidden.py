import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[3],
 [4],
 [5],
 [6],
 [7],
 [8],
 [9],
 [20],
 [0],
 [1],
 [2],
 [10],
 [15],
 [25],
 [13],
 [12],
 [30],
 [100],
 [35],
 [50],
 [99],
 [29],
 [24],
 [51],
 [3],
 [1],
 [16],
 [14],
 [26],
 [17],
 [18],
 [23],
 [49],
 [34],
 [98],
 [11],
 [0],
 [28],
 [20],
 [36],
 [22],
 [101],
 [4],
 [102],
 [5],
 [33],
 [31],
 [27],
 [21],
 [97],
 [6],
 [32],
 [52],
 [48],
 [53],
 [47],
 [19],
 [103],
 [9],
 [88],
 [87],
 [89],
 [7],
 [96],
 [95],
 [46],
 [45],
 [8],
 [44],
 [94],
 [104],
 [85],
 [37],
 [86],
 [43],
 [105],
 [42],
 [84],
 [38],
 [39],
 [106],
 [83],
 [82],
 [93],
 [108],
 [81],
 [41],
 [64],
 [40],
 [90],
 [54],
 [65],
 [66],
 [91],
 [63],
 [107],
 [67],
 [92],
 [109],
 [80],
 [62],
 [61],
 [55],
 [75],
 [79],
 [68],
 [111],
 [110],
 [1000000],
 [74],
 [73],
 [1000001],
 [999999],
 [999997],
 [999998],
 [999996],
 [999995],
 [76],
 [77],
 [78],
 [71],
 [72],
 [1000002],
 [1000003],
 [1000004]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO*J(eZ64TbH%UWg(`J|sbcWTuTc015Ia_XZp}nsBrhZ_gjz=_+XfE$hfL-St=`aB+Y5{`0rr|M$yZKL7md=Rbb@{olV?Y5McW'
    b'uU^;md3Bw#Q!CeG=23gu*}Kg-'
    b'w#d0_j5$U37<sqSz4djM=FD?H|NHZ|zyA2uYPmNpO)1?xa$WAW^BvNs$XY|UHZNnYe#DA)9W6<7S>vphG(XFnQB%p|_-'
    b'N<y{?eN3m7?jC)yrUCrH)ZXzxDbktg+YVD_OoO>uZ@SwRK%q<j!HfZo0`N&*IusS|{_cw=>V)Ir-'
    b'T=^&<I}+2(1o>(?@Jvvi%kHm|&EQlx7~a?xxz4Lj~-_TqQdym&ZQO?fptmB+R{wW-NFA0D2}_U-'
    b'9XoPEbOGtH~4<A=hHRj%u9qvbA3%A{tzx9a&?X0}rIY*Nz7_awTa<DS(=(s^!g$-'
    b'0b^IqYhe!m6a|sbzjwSuA}mlk<?%P8qIt=%LiLrL&`~Yqr~Rovq(Y>(3nS<8UHhwF*B?Io+>iir18j_j-9km-'
    b'B{WBk}f1e}*@jt$X&BPwQEe`c0)%^W`+Sv}c(ly@0yDSZHgi(|p!-D$N3J`<~%f_a3t*Ajy+w3QcQO=y-'
    b'j0lTK5fy)4!Gp&q>h)tPLM+q-G|V2T1RFUz!Q)^qA8RK3lj`>BoOHFKf(EnBIUd&+l#0o!^jC)!%Xojz0UR6w2EtfiKg*4DS-YqX'
    b'n}i83}~pl(osm3Q7!j@2~Xw2Q`EM1^&`(*>OjplyEo;HKYG%XUUnC$-&OK-'
    b'*BStub$wDMcEcJ{I9Q%Di<Y4$OQoH&2PH@UAM_R2gih;_|o+N?@)r5x}lk-HmxtpaP)x-'
    b'2k=#l#`xAX}V@J0g^uRjTfG+x{tQyw|g)I<72i`6)CMS)Pu?Nwz_5Y{!I9dK6?hNw;Z3XGD;^ct6lu4^{bhQ_EY<ad2>y`luBybX'
    b'|1Q>v!v{~A2z5gpLeR!GX9rW9jsStDaq7TFK@YZORI@?(9hHN!#5?%<wusZW#1>KJXv7ZxtV}qh}>sCwpXU?i^Av~&3m)CAiH-rx'
    b'tVlWWH3_2;iOq06DVqx!E0sPg|JfJD`f?vdjhTwW@>d9@qu5!1S-'
    b'}8jqb(+lx9iGW3XxW1=<<}!+0Nly^^MtE(8IzShSCa{l;vT$F*zAEv>%K0Dr;@;dJ17Mi8stJE3?UxYp={GSJnF$k#HvrrVcHhLW'
    b'k4GbD(nG~Tt>;e*BIg_XxG{mP}!&<#w-gjRu-zm_@Hjp2r!lDpFG7;4^E=v_co%7-'
    b'PISZf@lF}*A{(%pl<+WcDPn{?`%_@)ggbdQ>Kq`uBfKF^t+_Jv<s_jCjbn!q2%9Ep=DgWM4t5diSOPvJuF)zYkP7nVFLx;iR@Uu8'
    b'_=Oj=iOT2#;vIM>b5S9%i|e}-'
    b'W)+Xdw)YeLFq1rmdIYGDNlkOA|94q82%X7^NLIvo0&(AdkxpGq7_pHIcd&#rJ33ntZugrIBid7tsBUJd=8Or`DCfXY*1ff#ZrZ1o'
    b'mKbjt=)C^y7hdNzoXd7iu&R9AHHZpk?}KCxNJo<og;Dxorq*C<p6@R{j*CIVX7)+#7lqQglbqg2i)5X}Tk6M);pHxRt|@{!Ln`aw'
    b'+%cLLyUYl6CF`f@_wR-dM#9m+=!OU;!dW_u=l3Eg4%gQ^C;CV`%UKY(i+dJko>do3Aq4jQ5e11}NuYEbvHo2HH`T-'
    b'eGXAvhnRyBp@g0H7=PiglP`!ktY9RKV$_((oJ(<W+{HEo~jNv$B)gYC9I*XkO&uFh-Z(g~Bl-W_Pjq?$A@28${mny&8UXgaJWLdu'
    b'cfhv@Fvu%$cM(Q0{n+UZDa064V4;Km&+ogWT<#jR|z%AXj&})!961pw_UYSjw_*+1sc$9Fqf<BG7x|h?rGjPo@uwnaP=#*L>n%b5'
    b'JL%#^JZ2y1=kjWUrqbjuAAV8c>CO{w~jiLqnOK$OOO;C;egyv5?_EM!u}fR-'
    b'x~XGiaxSWN<bz2ZIk<m+!UL$k<NMc{7GaGgFC8IiM(KtZ>8Fn$#0MVpE^XrXgxSZSw*S{>?6Z1|ea2r3r)%OHxE|e8)meutP|Rfv'
    b'uK5qJc0U2iKg3;fErh+VCfMY+avnn6=?%pktR5W(jV^ZzIR>J=JZSgO#nEi{})Lv1b|77=3JD&|{C#FSCtZq=TU(jYj5rV#oNEIc'
    b'Qys6Nc)*w%Q(-'
    b'z6BYOOLwYd%8^kO94NL%3qowr+F=SWh8^|noo4hk7OPxzbU#)g(MC)eY6N>;MvHFEC?e{X$K>y5``ONb;x_4mOkm6`gGi7g-'
    b'y4Juo^fh`eStZcv0!6B5q9C!q!>Z0#7*0(fjEc!YTXo(gcCyf)JB}aLHkoRL<1!clY~9$p)DP?B2QscuA}2Djr_1>%EZBXQ0%h|<'
    b'B=S?W!ndd>^QXvXJA_w`N}<|j!_~B^jz=NxoA5y4AF;bKeUB?qk#B`rpAaPyu5`DUwFx(91Im_5EjPTtJ|2F36aUL0*Un;3M0iao'
    b'$*jMkr@B6_bPayu-O2qJ9NH`3NsL?!8EW5igz5PY7cE)+(Mc`OI|7&uObE`<iVs+tJzg7Bnk$EI-oloBu{BL4`RXN{px5_@P`Q!l'
    b'`vkOw6Z-sC&2(Qnvk*MS4Yfbb^?bj__5CdH~0O$S<?oC3n$?#uy2M4!`TH@hY=WSMg-'
    b'<0*fa>7^+3`XhWEu*j<x&KZ~)ml%tS0^{&P+{ow~bX7zP$aV)w+Kt|^eBA9q3Kt0x<Un6FKW3h)WGg1H;eEZzY=fIJG+kHkU|j7v'
    b'w_9QVQQk}ytWjlx`%@4Xecbhslpq{0Qm+{F)s(I``<EKHulbPxcNE_edAgRLy2BPh-G>$cECT8Dw{2-'
    b'95!#Tv51O=nCDl)_lU@o6&ZD=cUUUxAK)LP>q>wJhcz;#i6JjHAH+VRlg6gpqL=Bay7oPUa-56r?71I<I@7$R_O-U+fG%-'
    b'NP_52`WA=b_eX|1RorjnA}{6Lc-W(;3IXcx#p>u-'
    b'1@yYCIbJ$R+Qj|kIDE~a2(7zN{z099cGnjBuy8Tml`4Xq%_t}uN8nPH`Y;!TQws32xpJnfI$SmLD3f%CrlVlsR)*T=Z<?~RN4ItK'
    b'WM=U26RM_?(ji_nBlRCVM8#6xQG1&DrceTT9|R93gzPu@XAA5n_iaa6ov%C!4x6CP&^hv5d<hG{1_Vq#OXTp;aA`>^p&9NZ^Nr2s'
    b'YtaDrx*Zevi2Z-'
    b'ScsJJv5FO5X9YMKYloSiNITjJt34$q(DLX~NNa8U9W$3|aMb3snIQ&G1aff4$CUYl^;E5#hz9B1P1Vjow#o>e!slu6zLlK7aFh2!'
    b';~*QxZElIuD-K|ih$z<p>Q9MLdOY_a%v0wKPt(hTQc)4gL9oY{z+)+l7pR)Bxn+u3gtz|5rL%d?9W;u|%UC>2TBNBH-'
    b'hpYa86M0|tD$YT3g)8waVNryUeiWBJVJa6aE%PjROv)2o-KklG3nEZdKlslzL7m?z!kGSF$hnIFV-NOK9(>c=2geJ5f-'
    b'sT%jgaKK@P2WZ^NlUM0N?Iijl)<j6a+xmFotpC=MMrPHs`y?Z6&2^M1mt;U;JA2XkrR0t-'
    b'=ML1YBCr{PQnb39TVq<{R9666P#@iV~%0?mYWrWE!-'
    b'ppl^(v`cmw+1K39GR`3!s4|I4eX&X#pa4Neh7^Z=hhJn8eIg8>9n%V98+ktQDS7#Z&z}xyGte-7k4S-'
    b'|AxLW!ccvbfQS$_Zk+&QMl=Rg%E}_{2KVGc73eF_dgEgsfQ-'
    b'`On7d5~pV+1KT_z9`dP(res(_e)n<q=<xLL5RSb4?{k+_q0SpQ{)s&*7%!9fJ%qahHT_CxvdIg(%#7vSzPjF?^I<2_T};aKB1}wv'
    b'dMG9EPf($+bfh3O!)9V8l+t$sZ4Gk(HV3M2o-)$r1qKo8ZsYH`!*w-'
    b'|Im2WP#c0lC(NNjo3zZhlQSDn6@h!qQ~VRf)U|>j5tXL8_dPs$xw9<KiT<z#fQ%}BA=4e(@R@%Z%By5wBW%xK${L&Fp9&o!sFy+P'
    b'PnAO6Dc>ekF*d%gn%I;Z}cGg8!E>Pdi)9QYzMC8^;r}ek1T*N=*K~M$c%Kl+fyjkBX@XVLMp@Eh$Tb;#+eO}OD!%&!7ij0Hw32P#'
    b'PE_94is;(G7d_g+N^4zGXaujCWta7A78rG4OPY@W`>DE_?&q79aox&B^us0hUlGeh1fVVmayP*R$R!E7W>Ey2zVp%sq!I=@L?3NQ'
    b'4IrwJ48=v7^tUH%%%~Wg$&k+85x`r-'
    b'JQWFVUZE~sHib+N>py=WY~|=M&G17d3~{m4(zZ%7@6?4ycn(WL|t=(LVCpxD1eL$3rPPGa`63VCs3X5Eo7tWMDGMsZwQR1QXZ8D6'
    b'x@T9O;{ktPF9(v9_tOL3aJu?>Ak;{z6<CLoti<IPzm;eouk&!Qds3eV{yZ+2Iff4aeYh>0t!^*VLzy(F?1G~utNAlU@<pEFfWac)'
    b'hGeVgdfXsIn^U6V3El45y{^?MY!1YqPi>iz!&7hK#)H`|5~AqeoEX7<!HO@gg2@Bxdrm_UUiVRpiw9i?WDdK&bx_B)RP5+4JRX+A'
    b'$YtylYnMO#B!1%QaE1}XPjUK4rBukGGIci3?jHA08lw3$>U25up64U8j*ucjen_kymwm#1G3{XEWR9>oS4A1@Db2N=TvY3#s(=Qe'
    b'lm@Ci122|Hk64R%6_AVBuJXvT`@i<<H*Z^=l~i)^BzWWfB3TE8dKCB_XTkiP*Ci*;VZlzA=ScSv&Mv`XTf^3GYoZLn2(HF!FFRXF'
    b'3wtmtw(qcD*gJKgK6i{Mh0h;TtbENhQ15F5YQmbC%($aj&biR?&EO^_`JaepJfm!-'
    b'0s2rV3#Vxc}WQH<CTtk#9P9{aCaEK*5W#a7&K96P*{<e_fQNRhr)H-jTcC8HmNikjyJircL<~S#-*Mx7#}vm!I<yu@Zc-HkS{6%E'
    b'K&pRe3pgD9(KK0j3e<`0e4(>FzI6)ssQUU%NBKdCLAq+$5>(&Siv(sDlW8;KZ%>$+ddamxHWK%EsyKvb0D#EK9>;>igD?U*<UTp_'
    b'a?N+#w}do<kJeCkF0={G4i#62gjiZqXVHGvd4>?i=QMmVmjk)A~RxfqZwE9@hw5dQ%)?=iSHxGZ0?i>KOa{0z>-'
    b'giiCk=$!L)EjbPC(M6C=vX1o^o?N7hZt=_r<X5=gZ0zObuhy?3JQ61?5U(Cx#3BeX~*<PP@$rZ^pDfZ&H@>ngY)`V|F+0>(q4!u|'
    b'@KMFPo`qA2L5S27n)pNYr*AqJQP@o<%hj2K`~*ax!6TjGS)vM}S=k?Lx6F4z<ngOk0X4GYi4Ck{4*&;S-'
    b'Nm{3j2;Bfz8+L)b9E8?pOgs-T89C{btBnUOGkw~GGff325wnEn=&9I?Z)rW7K>1%jhRL_YmiQ-CdJGLOrjtruYaS;hskdoxoB<F&'
    b'@7J8AM5@Q|(KRp^Ti@bX>qm^J|s1=-{8`RWi1A*&~qZJc%I1h1&Bd7e3sGgl+3Op774_kaNE-'
    b'=sKqxdO2ANGKGUZq9utW(3QZd9E_vtQb>_|ge!F9}#MK7u&|Mv%B9pMC5B{Mas9<Mk6W5o+Kw@BwV`*-'
    b'gi_G34kNaXB`s{1>)OA_pIe6%M0Hf3vK~<`Pxx;f!&M1UP^1{RECX^CpRdmAF2Niz>)x7R7MJ_p+C=VH*RL@ih+HEGJ0e_+yih-E'
    b'l1Lm2GYayDkhIqw^uNHgGyr>{J;eiDiDZPrwfyNECXFx5NlK*u~OG?2Ii`wF;7Rd>0GF#Ap{(2ufy{>S}{PcH{n-'
    b'Wc!Zhh>H<)4XYPl`JznVIL9V3FiUtJvtppTHs&!Q#7<hblxHNXn5py6{{yo!_y_'
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
    candidate = tri  # noqa: F405
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
