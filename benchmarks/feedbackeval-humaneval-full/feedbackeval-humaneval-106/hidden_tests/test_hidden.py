import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[5],
 [7],
 [1],
 [3],
 [0],
 [2],
 [4],
 [6],
 [8],
 [10],
 [100],
 [15],
 [20],
 [12],
 [5],
 [7],
 [11],
 [9],
 [19],
 [99],
 [1],
 [101],
 [98],
 [52],
 [13],
 [3],
 [18],
 [21],
 [102],
 [103],
 [104],
 [105],
 [16],
 [85],
 [65],
 [84],
 [17],
 [14],
 [53],
 [64],
 [83],
 [63],
 [54],
 [81],
 [66],
 [97],
 [96],
 [106],
 [67],
 [95],
 [82],
 [94],
 [55],
 [22],
 [86],
 [70],
 [30],
 [29],
 [68],
 [38],
 [87],
 [31],
 [69],
 [37],
 [62],
 [88],
 [32],
 [93],
 [33],
 [71],
 [80],
 [79],
 [51],
 [61],
 [50],
 [92],
 [49],
 [23],
 [28],
 [24],
 [72],
 [35],
 [34],
 [39],
 [36],
 [41],
 [77],
 [25],
 [89],
 [40],
 [48],
 [42],
 [91],
 [78],
 [47],
 [45],
 [44],
 [76],
 [43],
 [26],
 [27],
 [60],
 [57],
 [90],
 [58],
 [73],
 [74],
 [75]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaGJF;ZEa-J!J9ENOJ3?vdr0N$Ml4LmY~z9t|`)-^BZt1nw;Rd4__*l`{mwX0A7@_(-'
    b'VfByMD{^@`I)1N>8_K*Md_ka1{|GsOtfBgM#GPH-'
    b'3qqRn~A={hUo2M)pb072O#y|cnq<SgOZ@n&U#cA!{_mBVkkAMFkfB)O?_DXo`dfO;c?X2~l7d`!!-'
    b'nG8nR3db0({g0=VtZHL=Dlguzm}=5@!>aGOcy(EP4hj=iPGAf^YuEH-'
    b'8GJQA7aH`lsdYv^GcQ4|5|3gkaMT_^z~TDbx2<pv)r(HW_x~0UvXErQA?Q4HMPXnUZu?P*E0L=JM9*?vhH5Rcw;@qIn2HH)HBAby'
    b'kJ$L7C+9#>^8NZrD5?cBf-J>Gi|iZ%gt2U7`Ld$*|nXht|!<5U%vUOczxIWgxs<Fcg3emn`Jgx+9IB^k-'
    b'45Nn@x|hYrc8gthQ&L{YB#f=J6<_aXfF|Zcb@;%(iE}L)@99>~5`|R=MhTMwF=$Ysc=&kQu;ncE0;n>GIbych@a)mvgqaN<ECN_^'
    b'90K*uz!)mSeoW*K-'
    b'D}cDhA4H?(dq^RH#RwH7Vv@HIomj&iqJ=LVzqSq8_Paprwm9W>l=bYAXomeQSfeaqP0T*cW<ia*|OzUr_#Dj47+ooNAX<~`UXFZg'
    b'L?t<hf9y|;dc61xmSyALk|I{4srLyI&Zzk{n#o3do>UVEvRAI`a7X{ztU2R~4{_lU{~?$up#OaK=)adL1n&N}TrUU^#H14OFH5p8'
    b'|6UcZ4a2le~4*unmnPVQSCh#AwvXW4h%7bCz*pTnh;?VLb&7u!p}yZP_M@KZ{#K-'
    b'dYl2~OHQ<%Nzu7fTmTI+Kh7uYu0)qsQf6WtvyUw;QhSwyS-rPixwhgK)S%G_C9KGMKVp(z--f@4c3{?ipZp)OWt!%q_4^Zhi$n7K'
    b'Q9rrr*{J!0m41|LcaUnTI@UXZmvi2(5j~jJv|xJGa>ARWDnGsbd^xvZdAAbhRf8954!-'
    b'Ev!^$V}8tO{uisC8QRbmQqmS&TAQD3t_I9$Bv`rpH>yqcihe0VcH{x361`dR?@$4w2kfid$E?epj~!v?3MwJ3qcWqny1+MYL{-'
    b'n}4H&gp<9+HkkL@#7S!eiu`%T^jspbLzcfnP#S&BT)WZ_4TzdC^HX<pE>?`|H%E7e7gLKfG4gEvkN7+nBZlZx1Tt4#mw!)_V)wtK'
    b'f&b@%^TXK=RnmY7vU0KsePh;fp$?qJ@bd+ogDh0N-mt4TxRm}^K6pz<xVsui_$ft*cy5=Bczc&`^*zU%C$%-'
    b'jy}x3(&+t=BsuFj#MWccairLL(;(Hulgp1}5?_q0Mc~*Sax-aVvX0VN34uRTvWz`(wDhYlT7Y9`8Qu6ZrKCcz2Q81DK&Mh|d6b=z'
    b'c8#S&ksnfQRKiPFc!Pl{-0zvhi1nzQR!s07IMFgF|OlEh*~8|4_;C;(42+ea>*3O_qHZ5j}wgS%2l)d#@U90T-'
    b'|+<u=wz@Xi}s;MfXmjNyHUV$k*3HmMc*!opkMg7LWMsBp1bJQJKr`>VckWN0x<PGnQX{#qu)xOVhrEiSf!jGEue+5c$O={SlBD7d'
    b'I>2OYxzP_*{YXPEofGAaJf3x|t`)mKrcQ)-'
    b'!${P5(YNgTc!Pl<=V0Gi$!OvZZn?}y@wWpElkbOKB9hw>flsWyY7c*XM3L0*Gf4y7O8vm|{2!7aamYe2J!6JYYoP&#0O>A;o~@I*'
    b'J_&51{yqMGxlrrafwXx7uq=bD|20sqRInBpyM=tGkWb4Q{dJfE2lu#P=;1<fb~YTsi3k{;(bsaMyPbx{y#`MB1}UYI7s#Otdq_0p'
    b'{%RDRi=*t6sPwfD-|?|$$@R-6-'
    b'e^mcR8cRmsh01H@+GGd%0r^Se&7SUuVaAHT3fo<sc3B@$&7%hpU<C|MiVi|355Gabi3~su!8A8q`L<CqKAiVb-aen#cjdD-'
    b'd7kiY20^p%qSLH9Z7Sn4-'
    b'm*T{8*9?uM2sjE0Iqc)Ef6H_X2ovQDlTRvH^rA`tICESMiYvpsCFWk0c?J>e`gmL)Fdko`NLQI;C$v<FoObT9V_<X)T$^lE3T%hs'
    b'+|4Mu69oWd6YR#Y{}dqylMpnqG!i3FeMb$t`-'
    b'Fuc9tcO<z^H&XUUp@dw~`|TGx~PZW=An6ffwdt@O(5K59nXv?Y@w+i;x8pOEj3P23C=VT<83unAlv<HRO(A0|y2+aD5<24CE&SPW'
    b'&<Llu*mW4ns#SNn3jY#E(-'
    b'13Z#GByi#__JPt%iFDn@lkv}qbAu(6P_$<;d7vv`u0QrvZipK(y9r}}XxwB3laa@I*2CEKezl8YK8_3?kt|KetdgPzc7_sGBhS5&'
    b'a)V-EI*oDso9#9kn6u<=PdK44cL`K-DUemK6IZm%%Fi93(QrgqY{5bO9O5l1!Df+0*A;%xOLP&+3NYj|;XQuia`VG8-'
    b'%!w;9W87e3^7sh1o@s{wvM%nji^BSoIVretHgo#o6np=oz)Lmo1PHl!COFRBoXR`#z|A-'
    b'jiGYfvlz{9r=nl~YszQA1=<}(4>%^B=s}FQ~Zo6FU=(K(whKlXU;GQu<;yLPQE(*f5T;;&uz)Q+6vMQh(L<k}3`lhg~f{Ua7nJkt'
    b'O?VF?mFW5kQe%Kq3{nW2;A0*~ZOh-'
    b'~Sw+(XOI+&9!z>goUW!=5RxM*^LTP?E;aklpO4#go?bD~KZHcr7g(NyS^dI8?KchV&3lx9L^7ygmd;T73Zef$Ovq;7KvNMH!QmLk'
    b'F>uth@Gpo0yvr2L6)jpT`g5+XU#1XuH?#RQQ~_~{6%5pB~E1O>XS_PKjY)wrm@-1Hg)fvuRyX+kJ-'
    b'_+`I#2Q)I_LYG67Y1kyLWyD4J{SZ4PVj#79pT{JUc&K9`-'
    b'hg`j4Ll<Tody@!()~TmK7%MRLeQTyRT?@xGpYnwL~CBfgqNZ$ReyQ|iRL54XOvjD39Il{($a3;xK;4RZQQXy3T{ssfZ>&#WVB8BJ'
    b'e&aG<QKk(M%dvb<IY@L$oz$2vklJzOnwBYbTZf?5QAcNiDvf~XgedZBAG$Pywz$&oP`eXQr~6uz{6n?0?6F6)t7@)Kv&-'
    b'O;ieRXZDpIx?6CFH3@UxKUE+EtC~<1zyC4Z<C*szjqh(=LPW4M$@aqs%2?3Di5W~$130I-9dj>v?9pYj-'
    b'w=wqU1d4>1MiYkn!7ss1QyDm3hDm}M21p~KOfFU@s<g}g79k-ul9ncH^F}sc<o4I@CastXM%XQ{l0_SXxp-'
    b'hjVFm?_veRV~Y|ujJR*O0JqP5`<cYm_g&t=k3gmYB-JX+Hy!KIzui3tUmyhBm}&}>mN>>#CwGzW;IezJwb(W;>$psm~s`MuE{0>w'
    b'C0othVXFFlHl)=F5$qf+`Pc$wh8fu~*yZjCgQ1RANHwyVGcW{<4j(Plo#ARau;0&ifNSpn+-A->%(;VcE|$_NRSWo%P09f@T-*{-'
    b'P0hIS4p;-sWaRAg<G0?GVPOiH3mKtBlhr_>I|RmO^e{&i#uk;1bU<YJx}qC<GO8BWu-zFbU&Lg{7=BCl8S``U!?dhc@rJv<<=6PJ'
    b'k<nXCmo>qb85Cw<`_-'
    b'=uPDaWbrL+>02=A}?(y&qFm&ib{dB6!wk55jQ#e1!~~F{v;hdM$nDiF;%!gX@iLHm=fBk&VVv1)qxhnDR_6`!z`!{c{G0UT6n{Id'
    b'<VQkMZL^+Gydljs=K?aLe}7*Ojto3$^7C7fD3&8;728ZGn^F~Os<YLo<U*bqgaV;R-'
    b'YU~lup9MqJ<P&WLf@%ul0M<cF~V~%t&=&6`B)eEFT1AzrgoUx>5F}JtHIdeLh4ggN-IE>#qp0%Ye|tU!V>&i2=fRp)=Q#y%G~3mD'
    b'2MM4pC_RS~G`ZAU$j3$8aTOU`JeF1e%3<=i^ZVQI_UG(I-^2OcA&#I<E!ABIUsj#undhu<4u-'
    b'VLAow_Pi$A!pt3#NOZEG0?TIEm?>HWHueg8s1x>knuK?+JqZKt0xqrylwhhP^NbDLW^;-'
    b'w>d4<V0TJ_(^V;qCP&0n;OR8{=jCYv;ot%`|?VyxNY{IQyBGlO&f=EX<2Gz`((n~VyUljNwo~tzwN3iVBDYygVf1N=;KOnqP(W5O'
    b'#Y;ba@j)G8_C)r+p?JhV9ndDDO65#fFv~1y&zCprf;~a=cvY;w9GZfmP*|-'
    b'S~S3le|%kD*=6jo>(UD^TRiJArbD<qw_tPH|=y@Sk)>2Azu9}IC`|JhxKIXIWiAnh*TTT$V`<#tcy#NqEHvow-DTDG2ZM@tA{WJz'
    b'T1yW&Me+Gs0#f@|!85D|oN$+Gh2X%*iz5EtYo_0jWjXL)Pqlj!(8FZO$wRiv<4J~$=ELP45yJ^-'
    b'loVN*^xcvuv`COPd}jMVAGJvjSwhJ3tui47#7LbM=ZVJ76xd=8mFn2L70C7dv4Sc)F#ATb=8!*@5@^6QyVU{=`#*gy=93b|>o6yq'
    b'GbgX0sC*TkFW$Vco*31a)9n7V>@I6tCP4Bg|6e4a)Vyu5AG9T*#V9f7CFOsuMaJ~Dak>en?F&BZdjKt*E2%x;ZN3Yi1$9|}D2lB`'
    b'c1>648bhz20m^Pvp)^HI|q-~I&D3c5m1IPbL8j6m8+yNC*Zrc+>WXM79bV6+U8<5CKLdIL;1*@Qxbmu)H+GC?@F`55bx_->-'
    b'JH_A{5F`GJRAdBou+nV2`HsNJssPqijRUej_7~H4k*AWXjFt8(r`AH22iTE0|y3=5o=<msXd1f4*{L10{(dh*f=P#^8J#_Ak<^p9'
    b'0{e&i8J<S0}6FUAU6d5-tW3A>dA#fLG^!6ti+e<ITF+suW7@aEb+8xcZ+|eR&&tKS|;ICq5O^J>LUBI`JQmMy66ohAM^V3Yn1o-'
    b'(_j5@6&A5qCK3XmmmMcpi~i?r96R)tm&gtujr_N-e5x+-lSMPcgPQ8h-}e-'
    b'FVC>;vZ!ZDvw?{?@@PpEOfHJ8_p{P5fK1{0&E_HepPT*4;WO@pr`!Ln2Z!ouT577XAhn%?AOyFnHqnc5vMR^cv*e?1orkK4<wo*$'
    b'+m2F&S#@qK-Y!XX%Wn5l<p526?@!(3%%(@kZ**N&R^Fu<|EcNUur9aLKyRkyCeq1dWHl=jak!B_czihHQF~HL-'
    b'<DgCiV5m@iS##So6mVu7a;A4qshF=W8KjG2<n`F6lZz<gw_eC#5e)Tt3fgzs)3HCl&^Qd6;|!);SEwreE_<*(l^6`tKQJ~*72gVs'
    b'sJGn8zr{2pc+A>kNa4&qi8cv8f!lD}B^^TZb{-s02^B@;g`O5hZ!H5=|p`1!y7KldV_1O'
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
    candidate = f  # noqa: F405
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
