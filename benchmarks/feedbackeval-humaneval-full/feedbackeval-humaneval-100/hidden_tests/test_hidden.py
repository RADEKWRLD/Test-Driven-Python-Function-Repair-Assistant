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
 [8],
 [1],
 [2],
 [10],
 [15],
 [20],
 [100],
 [12],
 [25],
 [50],
 [14],
 [16],
 [9],
 [24],
 [99],
 [21],
 [51],
 [52],
 [22],
 [73],
 [17],
 [3],
 [101],
 [72],
 [98],
 [97],
 [53],
 [13],
 [4],
 [96],
 [92],
 [102],
 [23],
 [11],
 [93],
 [49],
 [78],
 [86],
 [71],
 [95],
 [94],
 [70],
 [77],
 [69],
 [79],
 [103],
 [68],
 [37],
 [18],
 [36],
 [67],
 [91],
 [35],
 [8],
 [90],
 [48],
 [54],
 [87],
 [19],
 [85],
 [84],
 [55],
 [7],
 [104],
 [5],
 [38],
 [74],
 [39],
 [83],
 [66],
 [80],
 [105],
 [47],
 [109],
 [65],
 [6],
 [42],
 [89],
 [46],
 [40],
 [88],
 [82],
 [108],
 [110],
 [64],
 [111],
 [26],
 [57],
 [58],
 [63],
 [59],
 [45],
 [106],
 [41],
 [81],
 [62],
 [107],
 [56],
 [43],
 [75],
 [30],
 [32],
 [33],
 [29],
 [34],
 [31],
 [76],
 [27],
 [28],
 [44],
 [1000000],
 [60],
 [61]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO*JGL!1Ziel^9*09mUL^Pevz~|p0t8p*9)KM=>QJ7qKiqZeXaee`)|GV5u3`cIv-bb|%m4lNzx~s%|NZA5|Nf7E{ja|t8S{^S'
    b'{4I`bIp?%`!gox!HuUzWeaxa~oK?<Ucg)$>xb8Oi@fd4q?E1F;@xOok{h$BwH$QW}Ql^hF+wuC|9J@=eqrWm^_c-'
    b'^|Uak0*tLjHrURQ_p6BfTOQ?-n?n(+CzT6-'
    b'2!<~g$3D9diFe(RaNZ1K1Dp0Z2ZUUl|SRdoEmOh0>+9#3AoZ@lQSinx{I^TcfP_E~CK%}u+tEp<HcRToE*Q|5P>H?5T+TgyEwwmp'
    b'g2z1(?^wZ^keJLk$itIHW8uG-'
    b'|Cs9Qu&`DP=xmnwJlr%|Wftuu}md!=_(rYX9o?`1W{s<X`dimbs6Z;>kBX|9cHOQp?f)?L|9joWOj;ZnvaeZA4^@oqMcwq^V5dg_'
    b'W99P}IU@_04W*IvRRL)NMLika6^7B{IZY(8ys*7<rE_gl|913mYi`Ll498EfBGxfGjZ*EW@t^%kt~-V$|`#-'
    b'6N+*7B_EA&&v;w79=7Giz%V2v~5hJKeR7Rs6hn?1fkE{$_n%EbOqa!w6*6FfMymtsic7d1W0wc7v_W>Q?J*dRP=c=zAZ#t%b+%h<'
    b'EqsV>Q4uSZ0gzGvapVyrXjL*JRdutm-'
    b'Z1Yt5zGL3H5&Z?E3Vl=+518kWW*SLxrvTN|_2e)8~7ht^%2o$`VSh^k%ab~SOd{VDThAU$OG5}@{71{5^EyTF?U4g2DHHsnsGss%'
    b'^`%r&KNwzGHPh%gzf7FNh8+waSaa5ISH`|b`<TkhX>s|;n1aqk_jhbcqI%GO4cwN@EZmMxa~amr6+VguAZ-MedH%PtdYSJ4DueG{'
    b'TFJpPlz<7$2@&j*kJ&+p4v)42{f?{#Vd?})-'
    b'KInlMjr1j(;C<3yZX{!aKUef^2(m}{~8Nhzw!1T##f&7%h02L(wzcre~Lca<JlaZg}=#bM})B2X%@5=yq)_Ut?HdZ7dG8UslaC%|'
    b'?r!5@=#70N>Ku3U!ipFVoZt35qZbxu*NC3Jk6A7G9pmmKC%c1?)Z9rwF{l+owHb(R6=&M}&PIHIlZY4N3kneHJeyua_ig58LJ8=`'
    b'o6rLj>C{-'
    b'_9uMHMiy8N7mQ6Ze1s$J(p`uYgdeH?{|Qc*@8HrnM3Z>~@js<O<T`uaXj31kx}!=Fg|^Lk~py|~!Ex{)lKxA>gnX|G<Ga}uP%DG^'
    b'lgV|aTF)Pv#SCKJ?`$v-~~MjwtL4*BN;Kl=rr@=~we-jS(cob?+q=Zksg60VN@+|akih6~cxY{+z~7N3R`W5JDzZ`3_eQ<HV?`hA'
    b'(d$nF}j_g#3b`wlA8rur6B*e<Ax_i1}VrHZT_vxO+1woy2sxKuw*&GfgkBO+DYu$ya-3-'
    b'5*kZna;WLI@FfDNCYz+Mo`8RvaVxW@BUHg0*9nAV~Eflyxu0ivBn4Xj#MZc%(H=VgFqKTG4@4pxk#FRN*DuZDELW;Vp)!F>4s>OP'
    b'hnYiSXafzgC_bv%Kh9iuaB`XCr;;+*klE<%srbJO|(@lMxh?y8S+9o$=OF&Z6Ge#4)VC@ngPMqX-'
    b'}&QfLLpw<mPOqYx~jsm;(?820H<2*uw`$pGMNkL}~H4JPOzbOcF-9Tu(!pC@GZ*<Q>7-Yy!^*)%$-x-'
    b'z3MT43FqhWn4*Eg)GAy3G)Ja2+(SkUoZ4LCKS6KnK4-Nl63?=`NTmd&1Vgg<E>dT}WcIO1#-#niXYFD<Qk|RJ3!7jhS&~)Y-'
    b'<6N)D<OIruh31Yl1<av&%;*eJ6(F#wk+t`{0FG6CL`Ry?`?UPuxHD{P<V|9zSBh(UHZ^^LnuG#I&g9<BONGO#-'
    b'Asz`5DD_H^s%j{yH2}v*CYz`Tz0XIRb?mR%JmrMXw7_;&uB)=Lyke`K(pNuMe91%cn`rDsRrN5P`Bh~ccQKSL#;+&JwPXv_*Vew|'
    b'5dmo;(Y@V7CUhNH-ea?V3E5jItC<mb~7BhPue2K&Z)E!UZ{1wpN6J)bqR)Q%~V?It@GGjT!QEotl0P09LL6&reb$Sp29#{Yehz#M'
    b'PBRYrMAX?G^*C$(`o;&XINCN|3(Uovy280MkpZd;fis8$hopC~z@09~?a>M5g?kV&D&Bz&;s|q<*N>{Q(e^3#7%J4M@>S~;?A5MW'
    b'8dOd@@@WGFmvB@&VWPl<FLAqha^w^|hTMjslfINBj{?Jfdtwlcz-He}2C4y&hz%{S<!IE(QiIr8yfzc=)lZ1@%z;Uve?QxMUM4mN'
    b'?e?H~AQWE-'
    b'3fgxkttBCt1B=Zm_g=UU)yXU|Zd#}cym?bwmAU@tlO%zu5fDdQQ5gF;4$AK54T_S=;2PTXf5|NHeYM>zZ^p$sN{WewcxCA)v#q$p'
    b'ng_FCnpar|&BG;SoYr^CdY@AfT@L1`@EtT{8GQ_hExOe74mMtNuX9g4$`Z<}Kpi|O+TmF&~Vc)*}1qnl$&j&x0V<5hszecc(j`o2'
    b'(rvhQEbO+>_=0fVgrop7=!*ZvZgW^$tUq%5Ybb|myt7MSa;-{>BH^4Tb5gM;OL&o5wTgcIJfI&T|;CC5103#t9ccRZ@aM|-'
    b'nfdZ)}J{KHGF`ms~Gq5888$R)9@V1U0pUN_#tn^?jnA&=bnq!eknEXMP5$?57PLmDi3~?jIlNe}IF@J<YoT0NW5(Ll#?D*{NMuU3'
    b'fqqZ@tN$8+rk}K2N8|7heJW>YX;HTYj)3Q-Bsp~osid$7ci%yVCD;*TF5aY62&=7Gj{(tgP5_^4mLkC57Nw3_D#14@*a-'
    b'DSQ$X|n;*caQKq;2GoZ1*@yH#Uw&Ui)h+D+r6+UUor{+n6!XFUTrr-'
    b'w?g6Ly5hqj#Lj0K#ZjIwCv@*eIu@*W9^pV)abJ$k+>sOj|UqR@kKBc{OxdN4oF>qTnHUIjPUp2h8PD0xiC)9gdBDOD%L==BExmMT'
    b'r0Gwf}jx{J&WpEL^+a`%YC0uaUT=B0rgsK1i6&}($iSUR~dU40K6x#(V58?Xvv0mIP4}I{JC&~^ogvsmpySi;tQP+Ii#5ypij*}4'
    b'{r?qPC~~U5$6X`IaU3%nBkJhB-8zPgfQ%lMf8+WI2tkXV9sR~=RvrIr5!XXHlkX73N-'
    b'%)9_JJ~%qn;ugx+uqmW}pki^x<91=NBZ@+_(F&n{1f(EW5x5c$*zTJ#dK66Snh&6|W=ijl*J9xM&Pra)drj(yMUnul78qkckx9TR'
    b'#BeF*klph|=rXV890Wt8B8(sNRHN5jK`2zGRmRMUZZeLdV1Nj$_En(d|ZmP)|p;MwgFVQ8umJ)cde8=kKhOcO^qG=1y*wQrMrL{b'
    b'D1R}vbk-dIns6~51#X$|DDgj6yz!x75OMt{hOMhCX<GSp(~Y<c+(;dZ6@oosO|$1pioVgyLqBY6h4<$D2KIq8hCd-'
    b'*}}Ev+*ZB8G6ohCteaULAv^=8{ivWYkddox{cZGoeDh<sG-'
    b'j$iD1H600aB8zfupg>7R=%&IS@Mu25NgxbiEQ>coSY(QwBO%Re;#djIIjogNlq5C4(6C<b(A)hX9ZX!h%c(OeMj)f`?y3oTGdv4~'
    b'FbOoE6h)E^~b+pJg-'
    b'^_?lk|P3;C+%L(s7iX~QD4g<Nm}0^fTZ_rO7vzh3<q|Lt_}r(#f!8*@;C@?%s*rpWP^Z;&t#^<8x)p)BFafLGf~DPqEbaINhMPTZ'
    b'Z>-'
    b'pk~st0<UCYl0bHt9&Ysl}KR)%tPFP;nB%GgF)<O>28M1kt_ekm|n0KH2ozf2u>0LfBJX$3>^pSyFjozZQm@k2`fCehoAdF)y$isL'
    b'zFdrn86mU7X3RJl5tyOv8zxJKz%Fx#v)f|H(i2w$si*(?zluE^!sp($Pmt_G_hzeM2NqEoKzK1H9JLP*@<VT6TSlie<2E|rtYl_Y'
    b'Rq9Xg<d@m&i1~VR#(Ga_@mgSoZ`ZgEe>m|9Z<CSL+?MU@Y$ppw6f8g4}@!nzXSj(z{6V9JRK_kd+LX%;plR}G9z|)uS?MOwLP6!l'
    b';GLl1^AxmDcjM$QlT)q)+FoD<s%L;~>FraE|ABiJXBM`(j4jav!R)kXKqv~PK@PGX*953Wo+pkxa8b;P`nlJXu+-'
    b'c$$zAxbzfS9C%qTm#r6(t^l$Cryy*GBJZISp6=t-(D6PUR%z5iQ2fH!}R-'
    b'vWtR}uzw0EtY8h_hy~9g;bL$ENt6*oqlX||2mu*(L7~TfJYz3L0hS(s4um(-'
    b'Q$M}w>7jF>hm>{fnm|)7W{><ZV97%G6x~DkSikqmF#USP!*Kok%_gxxN>Xyx*e745k*dh)C^{jBhY)N9-'
    b'Ju4IejWu6shq=+k`t`vTlhx%Ch>==Jm3+r!!6%a6LRw9BXyr1jJ4sRC6*342#B6S0fGD9Y5F}I4dQ?Rk0?x?nIl>EKq@iyBH*O_I'
    b';bf5iXf{}m7VoEU$%VNkCq9z!Q~*jOXCM#7Yg}E|1>sXk?<10QDq*~r$Q0lHv40i_Gk5AgCL#yNusB|Gf#N2od*QfC^MyO2rEK~`'
    b'k>GBl5bx#<ABiiv#C|dN0B`W10LyQC}>V1Uu73;;5iaNnl4!ZN%#^VWM#F|Ie*}XAf3b<_-'
    b'LsCK@vr^l~BUIeId=Phq2FTPWytNjt>FRZLsa9`L>BS(lrQ2IKN~s!*wx7qPa0?D^z&$22M&Qtk^Jpi3A_n`aan*JgnvmheC}lq-'
    b'==CuT&7LSUNUIOxg<#h{q$+Hn!z=02>0IGtW=gM15fb-U1zZ@`Y^5X)vu(OMtU?vzWJxL6B?Hnh4SKawsPs{B)5-&GTy-'
    b'd>Rt+6r?z{ILsrzY=P+bJ27G`FbW%#W083F>g#93hz<S^IXP?aQJUoIH-%F-'
    b'uqR?O@?7K~#IbFJ=b}rGZkf`4f8L3brtu$Q5)qB+0!D}*i;V-*y*9nz2niJ9-KZJazbYMvArnUJdno#bG5ew!kSR-'
    b'm0y5tYHEzBTqv<L)Cc%2p=Lqt2bkaCc6swmnQ9J~ln5U^HcVpKVgXK|(DrnbyUFo7kXPx<Wi~$;92YVsW=SV+EXWIxReS+A4d?>o'
    b'mtEX8M41ra>Msp&Kj7$m}k`s;#{gh<E+3ly@QKo6KhaCkPNX;Ynqe=)g76=h)1{b14e?W(@ns0_-'
    b'v9<mPKHp^=Dauzk%o)i9{*|o)K_*jqOx6_E2&7D-'
    b'kT+Yt6Wx>otm{(zzwAe(ifJVGOiD29(COGddV<&hf&7Y*kWF#nSMc<kZ{rAE8&(~WKXWnM<Ec0fe-'
    b')FJUzTkYi==%{zJ%he`PCu~j;Kis$(J!>lbKrilIU<8!<=28zUX1jqm!p2-'
    b'#`%xi5vMf9*aLEhxW23oXyDT0$YAKg=C@hsP9uQgJU~KB7QI&py3_->+_7d_Q>uK^;ZUnvnd+#<C-'
    b'w{R8%run+=!6Y^!Bx2t;?#pYm%G&YxMAG#BY4l<JMU5-ESa*K``q#-@}b{(8?XbpH$FfRAM91;<P|-we<-'
    b'=tZX^gILsD`EA|Da9mztG(sT@DrMMe*f&;v=)i{m5iIEBk_;7;8A0ow@2^c{{CovSFGJ|47x=DHfc@m#49~thaLLH8a7wO|qmJT1'
    b'mCbL>sL79D{86)~uM$nultv&Lnx)}990jWZ$S0MYkuCC+^!qYy_S0O6P~)e1a6=A3^mrHAM83|rWMU4S>nB<>exo{(7|<BnEs>Ts'
    b'yD)yKK$XkHfBZl9gj8G'
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
    candidate = make_a_pile  # noqa: F405
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
